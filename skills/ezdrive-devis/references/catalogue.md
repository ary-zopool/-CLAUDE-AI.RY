# Catalogue et garde-fous — estimation EZdrive

*Relevé sur les devis EZD-DEV002985, 002986, 002987, 002995 et 002998, septembre 2026.
Source de vérité : Zoho Books, organisation EZ (`20087134268`), branche EZDRIVE, SKU `EZD_MQ_`.*

**Ces prix sont aussi codés en dur dans `scripts/generer_devis.py`. Toute modification doit être faite aux deux endroits, et la date ci-dessus mise à jour.**

## Socle, présent sur tout devis

| Article | HT | TVA |
|---|---|---|
| Borne non connectée AC 7,4 kW | 950,00 € | 0 % |
| Borne connectée et pilotée AC 7,4 kW | 1 085,00 € | 0 % |
| Disjoncteur bipolaire 40A courbe C, Pdc 10 kA | 60,00 € | 8,5 % |
| Bloc différentiel bipolaire 40A type A-SI 30 mA | 146,00 € | 8,5 % |

## Forfaits selon le linéaire

| Linéaire | Câble 3G10 | Tube IRL | Main d'œuvre | Base HT | TTC |
|---|---|---|---|---|---|
| Jusqu'à 6 ml | 108,00 € | 36,00 € | 200,00 € | 1 500,00 € | 1 546,75 € |
| 6 à 12 ml | 216,00 € | 78,00 € | 250,00 € | 1 700,00 € | 1 763,75 € |
| 12 à 20 ml | 360,00 € | 134,00 € | 250,00 € | 1 900,00 € | 1 980,75 € |
| 20 à 30 ml | 444,00 € | 150,00 € | 250,00 € | 2 000,00 € | 2 089,25 € |

Au-delà de 30 ml : devis sur mesure. **La grille ne s'extrapole jamais.** Le script refuse.

## Travaux complémentaires

| `id` | Article | HT | Unité | TVA |
|---|---|---|---|---|
| `tranchee` | Tranchée béton | 140,00 € | ml | **2,1 %** |
| `goulotte` | Goulotte électrique | 13,00 € | ml | 8,5 % |
| `cable3g16` | Câble 3G16 hors forfait | 19,90 € | ml | 8,5 % |
| `consuel` | Consuel IRVE | 182,00 € | — | 8,5 % |

## Non catalogués

Poteau, massif béton, **coffret de protection AC**, création de point de livraison EDF, reprise de tableau.

Le coffret figurait à 368,40 € sur le devis EZD-DEV002998. **Ce prix est faux** et l'article a été retiré du catalogue en attendant le bon tarif.
**Ne proposez aucun montant.** Demandez le prix au commercial et passez-le en `lignes_libres`. Le script bloque toute ligne libre sans montant.

## Les trois régimes de TVA

Borne **0 %** · Tranchée **2,1 %** · Tout le reste **8,5 %**.

**Guyane (973) : TVA non applicable** (article 294 du CGI). Toutes les lignes passent à 0 % et le document porte la mention « TVA non applicable, article 294 du CGI ». La grille HT reste celle de Martinique, à confirmer pour la Guyane.

La base imposable est le total HT **moins** la valeur de la borne. Les anciens devis affichent souvent un « montant total imposable » égal au HT complet : c'est faux, même si la TVA elle-même est juste.

## Les sept contrôles

Le script les exécute et les affiche. Un échec bloque la production.

1. **Forfait / linéaire** — le palier doit correspondre au linéaire saisi.
2. **Recomposition du HT** — somme des lignes = total annoncé, au centime.
3. **Base imposable et TVA** — une TVA nulle avec des lignes non-borne est une erreur.
4. **Fourchette** — hors de 1 500 à 2 200 € TTC, justification ligne par ligne exigée.
5. **Prix unitaires** — tous issus du catalogue ci-dessus.
6. **Référence à jour** — l'un des quatre paliers, jamais un libellé ancien.
7. **Mentions** — prix évolutif, décennale, TGBT, PDL, rétractation 14 jours, médiation.

## Erreurs relevées en production, à ne pas reproduire

| Devis | Problème |
|---|---|
| EZD-DEV002738 | Référencé « 6–12 ml », facturé 1 546,75 €, soit le tarif du palier inférieur. |
| EZD-DEV002819 | Total 1 500,00 € sans aucune TVA, accepté par la cliente. |
| EZD-DEV002987 | Disjoncteur à 65 € au lieu de 60 €, goulotte sans TVA. |
| EZD-DEV002998 | Coffret de protection AC à 368,40 €, prix erroné. Article retiré du catalogue. |
| EZD-DEV002949 | Nom d'affaire « 6–12 ml », référence « 12–20 ml ». |
| EZD-DEV002759 | Référence « 25 ml », palier qui n'existe pas. |
| — | Un devis « 6–12 ml » à 4 772,46 €. |

## Conflits connus, à signaler sans les trancher

**Deux grilles tarifaires.** Le manuel client annonce 1 550 / 1 750 / 1 950 € TTC, le catalogue donne 1 546,75 / 1 763,75 / 1 980,75 €. Appliquez le catalogue, signalez l'écart si le client cite le manuel.

**Deux codes TVA à 8,5 % dans Zoho** : « Taux normal » et « Taux normal TVA ». Sans incidence sur le montant, à signaler si un devis les mélange.

**Compteur ou tableau.** Le manuel demande de mesurer depuis le compteur et de photographier le tableau. Chez beaucoup de clients ce sont deux endroits distincts. En cas de doute, demandez lequel a servi de point de départ.

## Paiement

Plafond Alma : **2 000 € TTC**. Au-delà, le script masque le paiement en 4 fois et bascule sur acompte et solde à 50 %. Alma SAS est agréée par l'ACPR comme établissement de paiement et société de financement sous le **n° 17408**.

Alma impose contractuellement des mentions dans les CGV du marchand. Elles ne sont pas encore intégrées : à récupérer auprès d'Alma.

## Garantie

36 mois de garantie constructeur Autel, prolongés de 24 mois par EZdrive, soit 5 ans pièces et main d'œuvre. La prolongation est à la charge d'EZdrive.

## Nature du document

Le skill produit une **estimation**, pas un devis. Le prix est garanti jusqu'au montant affiché ; s'il est dépassé après la visite technique, le client accepte ou annule et se voit rembourser intégralement sous quatorze jours.

Le tunnel est intégralement à distance : aucun commercial ne se déplace avant signature. L'interdiction de percevoir un paiement avant sept jours, posée par l'article L221-10 du code de la consommation pour les contrats hors établissement, ne s'applique donc pas. **Si un commercial venait à se déplacer au domicile avant la signature, cette analyse tomberait** et l'acompte deviendrait illégal, sous peine de deux ans d'emprisonnement et 150 000 € d'amende (L242-7).

Le délai de rétractation et de remboursement est de **quatorze jours**, jamais trente. Le formulaire type de rétractation est produit en page 4 de chaque estimation.

## Médiateur de la consommation

CM2C — Centre de la Médiation de la Consommation de Conciliateurs de Justice, 14 rue Saint-Jean, 75017 Paris, www.cm2c.net, cm2c@cm2c.net. Coordonnées codées dans `scripts/generer_devis.py` (constante `MEDIATEUR`). **EZdrive doit avoir signé la convention d'adhésion avec le CM2C** : sans convention, la mention est fausse.
