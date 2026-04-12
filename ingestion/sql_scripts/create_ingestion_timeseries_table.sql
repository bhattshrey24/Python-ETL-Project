INSERT IGNORE INTO {target_table} (
	symbol
	,timezone
	,`date`
	,`open`
	,high
	,low
	,`close`
	,volume
	)
VALUES (
	:symbol
	,:timezone
	,:date
	,:open
	,:high
	,:low
	,:close
	,:volume
	)
