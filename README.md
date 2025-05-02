# CircuLab

**CircuLab** est un éditeur de réseaux routiers et simulateur de circulation développé avec **Python**, **Pygame** et **pygame_gui**.

Il permet aux utilisateurs de construire des routes, de placer de la signalisation et de simuler la circulation de véhicules sur un graphe généré dynamiquement.

---

## 🚀 Fonctionnalités principales

- **Créer une nouvelle partie** ou **charger une sauvegarde existante**.
- **Construire** un réseau de routes à l'aide d'une barre d'outils intuitive.
- **Placer de la signalisation** sur les routes.
- **Simuler** la circulation de véhicules sur le réseau créé.
- **Sauvegarder** automatiquement à la fermeture si activé.
- **Gestion dynamique** du zoom et du défilement de la carte.

---

## 🛠️ Installation

1. Assurez-vous d'avoir **Python 3.10+** installé.
2. Installez les dépendances :

```bash
pip install pygame_gui
pip install pygame
pip install networkx
pip install matplotlib
pip install dill
```

---

## 🎮 Comment jouer

### 📝 Créer une nouvelle sauvegarde

1. **Lancer l'application** :

   - Exécute `Circulab.py` pour ouvrir CircuLab.

2. **Créer une nouvelle partie** :

   - Sur l'écran d'accueil, cliquez sur **"Créer une nouvelle sauvegarde"**.

3. **Remplir les champs** :

   - **Nom de la sauvegarde** : Entrez un nom sans espaces ni caractères spéciaux (30 caractères maximum).
   - **Nombre de colonnes et de lignes** : Choisissez un nombre entre **50** et **300** pour chaque dimension.
   - **Chemin de la sauvegarde** : Cliquez sur le bouton `...` pour choisir un dossier où sera enregistrée votre carte.

4. **Valider la création** :
   - Cliquez sur **"Créer"** pour générer une nouvelle carte vide.
   - Si tout est correct, une nouvelle partie est automatiquement créée et ouverte.

---

### 📂 Charger une sauvegarde existante

1. **Depuis l'écran d'accueil** :

   - Cliquez sur **"Charger une sauvegarde"**.

2. **Sélection du fichier** :

   - Une fenêtre d'explorateur de fichiers s'ouvre automatiquement.
   - Par défaut, l'explorateur vous dirige vers le chemin initial :
     ```bash
     ../CircuLab/data/saves/
     ```
     _(C'est là que vos sauvegardes `.clab` sont stockées.)_

3. **Choisir une sauvegarde** :

   - Sélectionnez un fichier de sauvegarde avec l'extension `.clab`.
   - Cliquez sur **"OK"** pour valider.

4. **Jouer** :
   - Après un chargement réussi, vous êtes immédiatement replacé dans l'éditeur avec votre carte restaurée.

---

### 🚨 Remarques importantes

- **Validez toujours vos champs** lors de la création d'une sauvegarde : les colonnes et lignes doivent respecter les limites imposées.
- **La simulation** ne peut démarrer que si votre réseau est correctement connecté.
- **Deux routes minimum** sont requises pour une simulation fonctionnelle.

---

## 🎮 Contrôles importants (Touches Clavier)

| Touche                      | Fonction                                                              |
| :-------------------------- | :-------------------------------------------------------------------- |
| **Flèches directionnelles** | Se déplacer sur la carte (scroll horizontal et vertical)              |
| **Shift (⇧)**               | Accélérer le défilement de la carte                                   |
| **R**                       | Tourner l'orientation de la construction **dans le sens antihoraire** |
| **Q**                       | Tourner l'orientation de la construction **dans le sens horaire**     |
| **P**                       | Activer/Désactiver l'aperçu de la construction ("Build Preview")      |
| **+**                       | **Zoom avant** sur la carte                                           |
| **-**                       | **Zoom arrière** sur la carte                                         |
| **A**                       | Déconnecter le graphe de circulation ("unbind graph")                 |
| **H**                       | Revenir en mode éditeur après une simulation terminée                 |

---

## 🖱️ Contrôles Souris

- **Clique gauche** : Placer ou retirer une tuile selon le mode actif.
- **Boutons GUI** : Sélectionner le type de route, la signalisation ou changer de mode (Édition, Signalisation, Simulation).

---

## 📚 Comment fonctionne la simulation ?

- Le réseau est transformé en un **graphe orienté**.
- Les **intersections** sont représentées comme des **nœuds**.
- Les **routes** reliant les intersections sont représentées comme des **arêtes**.
- Lors du passage en mode **Simulation**, des **véhicules** sont créés aléatoirement sur le réseau.
- Chaque véhicule suit un chemin déterminé automatiquement à l'aide d'un **algorithme de parcours** (pathfinding simple).

---

## 🔥 Remarques spéciales

- Certaines fonctionnalités comme **l’aperçu** (`P`) ou le **mode debug** (`B`) sont très utiles pour construire des réseaux optimisés avant de lancer une simulation.
- **Deux routes minimum** sont nécessaires pour que la simulation démarre correctement.
- Le zoom et le défilement peuvent être utilisés pendant la simulation pour observer les déplacements en détail.

---

## 🧠 À propos

**CircuLab** est un projet éducatif visant à combiner :

- Les concepts de **graphe** et de **modélisation de réseaux**.
- Le développement d'une **interface utilisateur graphique** en **Pygame** et **pygame_gui**.
- Une **simulation dynamique** de circulation avec une approche simple d'**intelligence artificielle**.

Ce projet a été conçu pour apprendre, expérimenter et simuler de manière interactive les mécanismes de base d’un réseau routier.

---
