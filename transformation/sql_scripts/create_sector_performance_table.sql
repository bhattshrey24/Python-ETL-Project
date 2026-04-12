INSERT INTO {target_table} (
     sector
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
)
SELECT
     t3.sector
    ,t3.avg_market_cap_by_sector
    ,t3.total_market_cap
    ,t3.max_market_cap
    ,t3.min_market_cap
    ,t3.avg_pe_ratio
    ,t3.avg_eps
    ,t3.avg_profit_margin
    ,t3.avg_beta
    ,t3.company_count
    ,t4.symbol AS top_company_by_market_cap
FROM (
    SELECT
         sector
        ,AVG(market_capitalization)  AS avg_market_cap_by_sector
        ,SUM(market_capitalization)  AS total_market_cap
        ,MAX(market_capitalization)  AS max_market_cap
        ,MIN(market_capitalization)  AS min_market_cap
        ,AVG(pe_ratio)               AS avg_pe_ratio
        ,AVG(eps)                    AS avg_eps
        ,AVG(profit_margin)          AS avg_profit_margin
        ,AVG(beta)                   AS avg_beta
        ,COUNT(DISTINCT symbol)      AS company_count
    FROM {source_table}
    GROUP BY sector
) t3
INNER JOIN (
    SELECT symbol, sector
    FROM (
        SELECT
             symbol
            ,sector
            ,ROW_NUMBER() OVER (
                PARTITION BY sector ORDER BY market_capitalization DESC
            ) AS rn
        FROM {source_table}
    ) AS ranked
    WHERE rn = 1
) t4 ON t3.sector = t4.sector
ON DUPLICATE KEY UPDATE
     ingestion_date            = VALUES(ingestion_date)
    ,avg_market_cap_by_sector  = VALUES(avg_market_cap_by_sector)
    ,total_market_cap          = VALUES(total_market_cap)
    ,max_market_cap            = VALUES(max_market_cap)
    ,min_market_cap            = VALUES(min_market_cap)
    ,avg_pe_ratio              = VALUES(avg_pe_ratio)
    ,avg_eps                   = VALUES(avg_eps)
    ,avg_profit_margin         = VALUES(avg_profit_margin)
    ,avg_beta                  = VALUES(avg_beta)
    ,company_count             = VALUES(company_count)
    ,top_company_by_market_cap = VALUES(top_company_by_market_cap);