#!/usr/bin/env python3
"""Prépare les leads Meta (exports CSV du Leads Center) pour l'agent Trello.

Usage : python3 preparer_leads.py fichier1.csv [fichier2.csv ...] [-o leads.json]

- Fusionne les exports (souvent cumulatifs) et garde un lead par e-mail + date de création.
- Normalise le téléphone au format +596 696 12 34 56 et corrige le « 0 » en trop
  des numéros saisis en +5960696… (signalé dans « corrections »).
- Déduit le territoire de l'indicatif : +596 Martinique, +590 Guadeloupe,
  +594 Guyane, +262 La Réunion ; autre indicatif = « Hors territoire ».
- Classe le domaine de l'e-mail : « grand public » (gmail, orange…) ou « à vérifier »
  (domaine d'entreprise probable, à confirmer par l'agent).
Le script ne contacte aucun service : il lit les fichiers et écrit un JSON.
"""
import csv, json, re, sys, argparse
from datetime import datetime

GRAND_PUBLIC = {
    'gmail.com','googlemail.com','hotmail.com','hotmail.fr','live.fr','live.com','outlook.com','outlook.fr',
    'msn.com','yahoo.fr','yahoo.com','icloud.com','me.com','orange.fr','wanadoo.fr','sfr.fr','free.fr',
    'laposte.net','neuf.fr','mediaserv.net','canl.nc','outremer-telecom.fr','aol.com','gmx.fr','proton.me','protonmail.com'
}
TERRITOIRES = [('+596','Martinique'),('+590','Guadeloupe'),('+594','Guyane'),('+262','La Réunion')]
COLONNES = {
    'cree': ['Créé','Created','created_time','Date de création'],
    'nom': ['Nom','Full name','full_name','Nom complet'],
    'email': ['Adresse e-mail','Email','email','E-mail'],
    'tel': ['Téléphone','Phone','phone_number','Numéro de téléphone'],
    'source': ['Source'], 'formulaire': ['Formulaire','Form','form_name'],
    'etape': ['Étape','Stage'], 'proprietaire': ['Propriétaire','Owner'],
}

def col(row, cle):
    for c in COLONNES[cle]:
        if c in row and row[c] not in (None, ''):
            return row[c].strip()
    return ''

def norm_tel(t):
    if not t:
        return '', None
    t = re.sub(r'[^\d+]', '', t)
    correction = None
    if t.startswith('00'):
        t = '+' + t[2:]
    if not t.startswith('+'):
        if t.startswith('0') and len(t) == 10:
            # numéro local sans indicatif : 0696… / 0690… / 0694… / 0692-0693…
            pref = {'0696':'+596','0697':'+596','0690':'+590','0691':'+590','0694':'+594','0692':'+262','0693':'+262'}.get(t[:4])
            if pref:
                t = pref + t[1:]
                correction = 'indicatif ajouté'
    for ind, _ in TERRITOIRES:
        if t.startswith(ind + '0') and len(t) == len(ind) + 10:
            t = ind + t[len(ind) + 1:]
            correction = '0 en trop retiré après l’indicatif'
    return t, correction

def joli(t):
    for ind, _ in TERRITOIRES + [('+33','')]:
        if t.startswith(ind) and len(t) == len(ind) + 9:
            r = t[len(ind):]
            return f'{ind} {r[0:3]} {r[3:5]} {r[5:7]} {r[7:9]}'
    return t

def territoire(t):
    for ind, nom in TERRITOIRES:
        if t.startswith(ind):
            return nom
    return 'Hors territoire' if t else 'Inconnu'

def date_iso(s):
    for f in ('%m/%d/%Y %I:%M%p', '%d/%m/%Y %H:%M', '%Y-%m-%dT%H:%M:%S%z', '%Y-%m-%d %H:%M:%S'):
        try:
            return datetime.strptime(s, f).isoformat()
        except ValueError:
            pass
    return s

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('fichiers', nargs='+')
    ap.add_argument('-o', '--sortie', default='leads.json')
    a = ap.parse_args()
    vus, leads, lignes = set(), [], 0
    for f in a.fichiers:
        with open(f, encoding='utf-8-sig', newline='') as fh:
            for row in csv.DictReader(fh):
                lignes += 1
                email = col(row, 'email').lower()
                cree = col(row, 'cree')
                cle = (email or col(row, 'tel'), cree)
                if cle in vus:
                    continue
                vus.add(cle)
                tel, corr = norm_tel(col(row, 'tel'))
                dom = email.split('@')[1] if '@' in email else ''
                leads.append({
                    'nom': col(row, 'nom'), 'email': email, 'telephone': tel, 'telephone_affiche': joli(tel),
                    'territoire': territoire(tel), 'recu_le': date_iso(cree), 'recu_le_brut': cree,
                    'formulaire': col(row, 'formulaire'), 'source': col(row, 'source'), 'etape_meta': col(row, 'etape'),
                    'domaine_email': dom, 'type_domaine': 'grand public' if dom in GRAND_PUBLIC else ('à vérifier' if dom else 'aucun'),
                    'corrections': [corr] if corr else [],
                    'autres_champs': {k: v for k, v in row.items() if v and k not in sum(COLONNES.values(), [])},
                })
    leads.sort(key=lambda x: x['recu_le'])
    # doublons à l'intérieur des fichiers (même e-mail ou même téléphone, dates différentes)
    par_cle = {}
    for i, l in enumerate(leads):
        for k in (l['email'], l['telephone']):
            if k:
                par_cle.setdefault(k, []).append(i)
    for idx in par_cle.values():
        if len(idx) > 1:
            for i in idx:
                leads[i].setdefault('meme_personne_que', sorted(set(leads[j]['nom'] for j in idx if j != i)))
    json.dump({'lignes_lues': lignes, 'leads_uniques': len(leads), 'leads': leads}, open(a.sortie, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f'{lignes} lignes lues, {len(leads)} leads uniques → {a.sortie}')
    terr = {}
    for l in leads:
        terr[l['territoire']] = terr.get(l['territoire'], 0) + 1
    print('Par territoire :', ', '.join(f'{k} {v}' for k, v in sorted(terr.items(), key=lambda x: -x[1])))
    corr = [l for l in leads if l['corrections']]
    if corr:
        print(f'{len(corr)} numéro(s) corrigé(s) :', ', '.join(l['nom'] for l in corr))
    pro = [l for l in leads if l['type_domaine'] == 'à vérifier']
    print(f'{len(pro)} domaine(s) d’e-mail à vérifier (entreprise probable) :', ', '.join(f"{l['nom']} ({l['domaine_email']})" for l in pro) or 'aucun')

if __name__ == '__main__':
    main()
