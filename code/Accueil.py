# app.py
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Feature Store",
    layout="wide",
)

# ---- Header
st.title("FEATURE STORE")
st.caption(
    """Objectif : Créer un feature store structuré et reproductible dédié au cours du Bitcoin (BTC),
afin de faciliter l’entraînement et l’évaluation de modèles de machine learning et de deep learning
appliqués à des séries temporelles crypto-financières."""
)

# ---- Sidebar navigation
sections = [
    "Besoins métier",
    "Contraintes métiers",
    "Contraintes techniques",
    "Liste des features",
    "Sources",
]
choice = st.sidebar.radio("Sommaire", sections)



if choice == "Besoins métier":
    st.subheader("Principaux mécanismes du Bitcoin à capturer")
    st.markdown(
        """
Le feature store doit permettre de capturer :

- Les **dynamiques du prix** via des **rendements logarithmiques multi horizons** (momentum, accélérations, retournements)
- Le **risque & l'incertitude** avec des **volatilités glissantes**
- L'**intensité de l’activité** avec le **volume échangé** (proxy de liquidité / engagement)
- **Structure de tendance** avec les différents indicateurs **Ichimoku** (équilibre, congestion, régimes directionnels)
"""
    )

elif choice == "Contraintes métiers":
    st.subheader("Contraintes métiers")
    st.markdown(
        """
- Marché Bitcoin **continu (24/7, sans clôture)**
- Fenêtres glissantes basées **uniquement sur l’ordre temporel**
- **Forte volatilité** et **changements rapides de régime**
- Utilisation de **rendements logarithmiques** et **volatilité glissante multi-horizons**
- **Liquidité variable** et hétérogène
- **Log(volume)** et **moyenne mobile** pour lisser l’activité
"""
    )

elif choice == "Contraintes techniques":
    st.subheader("Contraintes techniques")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Performance")
        st.markdown(
            """
- Utilisation d’une **table matérialisée** pour éviter de recalculer les features
- Accès rapide par **timestamp**
- Création d’**index** sur les tables pour accélérer calculs et requêtes temporelles
"""
        )

    with col2:
        st.markdown("### Anti leakage")
        st.markdown(
            """
- Utilisation de **LAG()**
- Fenêtres SQL de type **PRECEDING AND CURRENT ROW**
- Objectif : pipeline compatible ML + backtesting **sans fuite d’information**
"""
        )

elif choice == "Liste des features":
    st.subheader("Liste des features")

    features = [
        {
            "Famille": "Returns",
            "Features": "logret_1m / 5m / 15m / 60m",
            "Rôle": "permettre aux modèles ML de capter des patterns de momentum et aux modèles DL "
            "comme le LSTM ou TCN d’apprendre des dynamiques temporelles cohérentes à différentes échelles",
            
        },
        {
            "Famille": "Return lags",
            "Features": "lag_logret_1m_n",
            "Rôle": "injecter de la mémoire dans les modèles tabulaires (XGBoost, Random Forest),"
            " et facilitent l’apprentissage de dépendances temporelles courtes sans surcharger la profondeur des réseaux DL",
            
        },
        {
            "Famille": "Volatilité",
            "Features": "vol_60m, vol_1d",
            "Rôle": "permettre aux modèles de conditionner leurs prédictions au régime de marché (calme vs stress),"
              "et d'améliorant la robustesse et réduisant les faux signaux en périodes de forte volatilité"
        },
        {
            "Famille": "Volume",
            "Features": "volume, log_volume, vol_ma_60m",
            "Rôle": "suivre la liquidité et l’activité en "
            "aidant les modèles à distinguer les mouvements significatifs des variations peu liquides ou bruitées.",
            
        },
        {
            "Famille": "Ichimoku lines",
            "Features": "tenkan, kijun, span_a_mod, span_b_mod",
            "Rôle": "apporter des informations sur la structure du marché"
            "aidant les modèles à apprendre des niveaux d’équilibre et des zones de support et de résistance."
            "Pas de décalage de la span_a et span_b pour éviter toute ambiguïté temporelle et empêcher toute fuite d’information",
            
        },
        {
            "Famille": "Derived features",
            "Features": "tenkan_dist, kijun_dist, cloud_large",
            "Rôle": "améliorer la généralisation des modèles grâce à des variables normalisées et notamment pour la multi-périodes.",
            
        },
        {
            "Famille": "Signals",
            "Features": "tenkan_sup_kijun, price_sup_cloud (+ lags)",
            "Rôle": "fournir des signaux de régime explicites qui facilitent la séparation non linéaire pour les modèles ML et stabilisent"
            "l’apprentissage des réseaux DL en réduisant l’ambiguïté du contexte de marché.",
            
        },
        {
            "Famille": "Target",
            "Features": "y_logret_5m",
            "Rôle": "label supervisé pour définir un objectif clair et aligné temporellement, permettant d’entraîner des modèles prédictifs exploitables"
            " tout en évitant les fuites d’information (data leakage).",
        },
    ]

    df = pd.DataFrame(features, columns=["Famille", "Features", "Rôle"])
    st.table(df)
                     


elif choice == "Sources":
    st.subheader("Sources")
    st.markdown(
        """
- **Ichimoku Analyses & Stratégies** : Comment détecter la tendance des marchés pour les stocks, la cryptomonnaie et le Forex en combinant l’analyse technique et l’Ichimoku Cloud (seconde édition) — *Broché, 8 novembre 2022*, Charles G. Koonitz
"""
    )

