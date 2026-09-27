---
name: ezdrive-devis
description: Établit une estimation client EZdrive pour l'installation d'une borne de recharge à domicile en Martinique, Guadeloupe, Guyane ou La Réunion, et la produit en PDF de quatre pages avec le prix garanti, le paiement Alma en 4 fois, les mentions légales et les contrôles de cohérence. Utilise ce skill dès qu'il est question de chiffrer, établir, corriger ou vérifier un devis, une estimation, un forfait Kit Standard, un linéaire de câble, une tranchée, ou dès qu'apparaît une référence EZD-DEV ou EZD-EST, même si l'utilisateur ne demande pas explicitement un « devis ». Utilise-le aussi pour vérifier qu'un chiffrage existant est juste.
---

# Estimation EZdrive

Chiffre une installation de borne à domicile et produit le PDF client.

**Le document produit est une *estimation*, jamais un devis.** En droit français un devis est une offre ferme ; ici le prix est arrêté après la visite du technicien. Le mot « devis » ne doit apparaître nulle part dans le document, et le skill ne le produit pas.

Le modèle repose sur un engagement : **prix garanti jusqu'au montant affiché**. Si la visite technique révèle un dépassement, le client accepte ou annule, et dans ce cas il est intégralement remboursé sous quatorze jours. Cet engagement est présenté en évidence en page 1, pas en petits caractères : c'est lui qui rend l'acompte acceptable.

**Le calcul ne se fait jamais de tête.** Le script `scripts/generer_devis.py` fait l'arithmétique, applique sept contrôles et refuse de produire un document si l'un échoue. C'est le seul chemin autorisé.

## Avant de chiffrer

Cinq informations sont nécessaires. S'il en manque une, demande-la et arrête-toi là.

1. **Le linéaire en mètres.** Un chiffre précis. « Environ 10 mètres » ne suffit pas : demande de trancher, le palier change à 6, 12, 20 et 30 ml.
2. **Le nom et l'adresse du client, code postal compris.** Le code postal fixe le territoire et donc la TVA : sans lui, le script refuse. En Guyane (973), la TVA n'est pas applicable (art. 294 du CGI) : le script passe toutes les lignes à 0 %.
3. **Le type de borne** : non connectée, ou connectée et pilotée.
4. **Les travaux complémentaires** et leurs quantités : tranchée, coffret, goulotte, câble 3G16, Consuel.
5. **Le type de pose** : contre un mur, ou sur poteau. Le poteau n'est pas catalogué — voir plus bas.

## Produire le devis

Écris un fichier JSON puis lance le script :

```bash
python3 scripts/generer_devis.py devis.json -o devis.pdf
```

```json
{
  "numero": "EZD-EST003001",
  "date": "2026-09-15",
  "client": {"nom": "Marlène ESCURE", "adresse": "12 rue des Flamboyants",
             "cp": "97200", "ville": "Fort-de-France"},
  "conseiller": {"nom": "Florence Lampla", "tel": "0696 24 95 38"},
  "lineaire_m": 6,
  "borne": "non_connectee",
  "options": [{"id": "goulotte", "qte": 10}],
  "remise_borne": 0,
  "remise_cable": 0,
  "lignes_libres": []
}
```

`borne` vaut `non_connectee` ou `connectee_pilotee`. Les `id` d'options sont `tranchee`, `goulotte`, `cable3g16`, `consuel` — pour les articles au mètre, `qte` est le linéaire.

Le script choisit le forfait d'après `lineaire_m`, calcule la TVA selon les trois régimes, décide si le paiement Alma en 4 fois est proposé, et rend un PDF de quatre pages : l'offre, la garantie de prix et la signature ; le détail chiffré ; les conditions, avec le médiateur de la consommation ; le formulaire type de rétractation.

## Après avoir lancé le script

Reprends **le rapport de contrôles tel quel** dans ta réponse, avant le lien vers le PDF. C'est ce qui permet au commercial de vérifier sans rouvrir le document. Signale ensuite les points à faire confirmer avant envoi.

Si un contrôle échoue, le script ne produit rien. N'essaie pas de contourner : corrige l'entrée ou remonte le problème.

## Ce que tu ne fais jamais

- **Inventer ou estimer un prix absent du catalogue.** Poteau, massif béton, coffret de protection AC, création de PDL EDF, reprise de tableau : demande le montant au commercial et passe-le en `lignes_libres`. Le coffret a été retiré du catalogue, son prix de 368,40 € relevé sur d'anciens devis étant erroné.
- **Extrapoler la grille au-delà de 30 ml.** C'est un devis sur mesure.
- **Accepter un prix total imposé et reconstituer les lignes à rebours.** C'est le mécanisme qui produit les devis faux : chaque ligne paraît plausible, seul le sens du calcul est inversé. Refuse et explique pourquoi.
- **Arrondir un total** pour faire plus propre.
- **Traiter une case cochée comme une signature électronique.** La signature passe par Zoho Sign.
- **Employer le mot « devis »** dans le document produit ou dans ta réponse au client.
- **Modifier un devis déjà signé.** Toute modification impose une nouvelle signature.
- **Passer sous silence un contrôle en échec** pour rendre service.

## Vérifier un chiffrage existant

Reconstruis l'entrée JSON à partir du document, lance le script, et compare les totaux. Les écarts relevés en production et leurs causes sont listés dans `references/catalogue.md`.

## Pour aller plus loin

- `references/catalogue.md` — prix, régimes de TVA, sept contrôles, erreurs connues, conflits en suspens. **Lis-le avant tout chiffrage qui sort du cas standard**, et systématiquement si l'utilisateur conteste un prix.
- `assets/` — feuille de style, logo EZdrive, tracé du logo Alma. Utilisés par le script, pas à modifier à la main.

## Dépendances

Python 3, `playwright` avec Chromium installé. Le rendu PDF échoue sans lui.
