INSERT IGNORE INTO {target_table} (
  `date`,
  symbol,
  timezone,
  `open`,
  high,
  low,
  `close`,
  volume
)
SELECT
  STR_TO_DATE(`date`, '%Y-%m-%d') AS `date`,
  TRIM(symbol),
  timezone,
  `open`,
  high,
  low,
  `close`,
  volume
FROM {source_table} t
WHERE
  symbol IS NOT NULL
  AND TRIM(symbol) <> ''

  AND `date` IS NOT NULL
  AND STR_TO_DATE(`date`, '%Y-%m-%d') IS NOT NULL
  AND STR_TO_DATE(`date`, '%Y-%m-%d') <= CURRENT_DATE

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

  AND NOT EXISTS (
    SELECT 1
    FROM {target_table} t2
    WHERE t2.symbol = t.symbol
      AND t2.`date` = STR_TO_DATE(t.`date`, '%Y-%m-%d')
  );