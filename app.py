import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.ensemble import IsolationForest

# Configuration de la page Streamlit
st.set_page_config(page_title="Smart Utility Monitor", layout="wide")

st.title("💧⚡ Smart-Utility-Monitor : Détection d'Anomalies")
st.markdown("Outil d'analyse pour repérer automatiquement les fuites, fraudes ou erreurs de compteurs dans le secteur public.")

# 1. Génération de fausses données de consommation (pour le test)
np.random.seed(42)
dates = pd.date_range(start="2023-01-01", periods=100)

# Consommation normale autour de 50m3, avec quelques légères variations
consumption = np.random.normal(loc=50, scale=5, size=100)

# Injection d'anomalies manuelles (Ce que le modèle doit trouver !)
consumption[20] = 120  # Grosse fuite ou fraude
consumption[75] = 15   # Compteur bloqué ou défectueux
consumption[85] = 110  # Autre fuite

# Création du DataFrame
df = pd.DataFrame({'Date': dates, 'Consommation (m3)': consumption})

# 2. Modèle de Machine Learning : Isolation Forest
# L'Isolation Forest est parfait pour isoler les valeurs aberrantes (outliers)
model = IsolationForest(contamination=0.05, random_state=42) # On suppose 5% d'anomalies
df['Prédiction'] = model.fit_predict(df[['Consommation (m3)']])

# Transformation des prédictions (-1 = Anomalie, 1 = Normal)
df['Statut'] = df['Prédiction'].map({1: 'Normal', -1: 'Anomalie'})

# 3. Visualisation avec Plotly
st.subheader("📊 Analyse des relevés de compteurs")

fig = px.scatter(
    df, 
    x='Date', 
    y='Consommation (m3)', 
    color='Statut',
    color_discrete_map={'Normal': '#1f77b4', 'Anomalie': '#d62728'},
    title="Détection des comportements anormaux via IA (Isolation Forest)",
    size=df['Statut'].map({'Normal': 1, 'Anomalie': 3}) # Rendre les points d'anomalies plus gros
)

# Ajouter une ligne pour relier les points et voir la tendance
fig.add_traces(px.line(df, x='Date', y='Consommation (m3)').data[0])
fig.update_traces(line=dict(color='gray', width=1), selector=dict(type='scatter', mode='lines'))

st.plotly_chart(fig, use_container_width=True)

# 4. Affichage des données critiques
st.subheader("🚨 Alertes détectées")
anomalies_df = df[df['Statut'] == 'Anomalie'].drop(columns=['Prédiction'])

if not anomalies_df.empty:
    st.error(f"{len(anomalies_df)} anomalies détectées nécessitant une intervention technique !")
    st.dataframe(anomalies_df, use_container_width=True)
else:
    st.success("Aucune anomalie détectée sur cette période.")