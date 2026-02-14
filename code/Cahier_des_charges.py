import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Feature Store",
    layout="wide",
)


st.title("FEATURE STORE")
st.subheader(
"Objectif du projet"
)

st.markdown(
"""
Créer un feature store structuré et reproductible dédié au Bitcoin (BTC),
afin de standardiser la génération de variables pour l’entraînement,
l’évaluation et le backtesting de modèles de machine learning et de deep learning
appliqués aux séries temporelles crypto-financières.
"""
)


sections = [
    "Besoins métier",
    "Contraintes métiers",
    "Contraintes techniques",
    "Sources de données",
    "Liste des features",
    "Sources",
]
choice = st.sidebar.radio("Sommaire", sections)



if choice == "Besoins métier":
    st.subheader("Principaux mécanismes du Bitcoin à capturer")
    st.markdown(
        """
Le feature store doit permettre de capturer :

- Les **dynamiques de prix** via des **rendements logarithmiques multi horizons** (momentum, accélérations, retournements)
- Le **risque & l'incertitude** avec des **volatilités glissantes**
- L'**intensité de l’activité** avec le **volume échangé** (proxy de liquidité / d'engagement)
- **Structure de tendance** avec les différents indicateurs **Ichimoku** (équilibre, congestion, régimes directionnels)
"""
    )

elif choice == "Contraintes métiers":
    st.subheader("Contraintes métiers")
    st.markdown(
        """
- Marché des crypto-monnaies **continu (24/7, sans clôture)**
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
        st.markdown("### Performance & architecture")
        st.markdown(
        """
    - Table de features **matérialisée** pour éviter les recomputations
    - Indexation temporelle pour accès rapide
    - Pipeline compatible batch + entraînement ML
    - Reproductibilité des features
    - Versionnage des transformations
    """
    )   

    with col2:
        st.markdown("### Prévention du data leakage")
        st.markdown(
        """
    - Utilisation systématique de **lags**
    - Fenêtres temporelles strictement passées
    - Aucune utilisation d’information future
    - Compatibilité avec backtesting réaliste
    - Alignement strict features/target
    """
    )

elif choice == "Sources de données":
    st.subheader("Data Sources & Storage")

    st.markdown(
    """
    ### Source primaire
    Les données de marché proviennent d’une base PostgreSQL centralisée servant de data warehouse.

    **Database**
    - PostgreSQL
    - Schéma : `market_data`
    - Table : `btc_ohlcv`
    - Granularité : 1 minute
    - Actif : BTC/USDT

    **Structure**
    - timestamp (PK)
    - open
    - high
    - low
    - close
    - volume

    ### Feature Store
    Les features sont matérialisées dans une table dédiée :

    - Schéma : `feature_store`
    - Table : `btc_feature_store`
    - Index : timestamp
    - Usage : ML training / backtesting / inference

    ### Pipeline
    API → ingestion → PostgreSQL → feature engineering → feature store
    """
    )


elif choice == "Liste des features":
    st.subheader("Liste des features")

    features = [
    {
        "Famille": "Returns",
        "Features": "logret_1m / 5m / 15m / 60m",
        "Rôle": "Capturer les dynamiques de prix à différentes échelles temporelles pour les modèles ML et DL."
    },
    {
        "Famille": "Return lags",
        "Features": "lag_logret_n",
        "Rôle": "Introduire de la mémoire temporelle dans les modèles tabulaires et stabiliser l’apprentissage."
    },
    {
        "Famille": "Volatility",
        "Features": "vol_60m, vol_1d",
        "Rôle": "Permettre aux modèles d’adapter leurs prédictions au régime de volatilité du marché."
    },
    {
        "Famille": "Volume",
        "Features": "volume, log_volume, vol_ma",
        "Rôle": "Mesurer l’intensité du marché et filtrer les mouvements peu liquides."
    },
    {
        "Famille": "Ichimoku",
        "Features": "tenkan, kijun, span_a, span_b",
        "Rôle": "Capturer la structure de tendance et les zones d’équilibre du marché."
    },
    {
        "Famille": "Derived",
        "Features": "tenkan_dist, kijun_dist, cloud_width",
        "Rôle": "Normaliser l’information de tendance pour améliorer la généralisation des modèles."
    },
    {
        "Famille": "Signals",
        "Features": "tenkan_cross, price_vs_cloud",
        "Rôle": "Fournir des signaux de régime explicites pour faciliter l’apprentissage non linéaire."
    },
    {
        "Famille": "Target",
        "Features": "future_logret",
        "Rôle": "Variable cible alignée temporellement pour l’entraînement supervisé."
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

