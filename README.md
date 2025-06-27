# Gestion Bibliothèque Meriem

## Auteur  
Meriem SADDOUKI

---

## Description

Gestion Bibliothèque Meriem est une application desktop développée en Python avec Tkinter qui permet de gérer efficacement une bibliothèque.  
Ce projet intègre :  
- Un backend orienté objet (POO) pour la logique métier  
- La gestion des exceptions personnalisées pour les erreurs métier  
- La persistance des données dans des fichiers (texte, JSON, CSV)  
- La génération de rapports statistiques avec Matplotlib  
- Une interface graphique avec onglets pour gérer livres, membres, emprunts et statistiques  
- (Optionnel) Intégration d'un système de recommandation basé sur TensorFlow/Keras

---

## Objectifs du projet

- Implémenter un système complet de gestion des livres, membres et emprunts.  
- Gérer les erreurs métier avec des exceptions personnalisées.  
- Assurer la sauvegarde et le chargement des données à partir de fichiers.  
- Visualiser des statistiques utiles sur la bibliothèque (répartition des genres, activité d'emprunts...).  
- Proposer une interface utilisateur intuitive via Tkinter.  

---

## Fonctionnalités principales

- **Gestion des Livres** :  
  - Ajouter, afficher, supprimer des livres  
  - Informations des livres : ISBN, titre, auteur, année, genre, statut (disponible/emprunté)

- **Gestion des Membres** :  
  - Ajouter, afficher, supprimer des membres  
  - Chaque membre possède un ID, un nom et une liste des livres empruntés

- **Gestion des Emprunts/Retours** :  
  - Emprunter un livre (mise à jour du statut et des emprunts du membre)  
  - Retourner un livre  

- **Gestion des erreurs métier** :  
  - Exceptions personnalisées telles que LivreIndisponibleError, QuotaEmpruntDepasseError, MembreInexistantError, LivreInexistantError  
  - Gestion des erreurs avec messages clairs pour l’utilisateur  

- **Statistiques et Visualisations** :  
  - Diagrammes circulaires, histogrammes, courbes temporelles avec Matplotlib  
  - Exemples : répartition des livres par genre, top auteurs, activité des emprunts  

- **Persistance des données** :  
  - Sauvegarde/chargement dans des fichiers texte, JSON, CSV  
  - Fichiers utilisés :  
    - `livres.txt` (format : ISBN;titre;auteur;année;genre;statut)  
    - `membres.txt` (format : ID;nom;livres_empruntés)  
    - `historique.csv` (format : date;ISBN;ID_membre;action)

---

## Prérequis

- Python 3.x  
- Modules Python :  
  - tkinter (livré avec Python)  
  - matplotlib  
  - exceptions (module interne au projet)  
  - bibliotheque (module interne au projet)  
  - tensorflow/keras (optionnel, pour la recommandation)

---

## Installation

1. **Cloner le dépôt :**

```bash
git clone https://github.com/meriemsadd/Gestion-Bibliotheque-Meriem.git
cd Gestion-Bibliotheque-Meriem
