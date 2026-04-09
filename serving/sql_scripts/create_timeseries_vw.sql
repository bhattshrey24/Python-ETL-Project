CREATE
	OR REPLACE VIEW {view_name} AS

SELECT `date`
	,symbol
	,ingestion_date
	,timezone
	,`open`
	,high
	,low
	,`close`
	,volume
FROM {source_table}