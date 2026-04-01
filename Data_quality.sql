-- Copie pour travail
CREATE TABLE stock_prices_work AS
SELECT *
FROM stock_prices;

-- Controle des types 
SELECT
    column_name,
    data_type
FROM information_schema.columns
WHERE table_name = 'stock_prices_work';

-- Controle valeurs manquantes
SELECT ts, open_price, high_price,
	   low_price, close_price, volume
FROM stock_prices_work
WHERE ts IS NULL OR
	open_price IS NULL OR
	high_price IS NULL OR
	low_price IS NULL OR
	close_price IS NULL OR
	volume IS NULL ;
	
-- Controle valeurs en doubles
SELECT ts
FROM stock_prices_work
GROUP BY ts
HAVING COUNT(*) > 1;

-- Symbole 
SELECT DISTINCT symbol 
FROM stock_prices_work;


-- Début et fin de la période

SELECT min(ts) as "début de la période", 
	   max(ts) as "fin de la période"
FROM stock_prices_work;
 

-- Nombre d'observations
SELECT COUNT(ts)
FROM stock_prices_work;

-- Aggrégation par mois pour afficher la distribution avec Graph visualiser

SELECT
    date_trunc('month', ts) AS month,
    ROUND (AVG(open_price),2)  AS avg_open,
    ROUND (AVG(high_price),2)  AS avg_high,
    ROUND(AVG(low_price),2)   AS avg_low,
    ROUND (AVG(close_price),2) AS avg_close,
    ROUND (AVG(volume) ,2)     AS avg_volume
FROM stock_prices
GROUP BY date_trunc('month', ts)
ORDER BY month;

-- Aggrégation par années pour afficher la distribution avec Graph visualiser
SELECT
    date_trunc('year', ts) AS year,
    ROUND (AVG(open_price),2)  AS avg_open,
	ROUND (AVG(volume) ,2) AS avg_volume
FROM stock_prices
GROUP BY date_trunc('year', ts)
ORDER BY year;




