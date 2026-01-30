import streamlit as st
from pathlib import Path

st.title("Contrôle qualité des données")

sql_path = Path("qualite_donnees.sql")
query = sql_path.read_text(encoding="utf-8")

st.code(query, language="sql")