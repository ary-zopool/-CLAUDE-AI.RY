# Mémoire projet — Suraya
Dernière mise à jour : 24 septembre 2026

Ce document résume tout ce qui a été discuté, construit et décidé sur le projet de reporting commercial et de pilotage d'équipe chez Suraya. Il sert de point de reprise pour une future conversation : à coller en début d'échange ou à faire lire avant de repartir sur ce sujet.

---

## 1. Contexte de l'entreprise

Suraya opère deux marques dans les DROM :
- **EZdrive** : bornes de recharge électrique (BtoC et BtoB)
- **EZsolar** : photovoltaïque résidentiel (BtoC)

Zones concernées : Martinique, Guadeloupe, Guyane, La Réunion — la plupart des chantiers documentés ici se concentrent sur la **Martinique**.

Personnes identifiées dans les échanges : **Ary Augustin** (porteur du projet, décideur), **Anthony Malartre** (technique/produit), **Florence** (commerciale terrain B2B/B2C), **Frantz** (commercial, tension récurrente avec Florence sur l'attribution des leads), **Loïs** (développeur), **Nogret** (ressource RH pressentie pour le test photovoltaïque), **Benjamin** (étude PV).

Problème structurel identifié tôt : le **plan de rentrée n'est pas chiffré** (mention "à chiffrer" sur les 7 leviers), et le seul document chiffré disponible est un tableau *EZD – SALES Q4 2026* (objectifs Martinique : 45 000 €/mois de CA B2B nouveau, 2 copropriétés Logivolt/mois, 2 baux ou acquisitions bornes publiques/mois, 2×9 kWc PV/mois). **Ce tableau contredit le plan de rentrée sur la Martinique** (le plan dit que Logivolt s'arrête en Martinique, le tableau en redemande) — contradiction non résolue à ce jour.

---

## 2. Les deux grands chantiers du projet

### Chantier A — Agent IA "Manager Suraya" (COO IA)
Objectif : un agent qui aide à **cadrer** les objectifs (trimestre/mois/semaine), les **diffuse** aux équipes, **collecte** le reporting hebdomadaire, **relance**, **escalade**, et produit des **synthèses** pour COMEX/managers/partners.

### Chantier B — Outils de reporting commercial (préalable concret, avant l'agent)
Une série d'outils testables tout de suite, sans attendre l'agent : formulaires de saisie, kanban de portefeuille, dashboard consolidé — pensés pour être repris/étendus par l'agent plus tard plutôt que jetés.

---

## 3. Cahier des charges de l'agent Manager Suraya — décisions actées

| Sujet | Décision |
|---|---|
| Statut | **Informationnel**, jamais de fondement RH ou contractuel |
| Périmètre V1 | Commercial, Martinique, EZdrive |
| Populations | Commerciaux salariés — **prestataires exclus du dispositif de relance/warning** (risque de requalification en lien de subordination, non tranché juridiquement) |
| Cascade objectifs | Trimestre → Mois → Semaine |
| Axes suivis | CA signé, baux d'exploitation signés, activité commerciale (RDV, devis) |
| Source de vérité objectifs | Outil tiers (ClickUp/Notion envisagé), l'agent lit et écrit |
| Rôle de cadrage | L'agent **questionne**, ne fixe jamais les chiffres lui-même |
| Validation objectifs | **COMEX** pour trimestre/mois, **manager** pour l'hebdo (sinon le COMEX est submergé) |
| Révision d'objectif | Autorisée, historique tracé (jamais modifié en place) |
| Données réalisées | **100 % déclaratif**, pas de CRM (refus explicite de Zoho) |
| Canaux | Email + WhatsApp + webapp de consultation |
| Rythme hebdo | Demande **vendredi 9h**, deadline **vendredi 15h**, heure locale (Réunion décalée de 8h/Antilles) |
| Relances | 2 max, puis warning au manager, puis escalade à Ary si silence 2 semaines |
| Ton | Factuel, sec, jamais de classement individuel |
| Synthèses | Ary + COMEX, PDF, bimensuel, toujours relu avant envoi |
| Transparence | **Au niveau équipe**, jamais de comparaison nominative entre commerciaux |
| Budget cible | 50–150 €/mois |
| Socle technique | Vercel + Postgres UE + WhatsApp Cloud API + API Claude (~60–90 €/mois estimé) |
| RGPD | Information préalable des salariés obligatoire, statut du DPO **non clarifié** |

**Trois arbitrages tranchés en cours de route** :
1. Transparence totale vs interdiction de classer → transparence au niveau équipe seulement, détail individuel restreint.
2. Objectifs manquants → un **projet d'objectifs chiffrés** a été rédigé par extrapolation du tableau SALES avec hypothèses explicites (panier moyen 12 000 €, taux de conversion 25/60/30 %), accompagné de **6 questions bloquantes** à poser au COMEX avant toute diffusion.
3. Prestataires dans le dispositif → exclus du warning/escalade en V1.

**WhatsApp — contrainte technique actée** : tout envoi hors fenêtre de 24h doit être un template pré-approuvé par Meta (catégorie utilitaire) ; 5 templates identifiés (`diffusion_objectifs`, `demande_reporting`, `relance_reporting_1`, `relance_reporting_2`, `alerte_manager`) ; vérification du compte Meta Business à lancer en tout premier car hors du contrôle du planning interne.

---

## 4. Le modèle de reporting commercial — évolution du raisonnement

Point de départ : Florence donne un compte rendu oral libre, riche mais inexploitable tel quel (mélange affaires/blocages/RH dans une même liste).

**Étape 1 — Segmentation en 4 blocs** : mouvements de pipeline / affaires sans mouvement / blocages / points managériaux. Pipeline en 7 étapes (0 à qualifier → 4 signé, + Perdu/Gelé).

**Étape 2 — Recadrage du but** : l'utilisateur précise que l'objectif n'est pas "avoir des chiffres à tout prix" mais **savoir si le commercial prospecte et relance vraiment les affaires qui dorment**. → déplacement de la mesure : on ne mesure pas la personne, on mesure le **portefeuille**.

**Étape 3 — Le mécanisme central retenu** : **inversion de l'entretien**. Le commercial ne choisit plus de quoi il parle ; l'outil lui présente d'abord les affaires endormies (triées de la plus vieille à la moins vieille), et exige sur chacune soit une action réalisée, soit une suite datée, soit "perdu". *"Je vais relancer"* n'est pas une réponse valide.

**Étape 4 — Vocabulaire final : "actions réalisées", pas "mouvements"** :

| Action | Engageante ? |
|---|---|
| Appel abouti | Oui |
| Rendez-vous tenu | Oui |
| Visite technique | Oui |
| Devis envoyé | Oui |
| Relance de devis (avec réponse client) | Oui |
| Signature obtenue | Oui |
| Message envoyé (sans réponse) | **Non** |
| Appel non abouti | **Non** |

**Règle d'or, validée explicitement** : *seule une action engageante réveille une affaire et remet son compteur de dormance à zéro.* Une relance par message qui ne récolte aucune réponse ne compte pas — c'est le garde-fou contre la relance de façade.

**Seuils** (à valider avec le manager, pas figés) :
- **Dormance** : 21 jours sans action engageante
- **Gel automatique** : 3 semaines consécutives sans décision (action ou suite datée) → l'affaire sort seule du portefeuille actif, sans validation humaine requise

**Sur le côté "déclaratif" du système** : l'utilisateur a validé que c'est acceptable ("pas grave si c'est du déclaratif"). Garde-fou retenu : **rien d'agrégé, tout de nommé** — un chiffre sans nom de compte associé n'est pas recevable, ce qui rend un mensonge visible via le compteur de dormance plutôt que par vérification a priori.

---

## 5. Les quatre segments du reporting (dernière itération, la plus aboutie)

Logique validée : **BtoC = volume = chiffres seuls** ; **BtoB = relationnel = fiche par compte nommé**.

| Segment | Logique | Indicateurs |
|---|---|---|
| BtoC Bornes | Chiffres seuls | Nouveaux leads contactés, leads relancés, devis envoyés, devis signés |
| BtoC Photovoltaïque | Chiffres + suivi chantier | Les 4 mêmes + état des chantiers (en attente / en cours / terminé) |
| BtoB Bornes privées (flottes, parkings) | Fiche par compte | Les 4 compteurs agrégés + par compte : nom, projet, actions réalisées horodatées |
| BtoB Bornes publiques (collectivités) | Fiche par compte | Idem + champ optionnel "prochaine échéance institutionnelle" (AG, conseil) |

**Règle transversale ajoutée à cette étape** : les compteurs BtoC ne sont **jamais saisis directement** — ils se déduisent du comptage des actions horodatées, exactement comme en BtoB. Un seul modèle de données pour les 4 segments, seule la restitution diffère. Référentiel de statuts commun : `Nouveau → Contacté → Relancé → RDV pris → Devis envoyé → Signé` (+ `Perdu`/`Gelé`).

---

## 6. Outils concrètement livrés

| Fichier / outil | Ce qu'il fait | Stockage |
|---|---|---|
| `reporting-hebdo/index.html` + `admin.html` + `dashboard.html` | Première version : formulaire à 6 champs numériques (prospects, nouveaux, devis, WIN, CA, LOST), backoffice de gestion des commerciaux, dashboard consolidé | Google Sheets + Apps Script |
| `actions-hebdo/` (`Code.gs`, `config.js`, `index.html`, `recap.html`) | **Version aboutie** : parcours du portefeuille par actions réalisées, dormeurs en premier, gel automatique à 3 semaines, montant obligatoire uniquement sur signature | Google Sheets + Apps Script — **c'est le socle technique à réutiliser pour tout développement futur** |
| `demo-actions-hebdo.html` | Démo testable en conversation avec données pré-chargées (portefeuille Florence + Frantz) | localStorage (démo uniquement) |
| `kanban-florence.html` (publié en artifact) | Kanban simple par compte, 5 colonnes, notes libres, bouton "copier pour envoyer" ; mis à jour de façon incrémentale semaine après semaine via un système de migrations qui préserve les modifications déjà faites | **localStorage uniquement — pas de stockage partagé**, à ne pas utiliser comme base d'un dashboard consolidé |
| `Reporting-B2C-S1.pptx` | Deck de reporting ventes B2C pour réunion, basé sur un classeur Excel fourni ; a révélé des incohérences de comptage des pertes (1 vs 9 vs 8 dans le même onglet) et 12 devis promis jamais envoyés | — |
| `Roadmap-commerciale-T4.pptx` | Deck 8 slides pour dirigeants ingénieurs/financiers : principe R&D-avant-forecast, formule ROI (1€ investi → X€ générés), matrice de maturité des 3 axes (BtoC Bornes / BtoC PV / BtoB Bornes PME) sur sept-déc | — |
| `reporting-commercial-suraya/SKILL.md` | Skill réutilisable qui documente toute la logique ci-dessus (4 segments, référentiel commun, socle technique Sheets+Apps Script, séquence de travail recommandée) pour que toute future session reprenne l'existant au lieu de repartir de zéro | — |

**Documents d'analyse produits** (non-outils, mais contiennent des décisions) : `Reporting-S37-...md`, `Reporting-S38-...md` (analyse de la note Gemini du call hebdo, révèle que Frantz reprend des leads de Florence pour la 3e semaine consécutive — sujet managérial non résolu), `Protocole-entretien-hebdomadaire-agent.md`, `Revision-mesurer-activite-plutot-que-chiffres.md`.

---

## 7. Ce qui reste ouvert

- **Aucun prix ni ROI réel validé.** Le panier moyen (12 000 € en hypothèse), les taux de conversion, et l'exemple de ROI du deck roadmap sont tous pédagogiques ou extrapolés — jamais des chiffres confirmés par le COMEX.
- **La contradiction Logivolt Martinique** (tableau SALES vs plan de rentrée) bloque la diffusion de l'objectif copropriétés.
- **Statut juridique des prestataires** dans le dispositif de reporting — non tranché, avis d'un juriste recommandé.
- **Attribution des leads Frantz/Florence** — remonté deux fois comme point managérial, jamais arbitré.
- **Volumétrie réelle par segment BtoB** (nombre de comptes actifs) — nécessaire avant de dimensionner l'outil final, jamais demandée à l'utilisateur.
- **Choix ClickUp vs Notion** comme source de vérité des objectifs — non tranché, avec la recommandation de vérifier si ClickUp Goals couvre déjà une partie du besoin.
- **Aucun envoi automatique du reporting** n'existe encore (ni WhatsApp ni email) — c'est le rôle prévu de l'agent Manager Suraya, pas encore construit.
- **DPO / registre de traitement RGPD** — statut non confirmé.

---

## 8. Point de vocabulaire à normaliser

"Frantz" (compte rendu oral S37) et "Franz" (note Gemini S38) désignent la même personne — à harmoniser avant toute création de fiche dans un outil.
