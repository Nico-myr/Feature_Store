import streamlit as st
from pathlib import Path

st.title("Contrôle qualité des données")
st.markdown(
"""
Les contrôles de qualité appliqués aux données se limitent aux vérifications structurelles :
types de variables, doublons et valeurs manquantes.

Aucun contrôle d’outliers n’est réalisé à ce stade.  
Dans le contexte des séries temporelles financières (Bitcoin), les valeurs extrêmes
font partie intégrante du signal de marché et doivent être conservées pour garantir
la cohérence des données utilisées pour l’entraînement, le backtesting et l’inférence
des modèles de machine learning.
"""
)


sql_path = Path("qualite_donnees.sql")
query = sql_path.read_text(encoding="utf-8")

st.code(query, language="sql")