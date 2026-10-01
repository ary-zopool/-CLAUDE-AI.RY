# Scan to Pay — application EZDRIVE (API Greenflux)

> Résumé d'un ancien projet, importé le 30/09/2026. Statut : Brouillon (CDC FIDECOIN non rédigé).

## Fiche

| Champ | Contenu |
|---|---|
| Entité | EZdrive (Suraya) |
| Prestataire technique | FIDECOIN (retenu) |
| Produit | Scan to Pay sur l'application EZDRIVE, via l'API Greenflux |
| Référence existante | Scan to Pay V-CITY via l'API ROAD / e-Flux |
| Cible | Usager sans compte ni application : scanne un QR sur la borne, paie par CB |
| Chiffres validés | Aucun |

## Ce qui a été construit

- Instructions pour Mathis (alternant SI/Exploitation) : .docx puis PDF compilé — contexte, schéma de flux, wireframes basse fidélité des 5 écrans clés, sources Drive, structure de CDC pour FIDECOIN.
- Wireframes publiés en canvas éditable.
- Note conservée dans le projet Claude d'origine.
- Skill « cdc-schema-first » créé (schéma + question wireframes avant tout CDC).

## Décisions

- FIDECOIN est le prestataire retenu.
- Mission de Mathis en deux volets : 1) comprendre l'existant ROAD / V-CITY ; 2) étudier la faisabilité Greenflux.
- Structure du futur CDC calquée sur le CDC LOT3 CPMS V-CITY existant.

## Ouvert

| # | Point | Bloque |
|---|---|---|
| 1 | Session anonyme disponible côté API Greenflux ? | Tout le projet (faisabilité) |
| 2 | Accès au dépôt GitHub EZDATA13/FORKEZD2.5road (non obtenu) | Volet 1 de Mathis |
| 3 | Prestataire de paiement CB | Montant pré-autorisé, écrans de paiement |
| 4 | QR statique ou dynamique | Dépend de 1 et 3 |
| 5 | Grille tarifaire spot + montant pré-autorisé | Rentabilité, affichage borne |

## Emplacement des livrables

- Instructions Mathis (PDF), wireframes, sources : Google Drive — [chemin à compléter]
