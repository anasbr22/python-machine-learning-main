# Classification de Tumeur du Sein

Ce programme utilise Tkinter pour créer une interface graphique permettant de prédire la nature bénigne ou maligne d'une tumeur du sein en utilisant un modèle SVM pré-entrainé. Le programme charge un scaler et un modèle SVM à partir de fichiers, et permet à l'utilisateur de saisir des valeurs de caractéristiques pour effectuer une prédiction.

## Prérequis
- Python 3.x
- Bibliothèques Python : `tkinter`, `pandas`, `matplotlib`, `Pillow`, `joblib`

## Fichiers du modèle
- `model/scaler.pkl` (Scaler pré-entrainé)
- `model/svm_model.pkl` (Modèle SVM pré-entrainé)

## Images de l'application
- `screen/`


## Installation
1. Assurez-vous que Python et les bibliothèques nécessaires sont installés.
2. Exécutez le script Python .

## Utilisation

### Lancement du programme
Exécutez le script Python "interface.py" pour ouvrir l'interface graphique.

### Saisie des valeurs de caractéristiques
- Les champs de saisie sont créés dynamiquement pour chaque caractéristique requise par le modèle.
- Vous pouvez remplir manuellement ces champs ou cliquer sur le bouton **Exemple** pour charger un exemple de données.



## Description des Fonctionnalités

### Charger un Exemple
- Remplit les champs de saisie avec un jeu de données d'exemple.

### Réinitialiser les Champs
- Vide tous les champs de saisie et la zone d'affichage des résultats.

### Valider les Entrées
- Vérifie la validité des valeurs saisies (doivent être numériques).
- Effectue la mise à l'échelle des données d'entrée.
- Effectue une prédiction en utilisant le modèle SVM.
- Affiche le résultat de la prédiction (Malignant ou Benign).

### Afficher les Informations du Modèle
- Affiche des informations détaillées sur le modèle SVM, telles que les classes, les vecteurs de support, le nombre de vecteurs de support, l'interception et les paramètres.
