# MEMOIRE_SURAYA.md — Projet Suraya

> Fichier à relire en début de chaque conversation du projet Suraya.
> Les décisions majeures prises ici sont reportées en 1 ligne dans le MEMOIRE.md du projet COO AI.Ry.
> Tout élément marqué *[à confirmer]* n'est pas validé par Ary : ne pas l'utiliser comme un fait.

---

## 1. Instructions du projet (à coller dans les instructions du projet Claude "Suraya")

Tu es le copilote d'Ary, COO de Suraya, holding d'EZdrive et EZsolar. Dans ce projet, tu travailles uniquement sur Suraya et ses filiales : catalogue, sous-produits, prix, vente, communication, logistique, coûts/finance, RH, admin.
Règles : tu prépares, Ary décide. Aucun envoi, aucune publication, aucun paiement sans accord explicite. Tu n'inventes aucun chiffre : si tu n'es pas sûr, tu le dis et tu cherches. Réponses courtes et structurées ; une décision attendue = une question claire à la fin. Lis MEMOIRE_SURAYA.md au début de chaque conversation et donne à la fin les lignes exactes à y ajouter.

---

## 2. Entités

```
SURAYA (holding — Ary = COO)
├── EZdrive (ezdrive.fr) — bornes de recharge à domicile
│     Territoires : Martinique, Guadeloupe, Guyane, La Réunion [à confirmer]
└── EZsolar (ezsolar.fr) — photovoltaïque
      Territoires : [à compléter]

Hors SURAYA à ce jour :
ECO CARIB (Sainte-Lucie, ecocarib.com) — EPC solaire + exploitation-maintenance
      Détenue majoritairement par la société de Frantz (ARJUN, 55 % selon l'organigramme) ;
      passage sous SURAYA envisagé [à confirmer]. Associé local : Denell Florius.
```

## 3. Objectifs

- Suraya : ≥ 10 000 €/mois (objectif général 12 mois)
- Répartition EZdrive / EZsolar : [à compléter]
- Objectifs par produit / par mois : [à compléter]

## 4. Catalogue produits

### EZdrive
| Produit / sous-produit | Cible | Prix | Statut |
|---|---|---|---|
| Kit Standard (forfait installation borne à domicile) [à confirmer] | [ ] | [ ] | [ ] |
| Options (linéaire de câble, tranchée…) [à confirmer] | [ ] | [ ] | [ ] |
| Paiement Alma en 4 fois [à confirmer] | — | — | [ ] |
| [à compléter] | | | |

### EZsolar
| Produit / sous-produit | Cible | Prix | Statut |
|---|---|---|---|
| Centrale PV en autoconsommation + vente du surplus [à confirmer] | [ ] | [ ] | [ ] |
| Variante avec batterie [à confirmer] | [ ] | [ ] | [ ] |
| Primes mobilisables (CRE / EDF SEI) [à confirmer] | — | — | [ ] |
| [à compléter] | | | |

## 5. Grille détail (remplie un produit à la fois)

Vente/Commercial · Communication · Logistique · Coût/Finance · RH · Admin

---

## 6. Journal des décisions

- **[2026-09-27]** Création du projet Suraya, séparé du copilote général COO AI.Ry.
- **[2026-11-03]** Agent « trello-leads-meta » (skill dans le dépôt, commits 32c3afb et 98fd0b3) : lancé à la demande avec les CSV du Leads Center, il ajoute les leads manquants au tableau LEADS BtC EZD - EZS, archive les doublons non protégés (10 au maximum), pose les étiquettes territoire et produit, qualifie particulier ou entreprise et met à jour le Claude Doc « Leads Meta · tableau récapitulatif ». À faire : importer le zip dans claude.ai ; ajouter une question produit au formulaire Meta.
- **[2026-11-09]** KoM « Reborn ECO CARIB 2027-2030 » (Frantz, Denell Florius, Ary) : Ary applique le programme Reborn (vente et marketing numérique) à ECO CARIB. Visite d'Ary à Sainte-Lucie décidée pour la semaine du 16 novembre. Détail en section 8.

---

## 7. Boîte à idées

- Proposer la recharge (EZdrive) à ECO CARIB : l'entreprise ne fait pas de bornes aujourd'hui.
- Réutiliser à Sainte-Lucie la méthode de suivi des leads d'EZdrive (actions engageantes, affaires endormies, Trello) plutôt qu'un CRM sur mesure.

---

## 8. ECO CARIB — programme Reborn 2027-2030

Source : notes et transcription Gemini du KoM du 9 nov. 2026 (Drive : « KoM - Reborn ECO CARIB 2027 - 2030 - Notes par Gemini »). Transcription automatique : noms et chiffres à vérifier.

**L'entreprise**
- Créée en 2019 par Frantz et Denell Florius (rencontrés en 2017-2018). Entreprise de transition énergétique à Sainte-Lucie : EPC solaire et exploitation-maintenance. Pas de recharge de véhicules à ce jour.
- La société de Frantz y est majoritaire ; Frantz soutient Denell à distance.
- Nom à normaliser : « ECO CARIB » (titre du KoM, domaine ecocarib.com), « Zaina Eco Caribbe » (notes Gemini), « ECOCARAIBE » (organigramme juridique).

**Denell Florius**
- Développement commercial et développement de projets renouvelables, du résidentiel au grand solaire.
- Assistance technique pour un fonds de développement caribéen (audits énergétiques, accès à des garanties de risque pour les banques) ; forme des banques aux produits renouvelables ; contribue aux politiques publiques. Nom exact du fonds à vérifier (transcrit « carcom development fund »).
- Formation : Sir Arthur Lewis Community College [à confirmer], ingénierie électrique appliquée, MBA récent.

**Les offres**
1. Solaire photovoltaïque avec batterie pour le résidentiel haut de gamme.
2. Exploitation, maintenance et suivi de centrales commerciales existantes (projets d'environ 100 kW) : revenu mensuel récurrent, ajouté l'an dernier.
3. Audits énergétiques de qualité investissement : grandes entreprises (hôtels, hôpitaux) et PME via le fonds institutionnel.

**Le modèle de vente** : audit énergétique → centrale solaire (EPC) → ajout d'une batterie (onduleur hybride).

**Acquisition et outils**
- Leads : Google, articles et formulaire sur le site (référencement), page d'atterrissage avec calculateur qui pré-qualifie le client (chaud, froid, non éligible), bouche-à-oreille. Adresse de la page à vérifier (transcrite « appt.com »).
- Problème identifié par Denell : la génération de leads fonctionne, le suivi et la relance des leads ne fonctionnent pas. Ancien CRM abandonné ; souhait d'un CRM sur mesure relié à leurs outils.
- Gestion de projets : Monday. Trello utilisé ponctuellement pour le reporting avec Frantz.

**Rôle d'Ary** : présenté par Frantz comme dirigeant externe, pressenti pour devenir directeur général du groupe ; mission Reborn : professionnaliser la vente et le marketing numérique de toutes les offres.

**Décisions et prochaines étapes**
- Visite d'Ary à Sainte-Lucie : jeudi 19 et vendredi 20 novembre 2026 avec Denell, séjour jusqu'au 22. (Les notes Gemini écrivent « septembre » : erreur, la réunion parle de la semaine suivante.)
- [Ary] Envoyer un e-mail récapitulatif : informations demandées et dates de visite. Informations à demander : produits par cible, histoire des deux derniers clients (comment ils sont entrés dans le pipe), délai entre premier contact et signature, connaissance du marché local.
- [Denell] Organiser des rendez-vous avec des entrepreneurs, des apporteurs d'affaires et des prospects pour comprendre le marché.
