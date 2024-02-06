## Projet de Détection de Chats et de Chiens

### Technologies et Outils Utilisés

- **Deep Learning**:
  - **TensorFlow**: Utilisé pour construire et entraîner le modèle de détection.
  - **Keras**: Interface haut niveau pour construire des réseaux de neurones de manière rapide et efficace.
- **Modèles Pré-entraînés**:
  - **MobileNetV2**: Utilisé comme modèle de base pour l'extraction de features.
- **Librairies Python**:
  - **Matplotlib**: Utilisé pour la visualisation des images et des résultats.
  - **Numpy**: Pour la manipulation des données.
- **Environnement de Développement**:
  - **Google Colab**: Plateforme cloud utilisée pour l'exécution du code.

### Projet Contenu

1. **Collecte des Données**:
   - Les données sont constituées d'images de chats et de chiens.

2. **Prétraitement des Données**:
   - Les images sont redimensionnées à une taille de 224x224 pixels.
   - Les pixels des images sont normalisés entre 0 et 1.

3. **Augmentation des Données**:
   - Rotation, zoom, retournement horizontal, décalage horizontal, décalage vertical, cisaillement, et variation de luminosité sont appliqués pour augmenter la variabilité des données.

4. **Construction du Modèle**:
   - Un modèle séquentiel est construit en utilisant MobileNetV2 comme base avec des couches supplémentaires de classification.
   - Les poids du modèle pré-entraîné sont gelés.
   - Le modèle est compilé avec l'optimiseur Adam et la perte de cross-entropy catégorique.

5. **Entraînement du Modèle**:
   - Le modèle est entraîné sur les données d'entraînement avec une validation sur les données de validation.
   - Le nombre d'époques est fixé à 20 avec un batch size de 128.

6. **Évaluation du Modèle**:
   - L'exactitude et la perte sont évaluées sur les données de test.
   - Des visualisations sont fournies pour analyser les performances du modèle.

7. **Résultats**:
   - Le modèle obtient une précision de 63% sur les données de test.
   - Les images de test sont classées comme chat ou chien avec leurs probabilités respectives.

### Avantages

- Utilisation d'un modèle pré-entraîné pour le transfert learning, ce qui permet de réduire le temps d'entraînement et d'obtenir de meilleures performances avec moins de données.
- Augmentation des données pour améliorer la généralisation du modèle et éviter le surajustement.
- Utilisation de Google Colab pour un accès facile à des ressources de calcul GPU, accélérant ainsi le processus d'entraînement.
