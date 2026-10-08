-- =====================================================================
-- STOCK MARKET ANALYSIS IN SQL  |  Labmentix Project 5  |  Vipsa
-- Six NSE stocks (Bajaj Auto, Eicher Motors, Hero Motocorp, Infosys, TCS, TVS Motors)
-- 889 trading days each, 1 Jan 2015 to 31 Jul 2018.  Database: MySQL 8.0.
--
-- HOW TO RUN: run this file top to bottom on a fresh database.
-- BEFORE YOU RUN: the six CSVs must be in MySQL's Uploads folder (find it with
--   SHOW VARIABLES LIKE 'secure_file_priv';). If yours is different from
--   C:/ProgramData/MySQL/MySQL Server 8.0/Uploads
--   change the six LOAD DATA paths in Part 0.
--
-- KEY FINDING: TCS (31 May 2018) and Infosys (15 Jun 2015) had 1:1 BONUS ISSUES, so their price
-- halved overnight with no real loss. Raw prices make them look like losers; adjusted prices
-- (earlier prices divided by 2) show they are among the best performers (Tasks 11, 12, 13).
-- =====================================================================

CREATE DATABASE IF NOT EXISTS stock_analysis;
USE stock_analysis;

-- =====================================================================
-- PART 0: LOAD THE DATA
-- Turns dates like 31-July-2018 into real dates and empty cells into NULL.
-- =====================================================================

DROP TABLE IF EXISTS bajaj_auto;
CREATE TABLE bajaj_auto (
  `date` DATE PRIMARY KEY,
  open_price DECIMAL(12,2), high_price DECIMAL(12,2), low_price DECIMAL(12,2),
  close_price DECIMAL(12,2), wap DECIMAL(16,4),
  no_of_shares BIGINT, no_of_trades BIGINT, total_turnover DECIMAL(20,2),
  deliverable_qty BIGINT, pct_deli_qty DECIMAL(6,2),
  spread_high_low DECIMAL(12,2), spread_close_open DECIMAL(12,2)
);
LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/Bajaj Auto.csv' INTO TABLE bajaj_auto
FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' IGNORE 1 LINES
(@d,@o,@h,@l,@c,@w,@s,@tr,@to,@dq,@pd,@shl,@sco)
SET `date` = STR_TO_DATE(@d, '%d-%M-%Y'),
  open_price = NULLIF(@o,''), high_price = NULLIF(@h,''), low_price = NULLIF(@l,''),
  close_price = NULLIF(@c,''), wap = NULLIF(@w,''), no_of_shares = NULLIF(@s,''),
  no_of_trades = NULLIF(@tr,''), total_turnover = NULLIF(@to,''),
  deliverable_qty = NULLIF(@dq,''), pct_deli_qty = NULLIF(@pd,''),
  spread_high_low = NULLIF(@shl,''), spread_close_open = NULLIF(TRIM(@sco),'');

DROP TABLE IF EXISTS eicher_motors;
CREATE TABLE eicher_motors LIKE bajaj_auto;
LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/Eicher Motors.csv' INTO TABLE eicher_motors
FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' IGNORE 1 LINES
(@d,@o,@h,@l,@c,@w,@s,@tr,@to,@dq,@pd,@shl,@sco)
SET `date` = STR_TO_DATE(@d, '%d-%M-%Y'),
  open_price = NULLIF(@o,''), high_price = NULLIF(@h,''), low_price = NULLIF(@l,''),
  close_price = NULLIF(@c,''), wap = NULLIF(@w,''), no_of_shares = NULLIF(@s,''),
  no_of_trades = NULLIF(@tr,''), total_turnover = NULLIF(@to,''),
  deliverable_qty = NULLIF(@dq,''), pct_deli_qty = NULLIF(@pd,''),
  spread_high_low = NULLIF(@shl,''), spread_close_open = NULLIF(TRIM(@sco),'');

DROP TABLE IF EXISTS hero_motocorp;
CREATE TABLE hero_motocorp LIKE bajaj_auto;
LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/Hero Motocorp.csv' INTO TABLE hero_motocorp
FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' IGNORE 1 LINES
(@d,@o,@h,@l,@c,@w,@s,@tr,@to,@dq,@pd,@shl,@sco)
SET `date` = STR_TO_DATE(@d, '%d-%M-%Y'),
  open_price = NULLIF(@o,''), high_price = NULLIF(@h,''), low_price = NULLIF(@l,''),
  close_price = NULLIF(@c,''), wap = NULLIF(@w,''), no_of_shares = NULLIF(@s,''),
  no_of_trades = NULLIF(@tr,''), total_turnover = NULLIF(@to,''),
  deliverable_qty = NULLIF(@dq,''), pct_deli_qty = NULLIF(@pd,''),
  spread_high_low = NULLIF(@shl,''), spread_close_open = NULLIF(TRIM(@sco),'');

DROP TABLE IF EXISTS infosys;
CREATE TABLE infosys LIKE bajaj_auto;
LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/Infosys.csv' INTO TABLE infosys
FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' IGNORE 1 LINES
(@d,@o,@h,@l,@c,@w,@s,@tr,@to,@dq,@pd,@shl,@sco)
SET `date` = STR_TO_DATE(@d, '%d-%M-%Y'),
  open_price = NULLIF(@o,''), high_price = NULLIF(@h,''), low_price = NULLIF(@l,''),
  close_price = NULLIF(@c,''), wap = NULLIF(@w,''), no_of_shares = NULLIF(@s,''),
  no_of_trades = NULLIF(@tr,''), total_turnover = NULLIF(@to,''),
  deliverable_qty = NULLIF(@dq,''), pct_deli_qty = NULLIF(@pd,''),
  spread_high_low = NULLIF(@shl,''), spread_close_open = NULLIF(TRIM(@sco),'');

DROP TABLE IF EXISTS tcs;
CREATE TABLE tcs LIKE bajaj_auto;
LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/TCS.csv' INTO TABLE tcs
FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' IGNORE 1 LINES
(@d,@o,@h,@l,@c,@w,@s,@tr,@to,@dq,@pd,@shl,@sco)
SET `date` = STR_TO_DATE(@d, '%d-%M-%Y'),
  open_price = NULLIF(@o,''), high_price = NULLIF(@h,''), low_price = NULLIF(@l,''),
  close_price = NULLIF(@c,''), wap = NULLIF(@w,''), no_of_shares = NULLIF(@s,''),
  no_of_trades = NULLIF(@tr,''), total_turnover = NULLIF(@to,''),
  deliverable_qty = NULLIF(@dq,''), pct_deli_qty = NULLIF(@pd,''),
  spread_high_low = NULLIF(@shl,''), spread_close_open = NULLIF(TRIM(@sco),'');

DROP TABLE IF EXISTS tvs_motors;
CREATE TABLE tvs_motors LIKE bajaj_auto;
LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/TVS Motors.csv' INTO TABLE tvs_motors
FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' IGNORE 1 LINES
(@d,@o,@h,@l,@c,@w,@s,@tr,@to,@dq,@pd,@shl,@sco)
SET `date` = STR_TO_DATE(@d, '%d-%M-%Y'),
  open_price = NULLIF(@o,''), high_price = NULLIF(@h,''), low_price = NULLIF(@l,''),
  close_price = NULLIF(@c,''), wap = NULLIF(@w,''), no_of_shares = NULLIF(@s,''),
  no_of_trades = NULLIF(@tr,''), total_turnover = NULLIF(@to,''),
  deliverable_qty = NULLIF(@dq,''), pct_deli_qty = NULLIF(@pd,''),
  spread_high_low = NULLIF(@shl,''), spread_close_open = NULLIF(TRIM(@sco),'');

-- Check: every table should show 889 rows, 2015-01-01 to 2018-07-31
SELECT 'bajaj_auto' AS tbl, COUNT(*) AS n, MIN(`date`) AS first_day, MAX(`date`) AS last_day FROM bajaj_auto
UNION ALL SELECT 'eicher_motors', COUNT(*), MIN(`date`), MAX(`date`) FROM eicher_motors
UNION ALL SELECT 'hero_motocorp', COUNT(*), MIN(`date`), MAX(`date`) FROM hero_motocorp
UNION ALL SELECT 'infosys', COUNT(*), MIN(`date`), MAX(`date`) FROM infosys
UNION ALL SELECT 'tcs', COUNT(*), MIN(`date`), MAX(`date`) FROM tcs
UNION ALL SELECT 'tvs_motors', COUNT(*), MIN(`date`), MAX(`date`) FROM tvs_motors;

-- =====================================================================
-- PART 1: EXPLORE THE DATA
-- =====================================================================

-- TASK 1: How much history? (Bajaj Auto)
-- Expect: 889 | 2015-01-01 | 2018-07-31
SELECT COUNT(*) AS trading_days,
       MIN(`date`) AS first_day,
       MAX(`date`) AS last_day
FROM bajaj_auto;

-- TASK 2: Eicher's five highest closing prices
-- Expect: five rows, all September 2017, top close 32786.40
SELECT `date`, close_price
FROM eicher_motors
ORDER BY close_price DESC
LIMIT 5;

-- TASK 3: TCS average close per year (RAW prices)
-- Expect: 2015 2537.39 | 2016 2419.00 | 2017 2475.36 | 2018 2729.12
-- Careful: 2018 is only 7 months and mixes pre- and post-bonus prices (see Task 3b).
SELECT YEAR(`date`) AS year,
       ROUND(AVG(close_price), 2) AS avg_close
FROM tcs
GROUP BY YEAR(`date`)
ORDER BY year;

-- TASK 3b: TCS average close per year on ADJUSTED prices (fixes the 2018 mix-up)
-- Expect: 2015 1268.69 | 2016 1209.50 | 2017 1237.68 | 2018 1646.45
SELECT YEAR(`date`) AS year,
       ROUND(AVG(CASE WHEN `date` < '2018-05-31' THEN close_price / 2 ELSE close_price END), 2) AS avg_adj_close
FROM tcs
GROUP BY YEAR(`date`)
ORDER BY year;

-- TASK 4: Missing delivery data (NULLs) across all six stocks
-- Expect: 6 rows on two dates (2015-12-09 and 2017-08-31)
SELECT 'bajaj_auto' AS stock, `date` FROM bajaj_auto WHERE deliverable_qty IS NULL
UNION ALL
SELECT 'eicher_motors', `date` FROM eicher_motors WHERE deliverable_qty IS NULL
UNION ALL
SELECT 'hero_motocorp', `date` FROM hero_motocorp WHERE deliverable_qty IS NULL
UNION ALL
SELECT 'infosys', `date` FROM infosys WHERE deliverable_qty IS NULL
UNION ALL
SELECT 'tcs', `date` FROM tcs WHERE deliverable_qty IS NULL
UNION ALL
SELECT 'tvs_motors', `date` FROM tvs_motors WHERE deliverable_qty IS NULL;

-- =====================================================================
-- PART 2: MOVING AVERAGES AND SIGNALS
-- =====================================================================

-- TASK 5: 20-day and 50-day moving averages for Bajaj Auto
-- The first 19 (ma20) and 49 (ma50) days stay NULL: not enough history yet.
DROP TABLE IF EXISTS bajaj1;
CREATE TABLE bajaj1 AS
SELECT
    `date`,
    close_price,
    CASE WHEN ROW_NUMBER() OVER (ORDER BY `date`) >= 20
         THEN ROUND(AVG(close_price) OVER (ORDER BY `date` ROWS BETWEEN 19 PRECEDING AND CURRENT ROW), 2)
    END AS ma20,
    CASE WHEN ROW_NUMBER() OVER (ORDER BY `date`) >= 50
         THEN ROUND(AVG(close_price) OVER (ORDER BY `date` ROWS BETWEEN 49 PRECEDING AND CURRENT ROW), 2)
    END AS ma50
FROM bajaj_auto;

SELECT * FROM bajaj1;

-- Check for Task 5. Expect: 2015-01-29 ma20 = 2415.53 | 2015-03-13 ma50 = 2283.80 | 2018-07-31 ma20 = 2918.51
SELECT `date`, ma20, ma50 FROM bajaj1
WHERE `date` IN ('2015-01-29', '2015-03-13', '2018-07-31');

-- TASK 6: Master table, all six closing prices side by side
-- Expect: 889 rows, 7 columns; on 2018-07-31 bajaj = 2700.70 and tvs = 517.45
DROP TABLE IF EXISTS master_table;
CREATE TABLE master_table AS
SELECT b.`date`,
       b.close_price AS bajaj,
       t.close_price AS tcs,
       v.close_price AS tvs,
       i.close_price AS infosys,
       e.close_price AS eicher,
       h.close_price AS hero
FROM bajaj_auto b
JOIN tcs t            ON t.`date` = b.`date`
JOIN tvs_motors v     ON v.`date` = b.`date`
JOIN infosys i        ON i.`date` = b.`date`
JOIN eicher_motors e  ON e.`date` = b.`date`
JOIN hero_motocorp h  ON h.`date` = b.`date`;

SELECT * FROM master_table;

SELECT * FROM master_table WHERE `date` = '2018-07-31';

-- TASK 7: Buy / Sell / Hold signals for Bajaj Auto (golden cross)
-- Buy = ma20 crosses ABOVE ma50 today; Sell = crosses BELOW; otherwise Hold.
-- `signal` is a reserved word in MySQL, so it needs backticks.
-- Expect: 889 rows; first Buy 2015-05-18; first Sell 2015-08-24
DROP TABLE IF EXISTS bajaj2;
CREATE TABLE bajaj2 AS
SELECT `date`, close_price,
    CASE
        WHEN ma20 IS NULL OR ma50 IS NULL
          OR prev_ma20 IS NULL OR prev_ma50 IS NULL THEN 'Hold'
        WHEN ma20 > ma50 AND prev_ma20 <= prev_ma50 THEN 'Buy'
        WHEN ma20 < ma50 AND prev_ma20 >= prev_ma50 THEN 'Sell'
        ELSE 'Hold'
    END AS `signal`
FROM (
    SELECT `date`, close_price, ma20, ma50,
           LAG(ma20) OVER (ORDER BY `date`) AS prev_ma20,
           LAG(ma50) OVER (ORDER BY `date`) AS prev_ma50
    FROM bajaj1
) AS t;

SELECT * FROM bajaj2;

-- TASK 8: How often did each signal fire? (Bajaj Auto)
-- Expect: Buy 12 | Hold 866 | Sell 11
SELECT `signal`, COUNT(*) AS days
FROM bajaj2
GROUP BY `signal`
ORDER BY `signal`;

-- TASK 8b: Completed Buy-then-Sell round trips for Bajaj Auto
-- Expect: 11 rows. Six lasted 30 trading days or less, and five of those six lost money.
WITH events AS (
    SELECT `date`, close_price, `signal`,
           LEAD(`signal`)    OVER (ORDER BY `date`) AS next_signal,
           LEAD(`date`)      OVER (ORDER BY `date`) AS next_date,
           LEAD(close_price) OVER (ORDER BY `date`) AS next_price
    FROM bajaj2
    WHERE `signal` <> 'Hold'
)
SELECT e.`date` AS buy_date, e.next_date AS sell_date,
       (SELECT COUNT(*) FROM bajaj2 b WHERE b.`date` > e.`date` AND b.`date` <= e.next_date) AS trading_days,
       ROUND(100 * (e.next_price / e.close_price - 1), 1) AS return_pct
FROM events e
WHERE e.`signal` = 'Buy' AND e.next_signal = 'Sell'
ORDER BY e.`date`;

-- TASK 9: Signal on a given day, as a reusable function
-- Expect: 2015-05-18 Buy | 2016-01-04 Hold | 2018-06-21 Buy
-- A date when the market was closed returns NULL (no row exists for it).
DROP FUNCTION IF EXISTS bajaj_signal;
DELIMITER $$
CREATE FUNCTION bajaj_signal(d DATE)
RETURNS VARCHAR(4) DETERMINISTIC READS SQL DATA
BEGIN
    DECLARE s VARCHAR(4);
    SELECT `signal` INTO s FROM bajaj2 WHERE `date` = d;
    RETURN s;
END $$
DELIMITER ;

SELECT bajaj_signal('2015-05-18') AS on_2015_05_18,
       bajaj_signal('2016-01-04') AS on_2016_01_04,
       bajaj_signal('2018-06-21') AS on_2018_06_21;

-- TASK 10: All six stocks in one query (PARTITION BY restarts every calculation per stock)
-- Uses RAW prices, as the course deck did.
-- Expect: Bajaj 12/11 | Eicher 6/7 | Hero 9/9 | Infosys 9/9 | TCS 12/13 | TVS 8/8  (56 Buys, 57 Sells)
WITH prices AS (
    SELECT 'Bajaj Auto' AS stock, `date`, close_price FROM bajaj_auto
    UNION ALL SELECT 'Eicher Motors', `date`, close_price FROM eicher_motors
    UNION ALL SELECT 'Hero Motocorp', `date`, close_price FROM hero_motocorp
    UNION ALL SELECT 'Infosys', `date`, close_price FROM infosys
    UNION ALL SELECT 'TCS', `date`, close_price FROM tcs
    UNION ALL SELECT 'TVS Motors', `date`, close_price FROM tvs_motors
),
ma AS (
    SELECT stock, `date`, close_price,
        CASE WHEN ROW_NUMBER() OVER (PARTITION BY stock ORDER BY `date`) >= 20
             THEN AVG(close_price) OVER (PARTITION BY stock ORDER BY `date`
                  ROWS BETWEEN 19 PRECEDING AND CURRENT ROW) END AS ma20,
        CASE WHEN ROW_NUMBER() OVER (PARTITION BY stock ORDER BY `date`) >= 50
             THEN AVG(close_price) OVER (PARTITION BY stock ORDER BY `date`
                  ROWS BETWEEN 49 PRECEDING AND CURRENT ROW) END AS ma50
    FROM prices
),
lagged AS (
    SELECT stock, `date`, ma20, ma50,
        LAG(ma20) OVER (PARTITION BY stock ORDER BY `date`) AS prev_ma20,
        LAG(ma50) OVER (PARTITION BY stock ORDER BY `date`) AS prev_ma50
    FROM ma
),
sig AS (
    SELECT stock, `date`,
        CASE
            WHEN ma20 IS NULL OR ma50 IS NULL
              OR prev_ma20 IS NULL OR prev_ma50 IS NULL THEN 'Hold'
            WHEN ma20 > ma50 AND prev_ma20 <= prev_ma50 THEN 'Buy'
            WHEN ma20 < ma50 AND prev_ma20 >= prev_ma50 THEN 'Sell'
            ELSE 'Hold'
        END AS `signal`
    FROM lagged
),
latest AS (
    SELECT stock, `date`, `signal`,
        ROW_NUMBER() OVER (PARTITION BY stock ORDER BY `date` DESC) AS rn
    FROM sig
    WHERE `signal` <> 'Hold'
)
SELECT s.stock,
       SUM(s.`signal` = 'Buy')  AS buys,
       SUM(s.`signal` = 'Sell') AS sells,
       l.`date`   AS last_signal_date,
       l.`signal` AS last_signal
FROM sig s
JOIN latest l ON l.stock = s.stock AND l.rn = 1
GROUP BY s.stock, l.`date`, l.`signal`
ORDER BY s.stock;

-- TASK 10b: Save moving averages and signals for ALL SIX stocks in one table
-- NOTE: built on RAW close prices (same as Task 10), so TCS still shows the false Sell.
-- The corrected TCS and Infosys signals are in the STRETCH query at the end.
-- Expect: 5334 rows; counts per stock match Task 10
DROP TABLE IF EXISTS all_signals;
CREATE TABLE all_signals AS
WITH prices AS (
    SELECT 'Bajaj Auto' AS stock, `date`, close_price FROM bajaj_auto
    UNION ALL SELECT 'Eicher Motors', `date`, close_price FROM eicher_motors
    UNION ALL SELECT 'Hero Motocorp', `date`, close_price FROM hero_motocorp
    UNION ALL SELECT 'Infosys', `date`, close_price FROM infosys
    UNION ALL SELECT 'TCS', `date`, close_price FROM tcs
    UNION ALL SELECT 'TVS Motors', `date`, close_price FROM tvs_motors
),
ma AS (
    SELECT stock, `date`, close_price,
        CASE WHEN ROW_NUMBER() OVER (PARTITION BY stock ORDER BY `date`) >= 20
             THEN AVG(close_price) OVER (PARTITION BY stock ORDER BY `date`
                  ROWS BETWEEN 19 PRECEDING AND CURRENT ROW) END AS ma20,
        CASE WHEN ROW_NUMBER() OVER (PARTITION BY stock ORDER BY `date`) >= 50
             THEN AVG(close_price) OVER (PARTITION BY stock ORDER BY `date`
                  ROWS BETWEEN 49 PRECEDING AND CURRENT ROW) END AS ma50
    FROM prices
),
lagged AS (
    SELECT stock, `date`, close_price, ma20, ma50,
        LAG(ma20) OVER (PARTITION BY stock ORDER BY `date`) AS prev_ma20,
        LAG(ma50) OVER (PARTITION BY stock ORDER BY `date`) AS prev_ma50
    FROM ma
)
SELECT stock, `date`, close_price,
    ROUND(ma20, 2) AS ma20, ROUND(ma50, 2) AS ma50,
    CASE
        WHEN ma20 IS NULL OR ma50 IS NULL
          OR prev_ma20 IS NULL OR prev_ma50 IS NULL THEN 'Hold'
        WHEN ma20 > ma50 AND prev_ma20 <= prev_ma50 THEN 'Buy'
        WHEN ma20 < ma50 AND prev_ma20 >= prev_ma50 THEN 'Sell'
        ELSE 'Hold'
    END AS `signal`
FROM lagged;

SELECT COUNT(*) AS total_rows FROM all_signals;
SELECT stock, SUM(`signal` = 'Buy') AS buys, SUM(`signal` = 'Sell') AS sells, SUM(`signal` = 'Hold') AS holds
FROM all_signals GROUP BY stock ORDER BY stock;
SELECT * FROM all_signals WHERE stock = 'Bajaj Auto' AND `date` IN ('2015-01-29', '2015-03-13', '2018-07-31');

-- =====================================================================
-- PART 3: QUESTION THE RESULT
-- =====================================================================

-- TASK 11: Percentage change from first to last day, per stock (RAW prices)
-- Expect: TVS 86.9 | Eicher 82.6 | Bajaj 10.0 | Hero 6.0 | TCS -23.8 | Infosys -30.9
WITH prices AS (
    SELECT 'Bajaj Auto' AS stock, `date`, close_price FROM bajaj_auto
    UNION ALL SELECT 'Eicher Motors', `date`, close_price FROM eicher_motors
    UNION ALL SELECT 'Hero Motocorp', `date`, close_price FROM hero_motocorp
    UNION ALL SELECT 'Infosys', `date`, close_price FROM infosys
    UNION ALL SELECT 'TCS', `date`, close_price FROM tcs
    UNION ALL SELECT 'TVS Motors', `date`, close_price FROM tvs_motors
),
span AS (
    SELECT stock, MIN(`date`) AS first_date, MAX(`date`) AS last_date
    FROM prices
    GROUP BY stock
)
SELECT e.stock,
       f.close_price AS first_close,
       l.close_price AS last_close,
       ROUND(100.0 * (l.close_price - f.close_price) / f.close_price, 1) AS pct_change
FROM span e
JOIN prices f ON f.stock = e.stock AND f.`date` = e.first_date
JOIN prices l ON l.stock = e.stock AND l.`date` = e.last_date
ORDER BY pct_change DESC;

-- TASK 11b: Rank the six stocks by ADJUSTED return with RANK()
-- Expect: TVS 1 | Eicher 2 | TCS 3 | Infosys 4 | Bajaj 5 | Hero 6
WITH prices AS (
    SELECT 'Bajaj Auto' AS stock, `date`, close_price AS adj_close FROM bajaj_auto
    UNION ALL SELECT 'Eicher Motors', `date`, close_price FROM eicher_motors
    UNION ALL SELECT 'Hero Motocorp', `date`, close_price FROM hero_motocorp
    UNION ALL SELECT 'Infosys', `date`,
        CASE WHEN `date` < '2015-06-15' THEN close_price / 2 ELSE close_price END FROM infosys
    UNION ALL SELECT 'TCS', `date`,
        CASE WHEN `date` < '2018-05-31' THEN close_price / 2 ELSE close_price END FROM tcs
    UNION ALL SELECT 'TVS Motors', `date`, close_price FROM tvs_motors
),
span AS (
    SELECT stock, MIN(`date`) AS first_date, MAX(`date`) AS last_date
    FROM prices GROUP BY stock
),
returns AS (
    SELECT s.stock,
           ROUND(100.0 * (l.adj_close - f.adj_close) / f.adj_close, 1) AS adjusted_return
    FROM span s
    JOIN prices f ON f.stock = s.stock AND f.`date` = s.first_date
    JOIN prices l ON l.stock = s.stock AND l.`date` = s.last_date
)
SELECT stock, adjusted_return,
       RANK() OVER (ORDER BY adjusted_return DESC) AS return_rank
FROM returns
ORDER BY return_rank;

-- TASK 11c: RANK() with ties: who had the most Buy signals? (RAW-price signals from all_signals)
-- Expect: Bajaj and TCS tie at rank 1 (12 Buys), then Hero and Infosys tie at rank 3 (9), TVS 5, Eicher 6
SELECT stock, SUM(`signal` = 'Buy') AS buys,
       RANK() OVER (ORDER BY SUM(`signal` = 'Buy') DESC) AS buy_rank
FROM all_signals
GROUP BY stock
ORDER BY buy_rank, stock;

-- TASK 12: Each stock's single worst day (finds the data trap)
-- Expect: TCS 2018-05-31 (-50.4) and Infosys 2015-06-15 (-49.9) are far worse than the rest (-6% to -10%).
-- Both are 1:1 BONUS ISSUES: every shareholder gets one free share per share held, so the price
-- halves overnight and nobody loses value.
WITH prices AS (
    SELECT 'Bajaj Auto' AS stock, `date`, close_price FROM bajaj_auto
    UNION ALL SELECT 'Eicher Motors', `date`, close_price FROM eicher_motors
    UNION ALL SELECT 'Hero Motocorp', `date`, close_price FROM hero_motocorp
    UNION ALL SELECT 'Infosys', `date`, close_price FROM infosys
    UNION ALL SELECT 'TCS', `date`, close_price FROM tcs
    UNION ALL SELECT 'TVS Motors', `date`, close_price FROM tvs_motors
),
moves AS (
    SELECT stock, `date`, close_price,
           100.0 * (close_price / LAG(close_price) OVER (PARTITION BY stock ORDER BY `date`) - 1) AS pct_move
    FROM prices
),
ranked AS (
    SELECT stock, `date`, close_price, ROUND(pct_move, 1) AS pct_move,
           ROW_NUMBER() OVER (PARTITION BY stock ORDER BY pct_move ASC) AS rn
    FROM moves
    WHERE pct_move IS NOT NULL
)
SELECT stock, `date`, close_price, pct_move
FROM ranked
WHERE rn = 1
ORDER BY pct_move ASC;

-- TASK 13: Fix it. Halve every price BEFORE each company's own bonus date.
-- Expect: Infosys +38.2 | TCS +52.4   (they were -30.9 and -23.8 in Task 11)
WITH adjusted AS (
    SELECT 'TCS' AS stock, `date`,
           CASE WHEN `date` < '2018-05-31' THEN close_price / 2 ELSE close_price END AS adj_close
    FROM tcs
    UNION ALL
    SELECT 'Infosys' AS stock, `date`,
           CASE WHEN `date` < '2015-06-15' THEN close_price / 2 ELSE close_price END AS adj_close
    FROM infosys
)
SELECT stock,
       ROUND(100.0 * (
           MAX(CASE WHEN `date` = '2018-07-31' THEN adj_close END) /
           MAX(CASE WHEN `date` = '2015-01-01' THEN adj_close END) - 1), 1) AS adjusted_pct_change
FROM adjusted
GROUP BY stock
ORDER BY stock;

-- STRETCH: Rebuild TCS and Infosys signals on ADJUSTED prices
-- Expect: TCS 12 Buys / 12 Sells, last signal Buy on 2018-04-20
--         (raw prices gave 12/13 with a false Sell on 2018-06-05, caused by the price cliff)
--         Infosys 10 / 10, last signal Buy on 2018-05-07 (raw gave 9/9)
WITH adjusted AS (
    SELECT 'TCS' AS stock, `date`,
           CASE WHEN `date` < '2018-05-31' THEN close_price / 2 ELSE close_price END AS adj_close
    FROM tcs
    UNION ALL
    SELECT 'Infosys' AS stock, `date`,
           CASE WHEN `date` < '2015-06-15' THEN close_price / 2 ELSE close_price END AS adj_close
    FROM infosys
),
ma AS (
    SELECT stock, `date`,
        CASE WHEN ROW_NUMBER() OVER (PARTITION BY stock ORDER BY `date`) >= 20
             THEN AVG(adj_close) OVER (PARTITION BY stock ORDER BY `date`
                  ROWS BETWEEN 19 PRECEDING AND CURRENT ROW) END AS ma20,
        CASE WHEN ROW_NUMBER() OVER (PARTITION BY stock ORDER BY `date`) >= 50
             THEN AVG(adj_close) OVER (PARTITION BY stock ORDER BY `date`
                  ROWS BETWEEN 49 PRECEDING AND CURRENT ROW) END AS ma50
    FROM adjusted
),
lagged AS (
    SELECT stock, `date`, ma20, ma50,
        LAG(ma20) OVER (PARTITION BY stock ORDER BY `date`) AS prev_ma20,
        LAG(ma50) OVER (PARTITION BY stock ORDER BY `date`) AS prev_ma50
    FROM ma
),
sig AS (
    SELECT stock, `date`,
        CASE
            WHEN ma20 IS NULL OR ma50 IS NULL
              OR prev_ma20 IS NULL OR prev_ma50 IS NULL THEN 'Hold'
            WHEN ma20 > ma50 AND prev_ma20 <= prev_ma50 THEN 'Buy'
            WHEN ma20 < ma50 AND prev_ma20 >= prev_ma50 THEN 'Sell'
            ELSE 'Hold'
        END AS `signal`
    FROM lagged
),
latest AS (
    SELECT stock, `date`, `signal`,
        ROW_NUMBER() OVER (PARTITION BY stock ORDER BY `date` DESC) AS rn
    FROM sig
    WHERE `signal` <> 'Hold'
)
SELECT s.stock,
       SUM(s.`signal` = 'Buy')  AS buys,
       SUM(s.`signal` = 'Sell') AS sells,
       l.`date`   AS last_signal_date,
       l.`signal` AS last_signal
FROM sig s
JOIN latest l ON l.stock = s.stock AND l.rn = 1
GROUP BY s.stock, l.`date`, l.`signal`
ORDER BY s.stock;