INSERT IGNORE INTO {target_table} (
	symbol
	,`date`
	,timezone
	,`close`
	,ma_7
	,ma_10
	,ma_20
	,ma_50
	,ma_100
	,ma_200
	,golden_cross
	,death_cross
	)
SELECT symbol
	,`date`
	,timezone
	,`close`
	,ma_7
	,ma_10
	,ma_20
	,ma_50
	,ma_100
	,ma_200
	,CASE
		WHEN ma_50 > ma_200
			THEN 1
		ELSE 0
		END AS golden_cross
	,CASE
		WHEN ma_50 < ma_200
			THEN 1
		ELSE 0
		END AS death_cross
FROM (
	SELECT symbol
		,`date`
		,timezone
		,`close`
		,AVG(`close`) OVER (
			PARTITION BY symbol ORDER BY `date` ROWS BETWEEN 6 PRECEDING
					AND CURRENT ROW
			) AS ma_7
		,AVG(`close`) OVER (
			PARTITION BY symbol ORDER BY `date` Rows BETWEEN 9 PRECEDING
					AND CURRENT ROW
			) AS ma_10
		,AVG(`close`) OVER (
			PARTITION BY symbol ORDER BY `date` Rows BETWEEN 19 PRECEDING
					AND CURRENT row
			) AS ma_20
		,AVG(`close`) OVER (
			PARTITION BY symbol ORDER BY `date` Rows BETWEEN 49 PRECEDING
					AND CURRENT row
			) AS ma_50
		,AVG(`close`) OVER (
			PARTITION BY symbol ORDER BY `date` Rows BETWEEN 99 PRECEDING
					AND CURRENT row
			) AS ma_100
		,AVG(`close`) OVER (
			PARTITION BY symbol ORDER BY `date` Rows BETWEEN 199 PRECEDING
					AND CURRENT row
			) AS ma_200
	FROM {source_table}
	) AS mov_avg