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
9. **Barème CRE : les aides baissent** (fond nuit) — la prime de la tranche de puissance du
   client, trimestre par trimestre, et l'évolution du prix du kWh. Voir « Slides 9 et 10 ».
10. **Compte à rebours du barème** (fond papier, accent or) — la date de fin du barème en cours,
    la règle du tarif figé, et ce que nous faisons d'ici là. Voir « Slides 9 et 10 ».
11. **Équipe / prochaines étapes** — logos des deux marques si les deux offres sont présentes.
12. **Annexe CGV et mentions légales**, TOUJOURS en toute dernière position, jamais mêlée aux
    slides de contenu commercial. Contenu : nature de l'offre (contrat distinct par entité
    juridique), garantie, règlement, validité, et le point clé B2B :

## Slides 9 et 10 : le barème CRE (urgence factuelle, jamais de pression)

À inclure quand l'installation PV relève du barème « S24 PV ZNI » de la CRE (bâtiment, 500 kWc
au plus, zones non interconnectées : Martinique, Guadeloupe, Guyane, La Réunion, Corse, Mayotte,
etc.). Hors de ce cadre (métropole, installation hors bâtiment, plus de 500 kWc), ne pas les
faire et le dire dans le compte rendu. Ces deux slides portent le logo EZsolar et se placent
APRÈS les slides de l'offre complémentaire et AVANT « Équipe / prochaines étapes ».

**Données (à écrire dans le tableau de l'étape 3, avec le fichier et la date de mise à jour)**
- Télécharger le fichier officiel de la CRE (open data) :
  `https://www.cre.fr/fileadmin/Documents/Open_data/Transition_energetique_et_appels_d_offres/Tarifs_PV_ZNI.zip`
  (fichier « Tarifs S24 ZNI T.. »). Lire avec `openpyxl` (`data_only=True`).
- Onglet « Autoconsommation » : première partie = prime à l'investissement (€/Wc), seconde =
  tarif d'achat du surplus (c€/kWh). Onglet « Vente en totalité » si le projet vend tout.
  Le nom du territoire figure sur la première ligne de son bloc ; les tranches P + Q
  (0-3, 3-9, 9-36, 36-100, 100-500 kWc) suivent. Les lignes « entre le… » et « et le… » donnent
  les dates de chaque trimestre. Contrôler à l'écran le territoire et la tranche lus.
- Retenir la tranche de la puissance du client (P + Q) et le territoire du site.
- La dernière colonne est le trimestre en vigueur. Si la date du jour est postérieure à sa date
  de fin, le fichier est périmé : télécharger la version à jour, ou le dire.
- Prime du client = prime €/Wc de la tranche × puissance en Wc. Elle doit retrouver l'aide du
  tableau de l'étape 3 ; sinon signaler l'écart sans trancher.
- Prix du kWh : tarif Bleu EDF option base 6 kVA publié par la CRE (série août 2016 à aujourd'hui) ;
  si absent du fichier lu, ne pas afficher la variation.

**Slide 9, « La prime baisse chaque trimestre »** : barres de la prime €/Wc de la tranche du
client, du premier trimestre du fichier (janvier 2024) au trimestre en vigueur ; le pic et le
niveau actuel étiquetés ; la variation en % entre le pic et aujourd'hui, en très gros. Si l'axe ne
part pas de zéro, l'écrire sous le graphique. Un second bloc donne l'évolution du prix du kWh
(en %, valeurs de départ et d'arrivée). Source écrite sur la slide : « CRE, barème S24 PV ZNI,
[territoire], mise à jour [mois année] ».

**Slide 10, « Le barème actuel s'arrête le [date] »** : la date de fin du trimestre en vigueur,
en très grand ; trois points : la CRE révise le barème chaque trimestre ; le tarif et la prime
sont ceux du trimestre où la demande complète de raccordement est déposée ; contrat d'achat
de 20 ans (à confirmer sur le contrat d'achat EDF avant de le promettre). Puis ce que nous
faisons d'ici là : l'étude, le dossier de raccordement, le suivi de la prime.

**Garde-fous**
- Aucun chiffre en euros du type « ce que vous perdez en attendant » ni « ce que les premiers
  ont touché en plus », et aucun gain ou économie d'un autre client (slides retirées par Ary le
  14/10/2026). Seuls chiffres autorisés : le barème public, et ceux du client dans le tableau.
- Ne pas annoncer le niveau du prochain barème : il n'est pas connu. Dire seulement qu'il est
  révisé chaque trimestre. Pour dire que les aides baissent, citer le chiffre exact du fichier
  (variation depuis le pic) plutôt qu'un superlatif.
- Compter les jours restants à la date de rédaction. Si l'échéance est proche (moins de trois
  semaines : seuil proposé, à ajuster par Ary), un dossier complet est peu probable : écrire
  « viser le trimestre suivant » plutôt que promettre un dépôt à temps. Un dossier complet
  dépend aussi de pièces du client : le dépôt avant la date est « à confirmer ».
- Aligner la validité de l'offre (annexe CGV) sur la fin du trimestre tarifaire en cours.
- Pas de logos CRE ni EDF sur ces slides sauf demande d'Ary ; si ajoutés, écrire « Source » et
  « ces logos n'impliquent aucun partenariat », et rappeler que l'usage des marques est à valider.
- Ton professionnel et factuel : l'urgence vient des chiffres officiels, pas des adjectifs.

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
(slides détail) plutôt que tout sur un seul ton. Slide 9 : fond nuit ; slide 10 : fond papier
avec la date en accent or.

## Ce qui a déjà existé comme erreur à ne pas refaire

- Ne pas dupliquer un même logo en inline ET en position absolue sur la même slide (nettoyer
  l'ancien placement avant d'ajouter le badge standard).
- Ne pas inventer un mécanisme de financement non confirmé (ex. délai de versement d'une aide) :
  le signaler explicitement comme "à confirmer avant signature" plutôt que de l'affirmer.
- Toujours revérifier le contenu d'une slide avant de la modifier si l'utilisateur a pu l'éditer
  à la main entre-temps (voir le `edits` counter dans l'`artifact-view-context` fourni par le
  client — un nombre qui augmente signifie qu'il faut relire avant d'écraser).
- Ne pas chiffrer en euros « ce que l'attente coûte » ni reprendre le gain d'un autre client
  sur les slides 9 et 10 (retiré par Ary le 14/10/2026) ; ne pas annoncer le prochain barème.
