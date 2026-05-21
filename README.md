# 💧⚡ Smart-Utility-Monitor : Détection d'Anomalies pour les Ressources Publiques

## 📌 Aperçu du Projet

La gestion des secteurs vitaux tels que la distribution d'eau et d'énergie nécessite des outils fiables pour prévenir les pertes et optimiser la facturation. **Smart-Utility-Monitor** est une application analytique conçue pour identifier automatiquement les comportements de consommation anormaux (fuites, fraudes, erreurs de capteurs) à partir de jeux de données massifs.

Ce projet démontre comment la data science peut s'intégrer dans des solutions de gestion globales pour le secteur public et industriel.

## 🚀 Fonctionnalités Clés

*   **Analyse de Consommation :** Nettoyage et exploration des données de compteurs via Pandas.

*   **Détection d'Anomalies :** Implémentation d'algorithmes statistiques (Z-score / Isolation Forest) pour isoler les pics ou chutes de consommation aberrants.

*   **Visualisation Interactive :** Tableau de bord généré avec Streamlit permettant aux gestionnaires de visualiser les alertes en temps réel.

## 🛠️ Stack Technique

*   **Data Science :** Python, Pandas, Numpy, Scikit-learn
*   **Data Visualization :** Plotly, Streamlit
*   **Versionnement :** Git & GitHub

## ⚙️ Déploiement Local

```bash
git clone [https://github.com/ton-username/Smart-Utility-Monitor.git](https://github.com/ton-username/Smart-Utility-Monitor.git)
pip install -r requirements.txt
streamlit run app.py