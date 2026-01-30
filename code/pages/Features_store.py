import streamlit as st
from pathlib import Path

st.title("Création du feature store")

sql_path = Path("table_feature.sql")
query = sql_path.read_text(encoding="utf-8")

st.code(query, language="sql")