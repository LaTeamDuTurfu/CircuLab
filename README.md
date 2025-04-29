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

## 🎮 Contrôles importants (Touches Clavier)

| Touche                      | Fonction                                                                       |
| :-------------------------- | :----------------------------------------------------------------------------- |
| **Flèches directionnelles** | Se déplacer sur la carte (scroll horizontal et vertical)                       |
| **Shift (⇧)**               | Accélérer le défilement de la carte                                            |
| **R**                       | Tourner l'orientation de la construction **dans le sens antihoraire**          |
| **Q**                       | Tourner l'orientation de la construction **dans le sens horaire**              |
| **P**                       | Activer/Désactiver l'aperçu de la construction ("Build Preview")               |
| **B**                       | Activer/Désactiver le mode **debug** pour voir des informations sur les tuiles |
| **+ / =**                   | **Zoom avant** sur la carte                                                    |
| **-**                       | **Zoom arrière** sur la carte                                                  |
| **A**                       | Déconnecter le graphe de circulation ("unbind graph")                          |
| **H**                       | Revenir en mode éditeur après une simulation terminée                          |

---

## 🖱️ Contrôles Souris

- **Clique gauche** : Placer ou retirer une tuile selon le mode actif.
- **Boutons GUI** : Sélectionner le type de route, la signalisation ou changer de mode (Édition, Signalisation, Simulation).

---

## 🛠️ Installation

1. Assurez-vous d'avoir **Python 3.10+** installé.
2. Installez les dépendances :

```bash
pip install pygame pygame_gui
```

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
