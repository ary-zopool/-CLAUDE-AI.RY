---
name: presentation-ezdrive-ezsolar
description: "Construire une présentation (Artifact Slides) combinant une offre EZsolar (photovoltaïque) et une offre EZdrive (borne de recharge) pour un même client B2B — structure pragmatique-puis-rassurance, double marque, annexe CGV. Utilisable à partir de liens Drive d'une étude PV (rapport de dimensionnement, devis, fiches) : lecture des fichiers, extraction des chiffres et visuels, puis slides commerciales."
---

# Présentation combinée EZdrive + EZsolar

Déclenché par : "fais-moi une présentation" / "proposition commerciale" pour un client ayant
un projet EZsolar (PV) et, en complément, un besoin de borne(s) EZdrive — ou l'inverse.

## Outil

Artifact de type **Slides** (pas un PDF, pas de HTML маison). Lire le `SKILL.md` du type
avant de commencer. Toujours vérifier `list` avec `type` "Design System" d'abord — si rien
n'est marqué par défaut et que rien n'est explicitement prévu pour ce type de document
commercial (ex. la DA "DA EZD 1" est réservée aux pubs Meta, pas aux présentations), partir
sur une direction propre, pas réutiliser une DA hors-sujet.

## Entrée : liens Drive de l'étude (utilisable par toute l'équipe)

Déclenché aussi quand l'utilisateur colle un ou plusieurs liens Drive d'une étude PV et demande
les slides commerciales. Le skill suppose un compte Claude de l'organisation avec le connecteur
Google Drive activé.

1. **Lire chaque lien** avec le connecteur Google Drive (métadonnées, puis contenu ; pour un PDF
   dont le texte ne suffit pas, télécharger et lire avec PyMuPDF). Connecteur absent ou lien
   refusé : le dire tout de suite et demander l'activation ou le fichier. Ne jamais reconstituer
   un contenu non lu.
2. **Repérer la source des chiffres** : le rapport de dimensionnement EZ SOLAR (PDF). Les autres
   fichiers (devis, fiche borne ou onduleur) le complètent. Si deux fichiers se contredisent,
   signaler l'écart sans trancher.
3. **Écrire le tableau de données avant de composer** : client et site ; puissance (kWc), modules,
   onduleur ; production annuelle ; besoins ; autoconsommation et surplus ; coût HT, aides, reste
   à charge net ; économie annuelle ; délai de retour ; gain sur 20 ans ; hypothèses (dégradation,
   indexation des prix). Chaque valeur cite son fichier et sa page. Une valeur absente s'écrit
   `[à compléter]` : jamais de chiffre inventé ni estimé de tête.
4. **Extraire les visuels du rapport** (rendu 3D, vue satellite) et les logos des fiches
   constructeur, comme décrit plus bas. Aucun visuel généré.
5. **Composer les slides** selon la structure validée ci-dessous. Chaque chiffre affiché vient du
   tableau de l'étape 3.
6. **Une présentation = un seul client** : ne jamais reprendre les chiffres, noms ou offres d'un
   autre client, même anonymisés, sauf demande expresse d'Ary.
7. **Rendre compte avant partage** : lister les `[à compléter]`, les hypothèses non confirmées
   (ex. délai de versement d'une aide) et les écarts entre fichiers. L'artefact reste privé
   tant que l'utilisateur ne le partage pas. Rien n'est envoyé au client sans validation d'Ary.

## Structure validée (ordre des slides)

1. **Couverture** — nom du client, titre, les deux offres annoncées si les deux sont présentes.
2. **Pragmatique d'abord** : combien ça coûte, combien le client paie réellement (reste à
   charge net après aides), AVANT tout argumentaire technique.
3. **Retour sur investissement** : revenu annuel, délai de retour, gain cumulé sur 20 ans.
4. **Dimensionnement énergétique** chiffré (besoins vs production vs autoconsommation vs surplus).
5. **Rassurance matériel** : marques reconnues (photos et logos réels des fabricants, jamais
   générées), garanties, normes.
6. **Méthode** : rigueur de l'étude (données réelles, indicateurs P50/P75/P90).
7. **Tenue dans la durée** : dégradation modélisée, prix indexés.
8. Si offre complémentaire (ex. borne EZdrive en plus du PV) : slide coût pragmatique de cette
   offre, puis slide détail/rassurance — même logique pragmatique-puis-rassurance en miniature,
   intégrée dans la même présentation plutôt qu'un document séparé.
9. **Équipe / prochaines étapes** — logos des deux marques si les deux offres sont présentes.
10. **Annexe CGV et mentions légales**, TOUJOURS en toute dernière position, jamais mêlée aux
    slides de contenu commercial. Contenu : nature de l'offre (contrat distinct par entité
    juridique), garantie, règlement, validité, et le point clé B2B :

## Point juridique B2B à ne jamais oublier

Si le client est une société (SARL, etc.) et non un particulier : le droit de rétractation de
14 jours et la médiation de la consommation (articles L221-18 et L616-1 du code de la
consommation) NE s'appliquent PAS de plein droit — seulement aux consommateurs, sauf cas du
« petit professionnel » (art. L221-3). Ne jamais copier les clauses consommateur résidentielles
dans un document B2B sans ce caveat écrit noir sur blanc.

## Visuels : toujours sourcés, jamais inventés

- Logos et photos produit : extraire des documents officiels déjà en possession (rapport
  d'étude EZsolar, fiche technique constructeur) via PyMuPDF (rendu haute résolution + recadrage
  + fond blanc rendu transparent par seuil colorimétrique), ou téléchargés directement par
  `curl` depuis le site officiel du fabricant (ex. fiche PDF Autel/Huawei) si rien n'est fourni.
  Ne jamais utiliser un logo tiers depuis un site de redistribution à licence incertaine
  (seeklogo, cdnlogo, etc.) — dans ce cas, préférer un traitement texte sobre (nom de marque
  dans sa couleur officielle) plutôt qu'un logo dont la licence n'est pas claire.
- Photos de site : extraites du rapport de dimensionnement officiel (vue satellite, rendu 3D
  du bâtiment) si disponible — jamais une photo de banque d'images générique.

## Logo en coin, sur toutes les slides

Petit badge discret en haut à gauche (`position:absolute; top:48px; left:48px`), fond blanc,
coins arrondis (`border-radius:8px`), padding `8px 14px` :
- Slide de couverture et slide de conclusion/équipe partagée entre les deux offres : les deux
  logos côte à côte, séparés par une fine ligne verticale (`width:1px;height:20px;background:#d8d3c4`).
- Chaque slide de contenu : le logo de la marque à laquelle appartient cette slide (EZsolar pour
  le PV, EZdrive pour la borne), hauteur ~22-26px, `object-fit:contain`.
- L'annexe CGV d'une offre donnée porte le logo de cette offre, pas les deux.

## Palette et typographie par défaut (sans système de design fourni)

Nuit `#0f2030`, panel `#16293b`, papier `#f5f2e9`, accent or `#c69a3b`, texte clair `#f5f2e9`,
texte sombre `#17222b`, gris doux `#5c6771`/`#8b96a0`/`#9aa6b0`. Titres en `Source Serif 4`,
texte courant en `Inter`. Alterner fond nuit (slides chiffres-choc) et fond papier/blanc
(slides détail) plutôt que tout sur un seul ton.

## Ce qui a déjà existé comme erreur à ne pas refaire

- Ne pas dupliquer un même logo en inline ET en position absolue sur la même slide (nettoyer
  l'ancien placement avant d'ajouter le badge standard).
- Ne pas inventer un mécanisme de financement non confirmé (ex. délai de versement d'une aide) :
  le signaler explicitement comme "à confirmer avant signature" plutôt que de l'affirmer.
- Toujours revérifier le contenu d'une slide avant de la modifier si l'utilisateur a pu l'éditer
  à la main entre-temps (voir le `edits` counter dans l'`artifact-view-context` fourni par le
  client — un nombre qui augmente signifie qu'il faut relire avant d'écraser).
