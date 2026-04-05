INSERT INTO {target_table} (
	symbol
	,ingestion_date
	,asset_type
	,name
	,description
	,cik
	,exchange
	,currency
	,country
	,sector
	,industry
	,address
	,official_site
	,fiscal_year_end
	,latest_quarter
	,market_capitalization
	,ebitda
	,pe_ratio
	,peg_ratio
	,book_value
	,dividend_per_share
	,dividend_yield
	,eps
	,revenue_per_share_ttm
	,profit_margin
	,operating_margin_ttm
	,return_on_assets_ttm
	,return_on_equity_ttm
	,revenue_ttm
	,gross_profit_ttm
	,diluted_eps_ttm
	,quarterly_earnings_growth_yoy
	,quarterly_revenue_growth_yoy
	,analyst_target_price
	,analyst_rating_strong_buy
	,analyst_rating_buy
	,analyst_rating_hold
	,analyst_rating_sell
	,analyst_rating_strong_sell
	,trailing_pe
	,forward_pe
	,price_to_sales_ratio_ttm
	,price_to_book_ratio
	,ev_to_revenue
	,ev_to_ebitda
	,beta
	,week_52_high
	,week_52_low
	,moving_avg_50d
	,moving_avg_200d
	,shares_outstanding
	,shares_float
	,percent_insiders
	,percent_institutions
	,dividend_date
	,ex_dividend_date
	)
SELECT TRIM(symbol)
	,CURRENT_TIMESTAMP AS ingestion_date
	,asset_type
	,name
	,description
	,cik
	,exchange
	,currency
	,country
	,sector
	,industry
	,address
	,official_site
	,fiscal_year_end
	,STR_TO_DATE(latest_quarter, '%Y-%m-%d')
	,market_capitalization
	,ebitda
	,pe_ratio
	,peg_ratio
	,book_value
	,dividend_per_share
	,dividend_yield
	,eps
	,revenue_per_share_ttm
	,profit_margin
	,operating_margin_ttm
	,return_on_assets_ttm
	,return_on_equity_ttm
	,revenue_ttm
	,gross_profit_ttm
	,diluted_eps_ttm
	,quarterly_earnings_growth_yoy
	,quarterly_revenue_growth_yoy
	,analyst_target_price
	,analyst_rating_strong_buy
	,analyst_rating_buy
	,analyst_rating_hold
	,analyst_rating_sell
	,analyst_rating_strong_sell
	,trailing_pe
	,forward_pe
	,price_to_sales_ratio_ttm
	,price_to_book_ratio
	,ev_to_revenue
	,ev_to_ebitda
	,beta
	,week_52_high
	,week_52_low
	,moving_avg_50d
	,moving_avg_200d
	,shares_outstanding
	,shares_float
	,percent_insiders
	,percent_institutions
	,STR_TO_DATE(dividend_date, '%Y-%m-%d')
	,STR_TO_DATE(ex_dividend_date, '%Y-%m-%d')
FROM {source_table}
WHERE symbol IS NOT NULL
	AND TRIM(symbol) <> ''
	AND CHAR_LENGTH(symbol) <= 10
	AND (
		latest_quarter IS NULL
		OR STR_TO_DATE(latest_quarter, '%Y-%m-%d') IS NOT NULL
		)
	AND (
		dividend_date IS NULL
		OR STR_TO_DATE(dividend_date, '%Y-%m-%d') IS NOT NULL
		)
	AND (
		ex_dividend_date IS NULL
		OR STR_TO_DATE(ex_dividend_date, '%Y-%m-%d') IS NOT NULL
		)
	AND (
		week_52_high IS NULL
		OR week_52_low IS NULL
		OR week_52_high >= week_52_low
		)
	AND (
		market_capitalization IS NULL
		OR market_capitalization >= 0
		)
	AND (
		revenue_ttm IS NULL
		OR revenue_ttm >= 0
		);