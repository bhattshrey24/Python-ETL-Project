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
ON DUPLICATE KEY UPDATE
     ingestion_date                  = CURRENT_TIMESTAMP
    ,asset_type                      = VALUES(asset_type)
    ,name                            = VALUES(name)
    ,description                     = VALUES(description)
    ,cik                             = VALUES(cik)
    ,exchange                        = VALUES(exchange)
    ,currency                        = VALUES(currency)
    ,country                         = VALUES(country)
    ,sector                          = VALUES(sector)
    ,industry                        = VALUES(industry)
    ,address                         = VALUES(address)
    ,official_site                   = VALUES(official_site)
    ,fiscal_year_end                 = VALUES(fiscal_year_end)
    ,latest_quarter                  = VALUES(latest_quarter)
    ,market_capitalization           = VALUES(market_capitalization)
    ,ebitda                          = VALUES(ebitda)
    ,pe_ratio                        = VALUES(pe_ratio)
    ,peg_ratio                       = VALUES(peg_ratio)
    ,book_value                      = VALUES(book_value)
    ,dividend_per_share              = VALUES(dividend_per_share)
    ,dividend_yield                  = VALUES(dividend_yield)
    ,eps                             = VALUES(eps)
    ,revenue_per_share_ttm           = VALUES(revenue_per_share_ttm)
    ,profit_margin                   = VALUES(profit_margin)
    ,operating_margin_ttm            = VALUES(operating_margin_ttm)
    ,return_on_assets_ttm            = VALUES(return_on_assets_ttm)
    ,return_on_equity_ttm            = VALUES(return_on_equity_ttm)
    ,revenue_ttm                     = VALUES(revenue_ttm)
    ,gross_profit_ttm                = VALUES(gross_profit_ttm)
    ,diluted_eps_ttm                 = VALUES(diluted_eps_ttm)
    ,quarterly_earnings_growth_yoy   = VALUES(quarterly_earnings_growth_yoy)
    ,quarterly_revenue_growth_yoy    = VALUES(quarterly_revenue_growth_yoy)
    ,analyst_target_price            = VALUES(analyst_target_price)
    ,analyst_rating_strong_buy       = VALUES(analyst_rating_strong_buy)
    ,analyst_rating_buy              = VALUES(analyst_rating_buy)
    ,analyst_rating_hold             = VALUES(analyst_rating_hold)
    ,analyst_rating_sell             = VALUES(analyst_rating_sell)
    ,analyst_rating_strong_sell      = VALUES(analyst_rating_strong_sell)
    ,trailing_pe                     = VALUES(trailing_pe)
    ,forward_pe                      = VALUES(forward_pe)
    ,price_to_sales_ratio_ttm        = VALUES(price_to_sales_ratio_ttm)
    ,price_to_book_ratio             = VALUES(price_to_book_ratio)
    ,ev_to_revenue                   = VALUES(ev_to_revenue)
    ,ev_to_ebitda                    = VALUES(ev_to_ebitda)
    ,beta                            = VALUES(beta)
    ,week_52_high                    = VALUES(week_52_high)
    ,week_52_low                     = VALUES(week_52_low)
    ,moving_avg_50d                  = VALUES(moving_avg_50d)
    ,moving_avg_200d                 = VALUES(moving_avg_200d)
    ,shares_outstanding              = VALUES(shares_outstanding)
    ,shares_float                    = VALUES(shares_float)
    ,percent_insiders                = VALUES(percent_insiders)
    ,percent_institutions            = VALUES(percent_institutions)
    ,dividend_date                   = VALUES(dividend_date)
    ,ex_dividend_date                = VALUES(ex_dividend_date);