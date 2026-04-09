CREATE
	OR REPLACE VIEW {view_name} AS

SELECT sector
	,ingestion_date
	,avg_market_cap_by_sector
	,total_market_cap
	,max_market_cap
	,min_market_cap
	,avg_pe_ratio
	,avg_eps
	,avg_profit_margin
	,avg_beta
	,company_count
	,top_company_by_market_cap
FROM {source_table}