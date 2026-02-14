CREATE MATERIALIZED VIEW stock_features_mv AS

WITH base AS (

  SELECT
    ts, 
	close_price, 
	high_price, 
	low_price, 
	volume,

    -- Rendements logarithmiques (returns)
    LN(close_price / LAG(close_price, 1) OVER (ORDER BY ts))  AS logret_1m,
    LN(close_price / LAG(close_price, 5) OVER (ORDER BY ts))  AS logret_5m,
    LN(close_price / LAG(close_price, 15) OVER (ORDER BY ts)) AS logret_15m,
    LN(close_price / LAG(close_price, 60) OVER (ORDER BY ts)) AS logret_60m,

    -- Volume logarithmiques
    LN(NULLIF(volume,0)) AS log_volume
  FROM stock_prices
),




ichimoku AS (
  SELECT
    *,
	-- Tenkan-sen (9 périodes) court terme
    (MAX(high_price) OVER (ORDER BY ts ROWS BETWEEN 8 PRECEDING AND CURRENT ROW) +
     MIN(low_price)  OVER (ORDER BY ts ROWS BETWEEN 8 PRECEDING AND CURRENT ROW)) / 2 AS tenkan,
	 
	-- Kijun-sen (26 périodes) moyen terme
    (MAX(high_price) OVER (ORDER BY ts ROWS BETWEEN 25 PRECEDING AND CURRENT ROW) +
     MIN(low_price)  OVER (ORDER BY ts ROWS BETWEEN 25 PRECEDING AND CURRENT ROW)) / 2 AS kijun,

	-- Senkou Span B (52 périodes) long terme sans décalage (voir docimentation)
    (MAX(high_price) OVER (ORDER BY ts ROWS BETWEEN 51 PRECEDING AND CURRENT ROW) +
     MIN(low_price)  OVER (ORDER BY ts ROWS BETWEEN 51 PRECEDING AND CURRENT ROW)) / 2 AS span_b_mod

	 -- Span_a calculer à part pour amméliorer la lisibilité et la maintenabilité
	 
  FROM base
),



feat AS (

  SELECT
    *,
	-- Senkou Span A
    (tenkan + kijun) / 2 AS span_a_mod,

    -- vol_60m régime court terme (sensibilité aux chocs immédiats)
    STDDEV_SAMP(logret_1m) OVER (ORDER BY ts ROWS BETWEEN 59 PRECEDING AND CURRENT ROW) AS vol_60m,

	-- vol_1d  régime long terme (1 jour = 1440 minute)
    STDDEV_SAMP(logret_1m) OVER (ORDER BY ts ROWS BETWEEN 1439 PRECEDING AND CURRENT ROW) AS vol_1d,

    -- Moyenne mobile du volume sur 60 minutes 
    AVG(volume) OVER (ORDER BY ts ROWS BETWEEN 59 PRECEDING AND CURRENT ROW) AS vol_ma_60m
  FROM ichimoku
)



SELECT
  ts,
  close_price,
  
  -- Rendements log multi horizons
  logret_1m, 
  logret_5m, 
  logret_15m, 
  logret_60m,

  -- Lags des rendements
  LAG(logret_1m, 1)  OVER (ORDER BY ts) AS lag_logret_1m_1,
  LAG(logret_1m, 5)  OVER (ORDER BY ts) AS lag_logret_1m_5,
  LAG(logret_1m, 15) OVER (ORDER BY ts) AS lag_logret_1m_15,
  LAG(logret_1m, 60) OVER (ORDER BY ts) AS lag_logret_1m_60,

  -- Risque (régime de marché)
  vol_60m,
  vol_1d,

  -- Activité et liquidité
  volume,
  log_volume,
  vol_ma_60m,

  -- Structure de marché 
  tenkan,
  kijun,
  span_a_mod,
  span_b_mod,

  -- Distance normalisé
  (close_price - tenkan) / close_price AS tenkan_dist,
  (close_price - kijun) / close_price AS kijun_dist,

  -- Epaisseur du nuage, incertitude structurelle
  ABS(span_a_mod - span_b_mod) / close_price AS cloud_large,

  -- Signal structurel Tenkan > Kijun 
  CASE WHEN tenkan > kijun THEN 1 ELSE 0 END AS tenkan_sup_kijun,

  -- Régime de tendance prix au dessus de la borne supérieure du nuage
  CASE WHEN close_price > GREATEST(span_a_mod, span_b_mod) THEN 1 ELSE 0 END AS price_sup_cloud,

  -- Persistance du régime (filtre faux signal)
  LAG(CASE WHEN close_price > GREATEST(span_a_mod, span_b_mod) THEN 1 ELSE 0 END, 5) OVER (ORDER BY ts) AS lag_price_sup_cloud_5,

  -- Target y 
  LEAD(logret_1m, 5) OVER (ORDER BY ts) AS y_logret_5m
FROM feat;

 -- Indexation

CREATE INDEX ON stock_prices(ts);
CREATE INDEX ON stock_features_mv(ts);