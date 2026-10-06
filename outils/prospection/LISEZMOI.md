# Robot de prospection LinkedIn — mode d'emploi (Windows)

Campagne active : **EZdrive D3 — bornes de recharge B2B**. Profil utilisé : celui d'Ary.

> Rappel : automatiser LinkedIn est contraire à l'article 8.2 de ses conditions d'utilisation. Votre profil peut être restreint. Décision prise en connaissance de cause le 06/10/2026.

## Ce que fait le robot, chaque jour ouvré

1. Il vérifie qui a accepté votre invitation et envoie le **message 1** aux nouveaux contacts.
2. Il envoie la **relance 1** (J+4) et la **relance 2** (J+10) aux personnes qui n'ont pas répondu.
3. Dès qu'un prospect répond, sa séquence s'arrête et il passe au statut `repondu`. C'est à vous de prendre la suite.
4. Il envoie au maximum **15 invitations, sans note**, aux prospects marqués `a_inviter`.
5. Si LinkedIn affiche une vérification ou un avertissement, **il s'arrête tout de suite** et vous prévient.

Il ne fait jamais de recherche sur LinkedIn : il ne traite que les profils que **vous** ajoutez dans `prospects.xlsx`.

## Installation (une seule fois, environ 20 minutes)

1. **Python** : téléchargez Python 3.12 sur https://www.python.org/downloads/windows/. Pendant l'installation, cochez **« Add python.exe to PATH »**.
2. **Copiez le dossier** `outils/prospection` du repo sur votre ordinateur, par exemple dans `C:\Prospection`.
3. Ouvrez le dossier, cliquez dans la barre d'adresse, tapez `cmd`, puis Entrée. Une fenêtre noire s'ouvre dans le bon dossier.
4. Tapez ces deux lignes, l'une après l'autre :
   ```
   pip install playwright openpyxl pyyaml
   python -m playwright install chromium
   ```
5. **Vérification** :
   ```
   python prospection.py --verifier
   ```
   Le fichier `prospects.xlsx` est alors créé.
6. **Connexion à LinkedIn** :
   ```
   python prospection.py --connexion
   ```
   Une fenêtre s'ouvre : connectez-vous normalement, puis revenez dans la fenêtre noire et appuyez sur Entrée. La connexion reste enregistrée dans le dossier `profil_navigateur`. Ne partagez jamais ce dossier, il contient votre session.

## Premier lancement : toujours en essai

1. Ajoutez 2 ou 3 prospects dans `prospects.xlsx` (onglet « Prospects », colonnes en jaune), avec le statut `a_inviter`. Supprimez la ligne d'exemple. **Fermez le fichier.**
2. Lancez :
   ```
   python prospection.py --essai --forcer
   ```
   Le robot fait tout le parcours, mais **n'envoie rien**. Regardez la fenêtre et le fichier `journal.log`.
3. Si tout se passe bien, lancez en réel :
   ```
   python prospection.py --forcer
   ```

## Lancement automatique chaque matin

1. Ouvrez le **Planificateur de tâches** (tapez « Planificateur » dans le menu Démarrer).
2. Cliquez sur **Créer une tâche de base**, nommez-la « Prospection LinkedIn », choisissez **Tous les jours** à **9:00**.
3. Pour l'action **Démarrer un programme** :
   - Programme : `python`
   - Arguments : `prospection.py`
   - Commencer dans : `C:\Prospection`
4. L'ordinateur doit être allumé et la session Windows ouverte. Le robot décale lui-même son départ au hasard (jusqu'à 40 min) et ne fait rien le week-end.

## Votre routine (5 minutes par jour)

- **Ajouter** des prospects : URL du profil, prénom, entreprise, poste, territoire, secteur, avec le statut `a_inviter`.
- **Traiter** les lignes au statut `repondu` : c'est là que se trouvent vos rendez-vous.
- **Regarder** la colonne `derniere_erreur`.
- **Fermer** `prospects.xlsx` avant 9 h.

Ces trois chiffres vont dans votre reporting : nouveaux contacts (`repondu`), devis envoyés, devis signés.

## Si le robot s'arrête

| Message | Que faire |
|---|---|
| « ROBOT ARRÊTÉ — LinkedIn demande une vérification » | Ne relancez pas. Ouvrez LinkedIn vous-même, répondez à la vérification, et attendez **48 h**. |
| « fermez-le dans Excel » | Fermez `prospects.xlsx` et relancez. |
| « Modèles refusés (charte V3) » | Un mot interdit ou un tutoiement se trouve dans `modeles.yaml`. Corrigez-le. |
| « bouton … introuvable », souvent et pour tout le monde | LinkedIn a changé son interface. Demandez à Claude de corriger le bloc `SELECTEURS` en haut de `prospection.py`, en lui donnant le `journal.log`. |
| Statut `erreur`, « variable vide » | Il manque une info (prénom, entreprise ou territoire) sur la ligne. Complétez-la, puis remettez `a_inviter`. |

## Fichiers

| Fichier | Rôle | Vous le modifiez ? |
|---|---|---|
| `config.yaml` | Quotas, horaires, exclusions, alertes e-mail | Oui, au besoin |
| `modeles.yaml` | Les messages | Oui (la charte est vérifiée automatiquement) |
| `prospects.xlsx` | Vos prospects | Oui, chaque jour |
| `prospection.py` | Le moteur | Non |
| `journal.log`, `profil_navigateur/` | Créés par le robot, **à ne pas mettre sur GitHub** | Non |
