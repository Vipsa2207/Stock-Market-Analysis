# Stock Market Analysis in SQL

An analysis of six NSE-listed stocks (Bajaj Auto, Eicher Motors, Hero MotoCorp, Infosys, TCS and TVS Motors) from 1 January 2015 to 31 July 2018, built in MySQL with a Python/Streamlit dashboard. Labmentix Project 5.

**Live app:** https://stocksense-nse.streamlit.app/

## The question

Using a 20-day and a 50-day moving average, which of the six stocks gives a Buy, Sell or Hold signal, and how do the six companies compare?

## Key finding: a data trap

The course deck's final report says to sell TCS and Infosys because both look like big losers. That conclusion does not hold up.

Both companies issued **1:1 bonus shares** (TCS on 31 May 2018, Infosys on 15 June 2015). Every shareholder received one free share for each share held, so the share price halved overnight without anyone losing value. Raw prices show this as a one-day fall of about 50%. After dividing every earlier price by 2, the picture reverses:

| Stock | First close | Last close | Change, raw prices | Change, adjusted |
|---|---|---|---|---|
| TVS Motors | 276.85 | 517.45 | +86.9% | +86.9% |
| Eicher Motors | 15,239.15 | 27,820.95 | +82.6% | +82.6% |
| TCS | 2,548.20 | 1,941.25 | -23.8% | **+52.4%** |
| Infosys | 1,975.80 | 1,365.00 | -30.9% | **+38.2%** |
| Bajaj Auto | 2,454.10 | 2,700.70 | +10.0% | +10.0% |
| Hero MotoCorp | 3,107.30 | 3,293.80 | +6.0% | +6.0% |

The same price cliff also created a false Sell signal for TCS. On adjusted prices, TCS's latest signal is a Buy.

## Other findings

- A 20/50-day crossover signal fires rarely. For Bajaj Auto it gave 12 Buys, 11 Sells and 866 Hold days out of 889.
- Latest signals on adjusted prices: Buy for Bajaj Auto, Infosys and TCS; Sell for Eicher Motors, Hero MotoCorp and TVS Motors.
- Following the signals would not have beaten simply holding for any of the six stocks, even before trading costs. This comparison is computed in Python in the app's Strategy tab, not in SQL.
- The only missing data is the deliverable quantity column, on two dates.

The full write-up (claim, evidence and caveat for each finding) is in the PDF in the `report` folder.

## What is in this repository

```
.
├── app.py                  Streamlit app
├── stocks_clean.csv        Merged and cleaned data used by the app (6 stocks x 889 days)
├── requirements.txt        Python packages for the app
├── .streamlit/config.toml  Dark theme settings
├── sql/                    Final MySQL file (all tasks, runs top to bottom)
└── report/                 Insights report (PDF)
```

## SQL techniques used

- Loading and cleaning: `LOAD DATA INFILE`, `STR_TO_DATE`, `NULLIF`
- Window functions: moving averages with `AVG() OVER (... ROWS BETWEEN ...)`, `LAG`, `ROW_NUMBER`, `RANK`, `PARTITION BY`
- Common table expressions (CTEs) to combine all six stocks in one query
- `JOIN` to build a master table with all six closing prices side by side
- A stored function, `bajaj_signal(date)`, that returns the Buy, Sell or Hold signal for a given day
- `CASE` logic for the golden-cross rule: Buy when the 20-day average crosses above the 50-day average, Sell when it crosses below

## The Streamlit app

Five tabs: **Overview** (the key finding), **Price Trends** (adjusted vs raw prices, bonus-issue dates marked), **Signals** (averages with Buy and Sell markers), **Strategy vs Hold**, and **SQL Lab**, a read-only playground where you can run your own `SELECT` queries on the data (SQLite syntax).

To run it on your own computer:

```
pip install -r requirements.txt
streamlit run app.py
```

## Running the SQL file

1. Install MySQL 8.0.
2. Copy the six source CSV files into MySQL's Uploads folder. Find its location with `SHOW VARIABLES LIKE 'secure_file_priv';`.
3. If that folder is different from the one in the `LOAD DATA` lines in Part 0, change those paths.
4. Run the file top to bottom on a fresh database.

## Limitations

- Moving averages use only past prices, so every signal confirms a move that has already started.
- The data covers about 3.5 years and six stocks from two sectors (two-wheelers and IT services).
- Dividends, company news, brokerage, taxes and the wider market are not included.
- Prices before each bonus issue were divided by 2, assuming there were no other corporate actions in the period.

**This project is a data-analysis exercise and is not investment advice.**

## Author

Vipsa Patel, Data Analyst Intern, Labmentix
