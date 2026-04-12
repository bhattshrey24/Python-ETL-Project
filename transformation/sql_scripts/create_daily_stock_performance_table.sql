INSERT IGNORE INTO {target_table} (
	symbol
	,`date`
	,timezone
	,`open`
	,high
	,low
	,`close`
	,volume
	,prev_open
	,prev_high
	,prev_low
	,prev_close
	,prev_volume
	,price_change
	,percentage_change
	,volume_change
	,gap_open_pct
    ,is_positive_day
	)
SELECT symbol
	,`date`
	,timezone
	,`open`
	,high
	,low
	,`close`
	,volume
	,prev_open
	,prev_high
	,prev_low
	,prev_close
	,prev_volume
	,`close` - prev_close AS price_change
	,((`close` - prev_close) / NULLIF(prev_close, 0)) * 100 AS percentage_change
	,volume - prev_volume AS volume_change
	,(`open` - prev_close) / NULLIF(prev_close, 0) * 100 as gap_open_pct
	,Case when `close` > `open` THEN 1 ELSE 0 END as is_positive_day
FROM (
	SELECT *
		,LAG(`open`, 1) OVER (
			PARTITION BY symbol ORDER BY `date`
			) AS prev_open
		,LAG(high, 1) OVER (
			PARTITION BY symbol ORDER BY `date`
			) AS prev_high
		,LAG(low, 1) OVER (
			PARTITION BY symbol ORDER BY `date`
			) AS prev_low
		,LAG(`close`, 1) OVER (
			PARTITION BY symbol ORDER BY `date`
			) AS prev_close
		,LAG(volume, 1) OVER (
			PARTITION BY symbol ORDER BY `date`
			) AS prev_volume
	FROM {source_table}
	) AS daily_data