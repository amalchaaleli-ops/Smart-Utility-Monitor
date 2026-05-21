import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.ensemble import IsolationForest

# Configuration de la page
st.set_page_config(page_title="Monitor AI", layout="wide", initial_sidebar_state="expanded")

# --- BARRE LATÉRALE (Contexte local) ---
with st.sidebar:
    st.header("⚙️ Paramètres Réseau")
    secteur = st.selectbox("Sélectionner la zone de supervision :", 
                           ["Secteur Ariana - Nord", "Secteur Tunis - FST", "Zone Industrielle"])
    sensibilite = st.slider("Sensibilité du modèle de détection", 0.01, 0.10, 0.05)
    st.markdown("---")
    st.markdown("*Outil d'intelligence artificielle destiné à la supervision des réseaux publics.*")

# --- TITRE PRINCIPAL ---
st.title(f"💧 Détection d'Anomalies - {secteur}")

# --- GÉNÉRATION DE DONNÉES RÉALISTES ET "SALES" ---
np.random.seed(42)
dates = pd.date_range(start="2023-01-01", periods=150)

# Simuler une tendance avec des variations (week-ends plus bas)
base_consumption = 50 + np.sin(np.linspace(0, 10, 150)) * 10
noise = np.random.normal(loc=0, scale=3, size=150)
consumption = base_consumption + noise

# 1. Injecter des valeurs aberrantes (fuites / fraudes)
consumption[25] = 130
consumption[80] = 15
consumption[140] = 115

# 2. Injecter des pannes de capteurs (Valeurs manquantes / NaN)
consumption[45:48] = np.nan 

df = pd.DataFrame({'Date': dates, 'Consommation': consumption})

# Nettoyage des données (interpolation pour combler les pannes de capteurs)
df['Consommation_Clean'] = df['Consommation'].interpolate()

# --- MODÉLISATION MATHÉMATIQUE ---
model = IsolationForest(contamination=sensibilite, random_state=42)
df['Prédiction'] = model.fit_predict(df[['Consommation_Clean']])
df['Statut'] = df['Prédiction'].map({1: 'Normal', -1: 'Anomalie'})

# --- MISE EN PAGE AVEC ONGLETS ---
tab1, tab2 = st.tabs(["📊 Dashboard Opérationnel", "🧠 Analyse Mathématique"])

with tab1:
    col1, col2, col3 = st.columns(3)
    col1.metric("Relevés totaux", len(df))
    col2.metric("Pannes Capteurs (NaN)", df['Consommation'].isna().sum())
    col3.metric("Anomalies Détectées", len(df[df['Statut'] == 'Anomalie']))

    # Graphique principal
    fig = px.scatter(
        df, x='Date', y='Consommation_Clean', color='Statut',
        color_discrete_map={'Normal': '#1f77b4', 'Anomalie': '#d62728'},
        size=df['Statut'].map({'Normal': 1, 'Anomalie': 3}),
        title="Supervision du flux avec interpolation des données manquantes"
    )
    fig.add_traces(px.line(df, x='Date', y='Consommation_Clean').data[0])
    fig.update_traces(line=dict(color='lightgray', width=1), selector=dict(mode='lines'))
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Justification du Modèle (Isolation Forest)")
    st.write("Contrairement à une simple analyse d'écart-type, l'algorithme *Isolation Forest* permet de traiter des distributions non normales et d'isoler les anomalies en partitionnant aléatoirement les données de consommation.")
    
    # Afficher la distribution
    fig_dist = px.histogram(df, x="Consommation_Clean", nbins=40, title="Distribution Statistique de la Consommation")
    st.plotly_chart(fig_dist, use_container_width=True)