INSERT INTO {target_table} (
     symbol
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
VALUES (
     :symbol
    ,:asset_type
    ,:name
    ,:description
    ,:cik
    ,:exchange
    ,:currency
    ,:country
    ,:sector
    ,:industry
    ,:address
    ,:official_site
    ,:fiscal_year_end
    ,:latest_quarter
    ,:market_capitalization
    ,:ebitda
    ,:pe_ratio
    ,:peg_ratio
    ,:book_value
    ,:dividend_per_share
    ,:dividend_yield
    ,:eps
    ,:revenue_per_share_ttm
    ,:profit_margin
    ,:operating_margin_ttm
    ,:return_on_assets_ttm
    ,:return_on_equity_ttm
    ,:revenue_ttm
    ,:gross_profit_ttm
    ,:diluted_eps_ttm
    ,:quarterly_earnings_growth_yoy
    ,:quarterly_revenue_growth_yoy
    ,:analyst_target_price
    ,:analyst_rating_strong_buy
    ,:analyst_rating_buy
    ,:analyst_rating_hold
    ,:analyst_rating_sell
    ,:analyst_rating_strong_sell
    ,:trailing_pe
    ,:forward_pe
    ,:price_to_sales_ratio_ttm
    ,:price_to_book_ratio
    ,:ev_to_revenue
    ,:ev_to_ebitda
    ,:beta
    ,:week_52_high
    ,:week_52_low
    ,:moving_avg_50d
    ,:moving_avg_200d
    ,:shares_outstanding
    ,:shares_float
    ,:percent_insiders
    ,:percent_institutions
    ,:dividend_date
    ,:ex_dividend_date
)
AS new_row
ON DUPLICATE KEY UPDATE
     ingestion_date                  = CURRENT_TIMESTAMP
    ,asset_type                      = new_row.asset_type
    ,name                            = new_row.name
    ,description                     = new_row.description
    ,cik                             = new_row.cik
    ,exchange                        = new_row.exchange
    ,currency                        = new_row.currency
    ,country                         = new_row.country
    ,sector                          = new_row.sector
    ,industry                        = new_row.industry
    ,address                         = new_row.address
    ,official_site                   = new_row.official_site
    ,fiscal_year_end                 = new_row.fiscal_year_end
    ,latest_quarter                  = new_row.latest_quarter
    ,market_capitalization           = new_row.market_capitalization
    ,ebitda                          = new_row.ebitda
    ,pe_ratio                        = new_row.pe_ratio
    ,peg_ratio                       = new_row.peg_ratio
    ,book_value                      = new_row.book_value
    ,dividend_per_share              = new_row.dividend_per_share
    ,dividend_yield                  = new_row.dividend_yield
    ,eps                             = new_row.eps
    ,revenue_per_share_ttm           = new_row.revenue_per_share_ttm
    ,profit_margin                   = new_row.profit_margin
    ,operating_margin_ttm            = new_row.operating_margin_ttm
    ,return_on_assets_ttm            = new_row.return_on_assets_ttm
    ,return_on_equity_ttm            = new_row.return_on_equity_ttm
    ,revenue_ttm                     = new_row.revenue_ttm
    ,gross_profit_ttm                = new_row.gross_profit_ttm
    ,diluted_eps_ttm                 = new_row.diluted_eps_ttm
    ,quarterly_earnings_growth_yoy   = new_row.quarterly_earnings_growth_yoy
    ,quarterly_revenue_growth_yoy    = new_row.quarterly_revenue_growth_yoy
    ,analyst_target_price            = new_row.analyst_target_price
    ,analyst_rating_strong_buy       = new_row.analyst_rating_strong_buy
    ,analyst_rating_buy              = new_row.analyst_rating_buy
    ,analyst_rating_hold             = new_row.analyst_rating_hold
    ,analyst_rating_sell             = new_row.analyst_rating_sell
    ,analyst_rating_strong_sell      = new_row.analyst_rating_strong_sell
    ,trailing_pe                     = new_row.trailing_pe
    ,forward_pe                      = new_row.forward_pe
    ,price_to_sales_ratio_ttm        = new_row.price_to_sales_ratio_ttm
    ,price_to_book_ratio             = new_row.price_to_book_ratio
    ,ev_to_revenue                   = new_row.ev_to_revenue
    ,ev_to_ebitda                    = new_row.ev_to_ebitda
    ,beta                            = new_row.beta
    ,week_52_high                    = new_row.week_52_high
    ,week_52_low                     = new_row.week_52_low
    ,moving_avg_50d                  = new_row.moving_avg_50d
    ,moving_avg_200d                 = new_row.moving_avg_200d
    ,shares_outstanding              = new_row.shares_outstanding
    ,shares_float                    = new_row.shares_float
    ,percent_insiders                = new_row.percent_insiders
    ,percent_institutions            = new_row.percent_institutions
    ,dividend_date                   = new_row.dividend_date
    ,ex_dividend_date                = new_row.ex_dividend_date;