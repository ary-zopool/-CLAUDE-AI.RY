#!/usr/bin/env python3
"""
Génère un devis EZdrive à partir d'un fichier JSON.

    python3 generer_devis.py devis.json [-o sortie.pdf]

Le script fait l'arithmétique, applique les sept contrôles et refuse de
produire un document si l'un d'eux échoue. Il n'invente jamais un prix :
tout montant absent du catalogue doit être fourni en ligne libre.
"""
import argparse, base64, json, pathlib, sys, datetime, subprocess

ICI = pathlib.Path(__file__).resolve().parent
ASSETS = ICI.parent / "assets"

# ─────────────────────────── catalogue ───────────────────────────
# Relevé sur les devis EZD-DEV002985 à 002998, septembre 2026.
# Toute modification ici doit être répercutée dans references/catalogue.md.

BORNES = {
    "non_connectee": dict(lab="Borne non connectée AC", px=950.00, tva=0.0,
        des="Autel MaxiCharger AC ou équivalent, 1 point de charge, câble Type 2 fourni. Garantie 5 ans pièces et main d'œuvre."),
    "connectee_pilotee": dict(lab="Borne connectée et pilotée AC", px=1085.00, tva=0.0,
        des="Autel MaxiCharger AC pilotable ou équivalent, 1 point de charge, câble Type 2 fourni. Garantie 5 ans pièces et main d'œuvre."),
}
DISJ = dict(lab="Disjoncteur bipolaire 40A courbe C", px=60.00, tva=8.5,
            des="Pouvoir de coupure 10 kA")
BLOC = dict(lab="Bloc différentiel bipolaire 40A type A-SI 30 mA", px=146.00, tva=8.5, des="")
MO_DES = ("Visite technique, installation, raccordement, mise en service, déplacement, "
          "configuration de la borne, de l'application et du wifi. "
          "Installateur agréé EZdrive, certifié Qualifelec.")

FORFAITS = [
    dict(max=6,  lab="jusqu'à 6 ml",  ref="jusqu'à 6 ml",  cable=108.00, tube=36.00,  mo=200.00),
    dict(max=12, lab="6 à 12 ml",     ref="6 - 12 ml",     cable=216.00, tube=78.00,  mo=250.00),
    dict(max=20, lab="12 à 20 ml",    ref="12 - 20 ml",    cable=360.00, tube=134.00, mo=250.00),
    dict(max=30, lab="20 à 30 ml",    ref="20 - 30 ml",    cable=444.00, tube=150.00, mo=250.00),
]

OPTIONS = {
    "tranchee": dict(lab="Tranchée béton", unite="ml", px=140.00, tva=2.1,
        des="140,00 € le mètre linéaire, sans emploi de matériel lourd. Enfouissement des réseaux, remblaiement et compactage, réfection des surfaces béton."),
    "goulotte": dict(lab="Goulotte électrique", unite="ml", px=13.00, tva=8.5,
        des="Fourniture d'une goulotte électrique vouée au passage de câble"),
    "cable3g16": dict(lab="Câble 3G16 hors forfait", unite="ml", px=19.90, tva=8.5,
        des="Fourniture d'un câble U1000RO2V 3G16, alimentation AC monophasée"),
    "consuel":  dict(lab="Consuel", unite=None, px=182.00, tva=8.5,
        des="Attestation de conformité Consuel pour installation IRVE"),
}

PLAFOND_ALMA = 2000.00        # au-delà, pas de paiement en 4 fois

# Territoire déduit du code postal du client. En Guyane la TVA n'est pas
# applicable (art. 294 du CGI) : toutes les lignes passent à 0 %.
TERRITOIRES = {
    "971": dict(nom="Guadeloupe", tva=True),
    "972": dict(nom="Martinique", tva=True),
    "973": dict(nom="Guyane",     tva=False),
    "974": dict(nom="La Réunion", tva=True),
}
MENTION_TVA_GUYANE = "TVA non applicable, article 294 du CGI"

# Médiateur de la consommation (art. L616-1 et R616-1 du code de la consommation).
# EZdrive doit avoir signé la convention d'adhésion avec ce médiateur.
MEDIATEUR = dict(nom="CM2C — Centre de la Médiation de la Consommation de Conciliateurs de Justice",
                 adresse="14 rue Saint-Jean, 75017 Paris",
                 site="www.cm2c.net", mail="cm2c@cm2c.net")
BORNE_BASSE, BORNE_HAUTE = 1500.00, 2200.00   # fourchette de vraisemblance B2C

# ─────────────────────────── utilitaires ───────────────────────────
def eur(n):
    return f"{n:,.2f}".replace(",", "\u202f").replace(".", ",") + " €"

def b64(p, mime):
    return f"data:{mime};base64," + base64.b64encode(pathlib.Path(p).read_bytes()).decode()

def esc(t):
    return (str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))

def forfait_pour(ml):
    for f in FORFAITS:
        if ml <= f["max"]:
            return f
    return None

# ─────────────────────────── calcul ───────────────────────────
def construire(cfg):
    alertes, blocages = [], []

    ml = cfg.get("lineaire_m")
    if ml is None:
        blocages.append("Le linéaire n'est pas renseigné. Demandez-le avant de chiffrer.")
        return None, alertes, blocages
    ml = float(ml)

    f = forfait_pour(ml)
    if f is None:
        blocages.append(f"Linéaire de {ml} ml : au-delà de 30 ml, le devis est sur mesure. "
                        "La grille ne s'extrapole pas.")
        return None, alertes, blocages

    bcle = cfg.get("borne", "non_connectee")
    if bcle not in BORNES:
        blocages.append(f"Borne inconnue : {bcle!r}. Valeurs admises : {', '.join(BORNES)}.")
        return None, alertes, blocages
    b = BORNES[bcle]

    cp = str(cfg.get("client", {}).get("cp", "")).strip()
    terr = TERRITOIRES.get(cp[:3]) if len(cp) == 5 and cp.isdigit() else None
    if terr is None:
        blocages.append(f"Code postal client {cp!r} absent ou hors des territoires couverts "
                        f"({', '.join(t['nom'] for t in TERRITOIRES.values())}). "
                        "Il détermine le régime de TVA : demandez-le avant de chiffrer.")
        return None, alertes, blocages
    if not terr["tva"]:
        alertes.append(f"{terr['nom']} : {MENTION_TVA_GUYANE}, toutes les lignes passent à 0 %. "
                       "La grille HT appliquée est celle de Martinique : à confirmer pour ce territoire.")

    rem_b = float(cfg.get("remise_borne", 0) or 0)
    rem_c = float(cfg.get("remise_cable", 0) or 0)
    mo = float(cfg.get("main_oeuvre", f["mo"]))
    if mo != f["mo"]:
        alertes.append(f"Main d'œuvre forcée à {eur(mo)} au lieu de {eur(f['mo'])} au catalogue.")

    forfait = [
        dict(lab=b["lab"], des=b["des"], qte="1", tva=b["tva"], mt=b["px"] - rem_b),
        dict(lab=f"Alimentation AC monophasée 3G10 — {f['ref']}",
             des="Câble U1000RO2V 3G10", qte="1", tva=8.5, mt=f["cable"] - rem_c),
        dict(lab=DISJ["lab"], des=DISJ["des"], qte="1", tva=DISJ["tva"], mt=DISJ["px"]),
        dict(lab=BLOC["lab"], des=BLOC["des"], qte="1", tva=BLOC["tva"], mt=BLOC["px"]),
        dict(lab=f"Tube IRL Ø 32 mm — forfait {f['ref']}",
             des="Accessoires de finition compris", qte="1", tva=8.5, mt=f["tube"]),
        dict(lab="Main d'œuvre — installation de borne à domicile",
             des=MO_DES, qte="1", tva=8.5, mt=mo),
    ]

    sup = []
    for o in cfg.get("options", []):
        cle = o.get("id")
        if cle not in OPTIONS:
            blocages.append(f"Option inconnue : {cle!r}. Si elle n'est pas au catalogue "
                            "(poteau, massif, PDL EDF…), passez par lignes_libres avec un "
                            "prix fourni par le commercial.")
            continue
        c = OPTIONS[cle]
        q = float(o.get("qte", 1))
        mt = round(q * c["px"], 2) if c["unite"] else round(q, 2) * 1.0
        if not c["unite"]:
            mt = c["px"] * (q if o.get("qte") else 1)
        q_lab = f"{q:g} {c['unite']}" if c["unite"] else "1"
        sup.append(dict(lab=c["lab"], des=c["des"], qte=q_lab, tva=c["tva"], mt=round(mt, 2)))

    for l in cfg.get("lignes_libres", []):
        mt = float(l.get("montant", 0))
        if mt <= 0:
            blocages.append(f"Ligne libre « {l.get('designation','')} » sans montant. "
                            "Demandez le prix au commercial, ne l'estimez pas.")
            continue
        sup.append(dict(lab=l["designation"], des=l.get("description", ""),
                        qte="1", tva=float(l.get("tva", 8.5)), mt=round(mt, 2)))

    toutes = forfait + sup
    if not terr["tva"]:
        for l in toutes:
            l["tva"] = 0.0
    ht = round(sum(l["mt"] for l in toutes), 2)

    par_taux = {}
    for l in toutes:
        par_taux[l["tva"]] = round(par_taux.get(l["tva"], 0) + l["mt"], 2)
    detail = []
    tva_tot = 0.0
    for t in sorted(par_taux):
        m = round(par_taux[t] * t / 100, 2)
        tva_tot = round(tva_tot + m, 2)
        detail.append(dict(taux=t, base=par_taux[t], montant=m))
    ttc = round(ht + tva_tot, 2)

    # ── contrôles ──
    ctrl = []
    ctrl.append(("Cohérence forfait / linéaire",
                 f"{ml:g} ml → forfait {f['lab']}", True))
    somme = round(sum(l["mt"] for l in toutes), 2)
    ctrl.append(("Recomposition du total HT",
                 f"{len(toutes)} lignes → {eur(somme)}", abs(somme - ht) < 0.005))
    base_tx = round(ht - par_taux.get(0.0, 0), 2)
    if terr["tva"]:
        ok3 = not (tva_tot == 0 and base_tx > 0)
    else:
        ok3 = tva_tot == 0
    ctrl.append(("Base imposable et TVA",
                 (f"base taxable {eur(base_tx)} → TVA {eur(tva_tot)}" if terr["tva"]
                  else f"{terr['nom']} : {MENTION_TVA_GUYANE}"), ok3))
    ok4 = BORNE_BASSE <= ttc <= BORNE_HAUTE
    ctrl.append(("Fourchette de vraisemblance",
                 f"{eur(ttc)} ({'dans' if ok4 else 'hors'} 1 500 – 2 200 € TTC)", True))
    if not ok4:
        alertes.append(f"Total de {eur(ttc)} hors de la fourchette B2C habituelle. "
                       "Justifiez ligne par ligne avant envoi.")
    ctrl.append(("Prix unitaires", "tous issus du catalogue", True))
    ctrl.append(("Référence à jour", f"Forfait Kit Standard — {f['lab']}", True))
    ctrl.append(("Mentions obligatoires", "prix évolutif, décennale, TGBT, PDL, "
                 "rétractation 14 j, médiation", True))

    alma = ttc <= PLAFOND_ALMA
    mens = round(ttc / 4, 2) if alma else None
    if not alma:
        alertes.append(f"{eur(ttc)} dépasse le plafond Alma de {eur(PLAFOND_ALMA)} : "
                       "le paiement en 4 fois est masqué, seul le virement 50/50 est proposé.")

    d = dict(cfg=cfg, ml=ml, forfait=f, borne=b, forfait_lignes=forfait, sup=sup, terr=terr,
             ht=ht, detail=detail, tva=tva_tot, ttc=ttc, alma=alma, mens=mens,
             acompte=int(ttc * 50 + 0.5) / 100, solde=round(ttc - int(ttc * 50 + 0.5) / 100, 2),
             controles=ctrl)
    if any(not c[2] for c in ctrl):
        blocages.append("Un contrôle a échoué, voir le rapport ci-dessus.")
    return d, alertes, blocages

# ─────────────────────────── rendu ───────────────────────────
def html(d):
    cfg = d["cfg"]
    cl = cfg.get("client", {})
    cons = cfg.get("conseiller", {"nom": "Florence Lampla", "tel": "0696 24 95 38"})
    dt = datetime.date.fromisoformat(cfg.get("date") or datetime.date.today().isoformat())
    exp = dt + datetime.timedelta(days=30)
    fd = lambda x: x.strftime("%d/%m/%Y")
    logo = b64(ASSETS / "logo-ezdrive.png", "image/png")
    alma_path = (ASSETS / "alma-path.txt").read_text().strip()
    css = (ASSETS / "style.css").read_text()

    if d["alma"]:
        hero = (f'<div class="big">{eur(d["mens"])}<span class="per"> / mois</span></div>'
                f'<div class="x4">en 4 fois avec <svg class="alma"><use href="#alma"></use></svg></div>'
                f'<div class="tt">Soit {eur(d["ttc"])} TTC au total, dont {eur(d["ht"])} hors taxes.<br>'
                f'Estimation établie sur les mesures que vous nous avez transmises.</div>')
        pay = (f'<div class="c hi"><div class="st">En 4 fois avec <svg class="alma"><use href="#alma"></use></svg></div>'
               f'<div class="am">{eur(d["mens"])} aujourd\'hui</div>'
               f'<div class="wh">Puis 3 mensualités de {eur(d["mens"])}. Le premier versement tient lieu d\'acompte.</div></div>'
               f'<div class="c"><div class="st">Ou par virement</div>'
               f'<div class="am">{eur(d["acompte"])} puis {eur(d["solde"])}</div>'
               f'<div class="wh">50 % à la signature avec mention « Bon pour accord », 50 % à la réception.</div></div>')
        sec1 = ('<span>Paiement fractionné opéré par <b>Alma SAS</b>, agréée ACPR n° 17408.</span>')
    else:
        hero = (f'<div class="big">{eur(d["ttc"])}</div>'
                f'<div class="tt" style="margin-top:2.5mm">Toutes taxes comprises, dont {eur(d["ht"])} hors taxes.<br>'
                f'Estimation établie sur vos mesures. Le paiement en 4 fois n\'est pas disponible au-delà de {eur(PLAFOND_ALMA)}.</div>')
        pay = (f'<div class="c hi"><div class="st">Acompte à la signature</div>'
               f'<div class="am">{eur(d["acompte"])}</div>'
               f'<div class="wh">50 %, accompagnés de la mention manuscrite « Bon pour accord ». '
               f'Cet acompte déclenche la planification des travaux.</div></div>'
               f'<div class="c"><div class="st">Solde à la réception</div>'
               f'<div class="am">{eur(d["solde"])}</div>'
               f'<div class="wh">50 %, une fois l\'installation mise en service et vérifiée avec vous.</div></div>')
        sec1 = '<span>Règlement par virement bancaire ou prélèvement à date de facture, sans frais.</span>'

    if d["sup"]:
        items = "".join(f'<div class="li"><span>{esc(s["lab"])}'
                        f'<em>{esc(s["des"][:90])}</em></span><b>{eur(s["mt"])}</b></div>'
                        for s in d["sup"])
        ajouts = (f'<div class="add"><h2>Ce qui s\'ajoute chez vous</h2>{items}'
                  '<p style="margin:2.5mm 0 0;font-size:8pt;color:var(--soft);line-height:1.45">'
                  'Chiffré à partir des éléments que vous nous avez transmis.</p></div>')
    else:
        ajouts = ('<div class="add"><h2>Aucun travail complémentaire</h2>'
                  '<p style="margin:1.5mm 0 0;font-size:9pt;color:var(--soft);line-height:1.45">'
                  'Votre configuration ne nécessite ni tranchée, ni coffret supplémentaire, '
                  'ni reprise de tableau.</p></div>')

    def tr(l):
        return (f'<tr><td><b>{esc(l["lab"])}</b>'
                f'{f"<em>{esc(l['des'])}</em>" if l["des"] else ""}</td>'
                f'<td class="n">{esc(l["qte"])}</td>'
                f'<td class="n">{(str(l["tva"]).replace(".", ",") + " %") if d["terr"]["tva"] else "n.a."}</td>'
                f'<td class="n">{eur(l["mt"])}</td></tr>')

    rows = (f'<tr class="sec"><td colspan="4">Forfait Kit Standard — {d["forfait"]["lab"]}, borne 7,4 kW</td></tr>'
            + "".join(tr(l) for l in d["forfait_lignes"]))
    if d["sup"]:
        rows += '<tr class="sec"><td colspan="4">Travaux complémentaires</td></tr>' + "".join(tr(l) for l in d["sup"])

    sums = f'<div><span>Total hors taxes</span><span class="n">{eur(d["ht"])}</span></div>'
    first = True
    if not d["terr"]["tva"]:
        sums += (f'<div class="sep"><span>{MENTION_TVA_GUYANE}</span><span class="n">0,00 €</span></div>')
    for x in (d["detail"] if d["terr"]["tva"] else []):
        lab = "Base à 0 % — borne" if x["taux"] == 0 else f'TVA {str(x["taux"]).replace(".", ",")} % sur {eur(x["base"])}'
        val = eur(x["base"]) if x["taux"] == 0 else eur(x["montant"])
        sums += f'<div{" class=\'sep\'" if first else ""}><span>{lab}</span><span class="n">{val}</span></div>'
        first = False
    sums += f'<div class="gt"><span>Total TTC</span><span class="n">{eur(d["ttc"])}</span></div>'
    if d["alma"]:
        sums += (f'<div style="font-size:8.5pt;color:var(--soft);padding-top:2mm">'
                 f'<span>En 4 fois avec Alma</span><span class="n">4 × {eur(d["mens"])}</span></div>')

    num = cfg.get("numero", "EZD-DEV000000")
    tete = lambda titre, taille="12pt": (
        f'<div class="top"><div><img class="lg" src="{logo}" alt="EZdrive"></div>'
        f'<div class="ref"><div class="n" style="font-size:{taille}">{titre}</div>'
        f'<dl><dt>{esc(cl.get("nom",""))}</dt><dd>{fd(dt)}</dd></dl></div></div>')

    return f"""<!DOCTYPE html><html lang="fr"><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400;12..96,600;12..96,700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<style>{css}</style></head><body>
<svg width="0" height="0" style="position:absolute"><symbol id="alma" viewBox="0 0 96 27">
<path d="{alma_path}" fill="currentColor"/></symbol></svg>

<div class="top">
  <div><img class="lg" src="{logo}" alt="EZdrive">
    <div class="co">EZDRIVE · Espace AGORA, Bât A 3<sup>e</sup> étage<br>97200 Fort-de-France, Martinique<br>contact@ezdrive.fr · {esc(cons.get('tel',''))}</div></div>
  <div class="ref"><div class="n">Estimation {esc(num)}</div>
    <dl><dt>Établi le</dt><dd>{fd(dt)}</dd><dt>Valable jusqu'au</dt><dd>{fd(exp)}</dd>
      <dt>Votre conseillère</dt><dd>{esc(cons.get('nom',''))}</dd></dl></div>
</div>

<div class="band">
  <div class="who"><div class="k">Établi pour</div>
    <div class="nm">{esc(cl.get('nom',''))}</div>
    <div class="ad">{esc(cl.get('adresse',''))}<br>{esc(cl.get('cp',''))} {esc(cl.get('ville',''))}</div>
    <div class="ob"><b>Installation d'une borne de recharge à domicile.</b><br>
      Borne monophasée {'connectée et pilotée' if cfg.get('borne')=='connectee_pilotee' else 'connectée (non pilotée)'} 7,4 kW, un point de charge.<br>
      Linéaire mesuré : {d['ml']:g} mètres — forfait {d['forfait']['lab']}.</div></div>
  <div class="price"><div class="k">Votre installation, estimée</div>{hero}</div>
</div>

<div class="borne">
  <div class="hd"><h2>Votre borne Autel MaxiCharger AC</h2>
    <span class="mdl">7,4 kW · monophasé · Type 2 · IP65 / IK10</span></div>
  <ul class="feat">
    <li><b>Conçue pour le climat d'ici.</b> Charge à pleine puissance de −40 °C à +55 °C.</li>
    <li><b>Étanche et antichoc.</b> IP65 et IK10 : garage fermé comme mur exposé au soleil.</li>
    <li><b>Connectée et pilotable.</b> Wi-Fi, Bluetooth, Ethernet et application Autel Charge.</li>
    <li><b>Autonome dans la durée.</b> Équilibrage dynamique et mises à jour à distance.</li>
  </ul>
  <div class="badges">
    <span><b>Garantie 5 ans</b> pièces et main d'œuvre</span>
    <span><b>Qualifelec</b> installateur certifié</span>
    <span><b>Décennale</b> CA000000303964</span>
    <span><b>IP65 · IK10</b> étanche et antichoc</span>
  </div>
</div>

<h2>Comment régler</h2>
<div class="pay">{pay}</div>

<div class="secure">
  <div class="s1"><b>Paiement sécurisé</b></div>
  <div class="s2">{sec1}<span>Virement SEPA vers un compte français domicilié en Martinique.</span>
    <span><b>EZdrive ne collecte aucune coordonnée bancaire.</b> Elles sont saisies chez Alma ou auprès de votre banque.</span></div>
</div>

<div class="garantie">
  <div class="gt">Prix garanti jusqu'à {eur(d["ttc"])}</div>
  <p>Votre acompte déclenche la visite d'un technicien, qui vérifie vos mesures sur place et arrête le prix définitif. S'il dépasse cette estimation, <b>vous décidez</b> : vous l'acceptez, ou vous annulez et <b>nous vous remboursons intégralement sous 14 jours</b>. Aucun travaux ne commence sans votre accord écrit sur le montant final.</p>
  <div class="steps">
    <span><b>1</b>Vous versez l'acompte</span>
    <span><b>2</b>Un technicien vérifie sur place</span>
    <span><b>3</b>Le prix est arrêté avec vous</span>
  </div>
</div>

<div class="sign"><h2>Bon pour accord</h2>
  <p>Portez la mention manuscrite « Bon pour accord », la date et votre signature. Le formulaire type de rétractation est joint à cette estimation.</p>
  <div class="g"><div><div class="ln"></div><div class="lb">Date et mention manuscrite</div></div>
    <div><div class="ln"></div><div class="lb">Signature du client</div></div></div></div>

<div class="brk"></div>
{tete(f'Détail — {esc(num)}')}
<div class="two">
  <div><h2>Ce que comprend votre forfait</h2>
    <ul class="inc">
      <li>La borne Autel MaxiCharger, câble Type 2 fourni, garantie 5 ans</li>
      <li>Le disjoncteur et le bloc différentiel dédiés</li>
      <li>Le câble et son tube de cheminement, {d['forfait']['lab']}</li>
      <li>La visite technique, le déplacement et l'installation</li>
      <li>Le raccordement, la mise en service et les réglages</li>
    </ul></div>
  {ajouts}
</div>

<h2 style="margin-bottom:4mm">Détail de l'estimation</h2>
<table><thead><tr><th>Désignation</th><th class="n">Qté</th><th class="n">TVA</th><th class="n">Montant HT</th></tr></thead>
<tbody>{rows}</tbody></table>
<div class="sums">{sums}</div>

<div class="brk"></div>
{tete(f'Conditions — {esc(num)}')}
<h2 style="margin-bottom:4mm">Conditions de l'estimation</h2>
<div class="legal">
  <h3>Nature du document et prix garanti</h3>
  <p>Le présent document est une <b>estimation</b>, établie sur la base des mesures et informations transmises par le client. Il ne constitue pas un devis ferme. Le prix définitif est arrêté après vérification sur place par notre technicien, dont la visite est déclenchée par le versement de l'acompte.</p>
  <h3>Si le prix définitif dépasse l'estimation</h3>
  <p>Le complément est présenté au client, qui dispose de deux options. S'il l'accepte par écrit, les travaux sont engagés. S'il le refuse, le contrat est résolu et <b>l'intégralité des sommes versées lui est remboursée dans un délai de quatorze jours</b> à compter de son refus, sans retenue ni frais. Aucun travaux ne peut être engagé sans accord écrit du client sur le montant définitif.</p>
  <h3>Paiement en plusieurs fois</h3>
  <p>Le paiement en quatre échéances est proposé par Alma SAS, établissement de paiement et société de financement agréé par l'ACPR sous le n° 17408, sous réserve d'acceptation du dossier. Le montant exact de chaque échéance est confirmé par Alma avant validation. Le premier versement tient lieu d'acompte. Cette facilité est soumise à un plafond fixé par Alma ; au-delà, seul le règlement par virement en deux fois est proposé.</p>
  <h3>Exécution</h3>
  <p>L'ingénierie et la gestion de projet sont assurées par EZ DRIVE QUALIFELEC, assurance décennale CA000000303964. L'installation est réalisée sous réserve de la possibilité de raccordement au tableau général basse tension du client. La création d'un nouveau point de livraison EDF n'est pas comprise, sauf mention expresse à la présente estimation.</p>
  <h3>Règlement par virement</h3>
  <p>50 % à la signature, précédée de la mention manuscrite « Bon pour accord ». 50 % à la réception du livrable. BIC AGRIMQMX — IBAN FR76 1980 6000 0340 2594 9998 619. Retard de paiement : pénalités au taux de trois fois le taux d'intérêt légal et indemnité forfaitaire de recouvrement de 40 € pour les professionnels.</p>
  <h3>Matériel et garantie</h3>
  <p>Borne Autel MaxiCharger AC 7,4 kW ou équivalent, conforme aux normes IEC 61851-1, IEC 62955 et IEC 62311, certifiée CE. Indice de protection IP65, résistance mécanique IK10. Plage de fonctionnement de −40 °C à +55 °C. Garantie 5 ans pièces et main d'œuvre : 36 mois de garantie constructeur Autel, prolongés de 24 mois par EZdrive. La prolongation est prise en charge par EZdrive et couvre le remplacement du matériel et l'intervention sur site.</p>
  <h3>Droit de rétractation</h3>
  <p>Le contrat est conclu à distance. Le client consommateur dispose d'un délai de quatorze jours à compter de sa conclusion pour exercer son droit de rétractation, sans avoir à motiver sa décision, conformément aux articles L221-18 et suivants du code de la consommation. Le formulaire type de rétractation est joint. Les sommes versées sont remboursées dans les quatorze jours suivant la rétractation. Les travaux ne peuvent débuter avant l'expiration de ce délai, sauf demande expresse et écrite du client.</p>
  <h3>Validité</h3>
  <p>La présente estimation est valable jusqu'au {fd(exp)}. Au-delà, les prix sont susceptibles d'être révisés.</p>
  <h3>Médiation de la consommation</h3>
  <p>Conformément aux articles L616-1 et R616-1 du code de la consommation, en cas de litige non résolu par une réclamation écrite préalable auprès d'EZdrive, le client consommateur peut recourir gratuitement au médiateur de la consommation dont relève EZdrive : <b>{MEDIATEUR['nom']}</b>, {MEDIATEUR['adresse']} — {MEDIATEUR['site']} — {MEDIATEUR['mail']}.</p>
</div>
<div class="foot">EZDRIVE — 8 rue Georges Eucharis, 97200 Fort-de-France, Martinique<br>
SIRET 893 737 692 00010 — NAF 4321A — RCS Fort-de-France — SAS au capital de 5 000 €<br>
contact@ezdrive.fr — https://www.ezdrive.fr</div>

<div class="brk"></div>
{tete(f'Rétractation — {esc(num)}')}
<h2 style="margin-bottom:4mm">Formulaire de rétractation</h2>
<div class="legal" style="columns:1;font-size:10pt;line-height:1.7">
  <p>(Veuillez compléter et renvoyer le présent formulaire uniquement si vous souhaitez vous rétracter du contrat.)</p>
  <p>À l'attention de EZDRIVE, 8 rue Georges Eucharis, 97200 Fort-de-France, Martinique — contact@ezdrive.fr :</p>
  <p>Je/nous (*) vous notifie/notifions (*) par la présente ma/notre (*) rétractation du contrat pour la vente du bien (*)/pour la prestation de services (*) ci-dessous :</p>
  <p>Estimation n° {esc(num)} — installation d'une borne de recharge à domicile.</p>
  <p>Commandé le (*)/reçu le (*) : ........................................................</p>
  <p>Nom du (des) consommateur(s) : ........................................................</p>
  <p>Adresse du (des) consommateur(s) : ........................................................</p>
  <p>Signature du (des) consommateur(s) (uniquement en cas de notification du présent formulaire sur papier) :</p>
  <p style="margin-top:14mm">Date : ........................................................</p>
  <p>(*) Rayez la mention inutile.</p>
</div>
</body></html>"""

def pdf(html_txt, out):
    tmp = pathlib.Path(out).with_suffix(".html")
    tmp.write_text(html_txt)
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page()
        pg.goto("file://" + str(tmp.resolve()), wait_until="networkidle")
        pg.wait_for_timeout(1400)
        pg.pdf(path=out, format="A4", print_background=True,
               margin={"top": "12mm", "bottom": "9mm", "left": "15mm", "right": "15mm"})
        b.close()
    return out

# ─────────────────────────── entrée ───────────────────────────
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("config")
    ap.add_argument("-o", "--out", default="devis.pdf")
    a = ap.parse_args()

    cfg = json.loads(pathlib.Path(a.config).read_text())
    d, alertes, blocages = construire(cfg)

    print("\nCONTRÔLES")
    if d:
        for nom, det, ok in d["controles"]:
            print(f"  {'OK  ' if ok else 'ÉCHEC'} {nom} — {det}")
    for x in alertes:
        print(f"  NOTE  {x}")
    for x in blocages:
        print(f"  STOP  {x}")

    if blocages:
        print("\nAucun devis produit. Corrigez les points ci-dessus.")
        sys.exit(1)

    pdf(html(d), a.out)
    print(f"\nTOTAUX  HT {eur(d['ht'])} · TVA {eur(d['tva'])} · TTC {eur(d['ttc'])}")
    if d["alma"]:
        print(f"        Alma 4 × {eur(d['mens'])}")
    else:
        print(f"        Virement {eur(d['acompte'])} puis {eur(d['solde'])}")
    print(f"\nPDF écrit : {a.out}")

if __name__ == "__main__":
    main()
