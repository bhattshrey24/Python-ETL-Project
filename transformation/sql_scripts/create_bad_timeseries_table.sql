INSERT IGNORE INTO {target_table} (
  `date`,
  symbol,
  timezone,
  `open`,
  high,
  low,
  `close`,
  volume,
  reason -- stores the reason of why the row was rejected
)
SELECT
  `date`,
  symbol,
  timezone,
  `open`,
  high,
  low,
  `close`,
  volume,
  -- CONCAT_WS ignores NULLs, so only failing checks appear
  CONCAT_WS(' | ',
    CASE WHEN symbol IS NULL OR TRIM(symbol) = ''
         THEN 'invalid_symbol' END,

    CASE WHEN `date` IS NULL
         THEN 'null_date' END,

    CASE WHEN `date` > CURRENT_DATE
         THEN 'future_date' END,

    CASE WHEN timezone IS NULL
         THEN 'null_timezone' END,

    CASE WHEN `open` IS NULL OR `open` <= 0
         THEN 'invalid_open' END,

    CASE WHEN high IS NULL OR high <= 0
         THEN 'invalid_high' END,

    CASE WHEN low IS NULL OR low <= 0
         THEN 'invalid_low' END,

    CASE WHEN `close` IS NULL OR `close` <= 0
         THEN 'invalid_close' END,

    CASE WHEN volume IS NULL OR volume <= 0
         THEN 'invalid_volume' END,

    CASE WHEN high < low
         THEN 'high_less_than_low' END,

    CASE WHEN high < `open` OR high < `close`
         THEN 'high_not_highest' END,

    CASE WHEN low > `open` OR low > `close`
         THEN 'low_not_lowest' END
  ) AS reason

FROM {source_table}
WHERE NOT (
  symbol IS NOT NULL
  AND TRIM(symbol) <> ''
  AND `date` IS NOT NULL
  AND timezone IS NOT NULL
  AND `open` IS NOT NULL
  AND high IS NOT NULL
  AND low IS NOT NULL
  AND `close` IS NOT NULL
  AND volume IS NOT NULL
  AND `open` > 0
  AND high > 0
  AND low > 0
  AND `close` > 0
  AND volume > 0
  AND high >= low
  AND high >= `open`
  AND high >= `close`
  AND low <= `open`
  AND low <= `close`
  AND `date` <= CURRENT_DATE
);