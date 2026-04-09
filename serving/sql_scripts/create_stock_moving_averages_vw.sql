CREATE
	OR REPLACE VIEW {view_name} AS

SELECT symbol
	,`date`
	,ingestion_date
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
FROM {source_table}