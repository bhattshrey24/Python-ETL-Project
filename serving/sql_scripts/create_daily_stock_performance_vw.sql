CREATE
	OR REPLACE VIEW {view_name} AS

SELECT symbol
	,`date`
	,ingestion_date
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
FROM {source_table}