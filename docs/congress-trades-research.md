# Following politicians' stock trades: what the data is, who to watch, and whether it pays

Research notes, 4 October 2026. Companion to `trades.html` and `scripts/fetch_trades.py` in this repo.

## Short version

- **The data is public and free.** Since the 2012 STOCK Act, every member of Congress must disclose trades over $1,000 made by themselves, their spouse or dependent children on a Periodic Transaction Report (PTR) within 30 days of learning of the trade and never later than 45 days after it. The President and Vice President file the same report with the Office of Government Ethics. Amounts are reported as brackets ($1,001–$15,000 up to over $50,000,000), with no prices or share counts required.
- **Nancy Pelosi is the archetype.** Her household (the trades are executed by her husband Paul Pelosi and are reported with owner "SP") makes a handful of very large, concentrated bets each year, usually deep-in-the-money long-dated call options (LEAPS) on big tech. In 2026 so far: Intel and Uber calls in May, Bloom Energy shares and calls plus more Intel in July. She retires when her term ends on 3 January 2027, after which her trades stop being disclosed.
- **Trump's filings are not an equity signal.** As President he files PTRs, but the portfolio is overwhelmingly municipal bonds (over 1,000 positions worth $300M to $1B by CNBC's count), with some corporate bonds and tiny bank-stock stakes. His wealth is in Trump Media stock and crypto, which show up in the annual Form 278e rather than in trade reports.
- **Copying the aggregate loses to the index.** The best recent study (17,859 disclosure events, 2020–2025) finds that buying what Congress bought, on the day it became public, trailed the S&P 500 by about 5 percentage points over the next year. A minority of filers beat the market in any given year. The only sub-group with a documented edge is members who hold leadership posts, and even then you learn about the trade about a month late.
- **What was built.** A daily GitHub Action now pulls the official House, Senate and White House filings into `data/*.json`, and `trades.html` lets you filter by politician, ticker, chamber and time window, keep a watchlist, and see which tickers several members are buying or selling at once.

## 1. How disclosure works

The Stop Trading on Congressional Knowledge (STOCK) Act of 2012 applied insider-trading law explicitly to Congress and added the PTR requirement to the Ethics in Government Act. The Congressional Research Service explainer is the clearest primary reference ([CRS, "Stock Trading in Congress"](https://www.congress.gov/crs_external_products/TE/HTML/TE10073.html)).

| Rule | Detail |
| --- | --- |
| Who files | Members of the House and Senate, candidates, senior staff, the President, the Vice President and senior executive-branch officials. Trades by a spouse or dependent child are included. |
| What triggers a PTR | Any purchase, sale or exchange over $1,000 in stocks, bonds, options, futures and other securities. Widely held funds (mutual funds, ETFs) are exempt from PTRs, as are Treasuries in most cases. |
| Deadline | Within 30 days of being notified of the trade (for example a broker confirmation) and no later than 45 days after the trade date. |
| What is reported | Asset name, ticker where applicable, owner (self, spouse, dependent child, joint), transaction type, transaction date, notification date, and an amount bracket. House filers add a free-text description, which is where option strike and expiry details appear. |
| Amount brackets | $1,001–$15,000; $15,001–$50,000; $50,001–$100,000; $100,001–$250,000; $250,001–$500,000; $500,001–$1,000,000; $1,000,001–$5,000,000; $5,000,001–$25,000,000; $25,000,001–$50,000,000; over $50,000,000. Spouse and child assets above $1,000,000 may be reported as "Spouse/DC Over $1,000,000". |
| Penalty for late filing | $200, which is why late filings are common. In this repo's data 15% of House rows and 44% of Senate rows were filed more than 45 days after the trade date (the Senate figure is inflated by amendments to old reports and by large batch filings). |
| Where published | House: the Clerk's financial disclosure site, as PDFs plus a yearly tab-separated index. Senate: the eFD portal, as HTML tables (paper filings are scanned images). Executive branch: the Office of Government Ethics; the White House also posts the President's PTRs as scanned PDFs. |

**Where the lag comes from.** A trade on day 0 can legally appear on day 45. In practice the median gap in the 2025–2026 data is 28 days for the House and 35 days for the Senate. Whatever edge a politician has at the time of the trade, a copier gets a month later.

**Legislative status.** The House passed a ban on new stock purchases by members, spouses and dependent children 232–198 on 22 July 2026 ([Roll Call](https://rollcall.com/2026/07/22/congressional-stock-trading-bill-passes-the-house/)). The Senate failed to advance it 53–47 on 30 September 2026 because the House had attached a voter-ID provision ([24/7 Wall St](https://247wallst.com/investing/2026/10/01/the-senate-just-voted-down-a-ban-on-congressional-stock-trading/)). A ban would end new purchases but existing holdings and sales would still be reported, so the disclosure feed would not disappear.

## 2. Who to follow

### Nancy Pelosi (D-CA-11)

Everything reported under her name is owner "SP" (spouse): Paul Pelosi runs a venture and real-estate firm and places the trades. Pattern over 2025–2026, from the filings this repo parsed (39 transactions):

| Trade date | Filed | What | Bracket |
| --- | --- | --- | --- |
| 20 Dec 2024 | 17 Jan 2025 | Exercised 500 NVDA calls bought Nov 2023 (50,000 shares at a $12 strike); exercised 140 PANW calls | $500K–$1M; $1M–$5M |
| 31 Dec 2024 | 17 Jan 2025 | Sold 31,600 AAPL and 10,000 NVDA shares | $5M–$25M; $1M–$5M |
| 14 Jan 2025 | 17 Jan 2025 | Bought 50 calls each on GOOGL ($150), AMZN ($150), NVDA ($80), TEM ($20), VST ($50), all expiring 16 Jan 2026 | $50K–$1M each |
| 20 Jun 2025 | 9 Jul 2025 | Exercised 200 AVGO calls bought June 2024 (20,000 shares at $80) | $1M–$5M |
| 24–30 Dec 2025 | 23 Jan 2026 | Sold 45,000 AAPL, 20,000 AMZN, 20,000 NVDA, 10,000 DIS, 5,000 PYPL; donated AAPL and GOOGL shares to a donor-advised fund; bought 20 calls each on GOOGL, AMZN, AAPL, NVDA expiring Jan 2027 | up to $5M–$25M |
| 16 Jan 2026 | 23 Jan 2026 | Exercised the Jan 2025 calls on GOOGL, AMZN, NVDA, TEM, VST; bought 25,000 AB (AllianceBernstein) shares | $50K–$5M |
| 29 May 2026 | 23 Jun 2026 | Bought 200 INTC calls ($50 strike) and 200 UBER calls ($50 strike), both expiring 19 Mar 2027 | $1M–$5M; $500K–$1M |
| 24–28 Jul 2026 | 21 Aug 2026 | Bought 15,000 BE (Bloom Energy) shares and 200 BE calls ($100 strike, Jun 2027); 10,000 INTC shares and 50 more INTC calls | $250K–$5M per line |

Reading the pattern: she buys deep-in-the-money LEAPS (a $50 strike on Intel when the stock was far above it) and exercises them a year later, which is a leveraged, tax-deferred way to build a stock position. Her 2024 portfolio was up about 70.9% against 24.9% for the S&P 500 according to Unusual Whales' annual tally ([Motley Fool summary](https://www.fool.com/research/congressional-stock-trading-who-trades-and-makes-the-most/)). Trackers quote a ten-year cumulative return in the 800% range, but those figures are estimates built from bracket midpoints. Her 2026 disclosed volume is down to roughly $9M from about $49M in 2025 ([Kadoa tracker](https://www.kadoa.com/congress/filer/house_nancy_pelosi)). She announced in November 2025 that she will not seek re-election ([CBS News](https://www.cbsnews.com/news/nancy-pelosi-former-house-speaker-retire-congress/)); after 3 January 2027 her household's trades will no longer be public.

### Donald Trump (President)

Presidential PTRs (OGE Form 278-T) are posted at [whitehouse.gov/disclosures](https://www.whitehouse.gov/disclosures/); the repo lists 17 of them from August 2025 to September 2026. They are image scans without a text layer, so this project links them rather than parsing them. What press analyses of the PDFs show:

- Overwhelmingly municipal bonds: 807 positions worth $240.7M–$797.6M at the end of 2025 plus at least 243 purchases in 2026 worth $68.2M–$233.8M, over 1,000 positions in all, valued at $300M to $1B. 8,940 transactions between January 2025 and 29 June 2026 (5,772 purchases, 3,168 sales), filed in large batches ([CNBC, 29 Sep 2026](https://www.cnbc.com/2026/09/29/trump-municipal-bond-portfolio.html)).
- The March 2026 report held 175 transactions: corporate bonds of Nvidia, General Motors, Netflix and Boeing, plus apparent equity stakes in Bank of America and Wells Fargo worth roughly $130K–$300K combined with two other bank positions ([Bloomberg via Fortune, 25 Apr 2026](https://fortune.com/2026/04/25/trump-bond-purchases-ethics-disclosure-netflix-boeing-nvidia/)).
- The annual Form 278e released in June 2026 reported more than $580M of crypto-related income (World Liberty Financial token sales and related equity) and a Trump Media (DJT) stake valued over $50M ([CNBC, 30 Jun 2026](https://www.cnbc.com/2026/06/30/trump-financial-disclosure-released.html)).
- [Open Cabinet](https://open-cabinet.org/officials/trump-donald-j) hand-parses the executive-branch PDFs into rows (31,000+ through July 2026, an estimated $3.2B of volume, 73% flagged as late) and is the place to go for transaction-level detail.

The filings do not say who places the trades. For equity investors the useful reading is sector exposure (which issuers he lends to) and policy overlap, not individual stock picks.

### Everyone else

Volume and performance are different lists:

- **Most active in 2026** (this repo's data): Gilbert Cisneros (D-CA, 883 rows), Sen. Alan Armstrong (R-WY, 707), April McClain Delaney (D-MD, 339), Julia Letlow (R-LA, 257), Sen. John Boozman (R-AR, 202), Sen. David McCormick (R-PA, 200), Sen. Tommy Tuberville (R-AL, 193). Most of this is adviser-managed accounts rebalancing in $1K–$15K lots and carries no information. The Signals view counts distinct politicians per ticker precisely to wash this out.
- **Biggest traders by volume** (2025, Capitol Trades and Unusual Whales via [Motley Fool](https://www.fool.com/research/congressional-stock-trading-who-trades-and-makes-the-most/)): Jefferson Shreve (R-IN, about $151M), Sen. Richard Blumenthal (D-CT, about $86M, mostly spouse), Michael McCaul (R-TX, about $80M), Ro Khanna (D-CA, about $60M across 4,284 trades, almost all in family trusts). Sen. Cleo Fields (D-LA) and Josh Gottheimer (D-NJ) also feature.
- **Best 2025 returns** per Unusual Whales (same source): Warren Davidson (R-OH, +78.8%, from GE and GE Vernova), Donald Norcross (D-NJ, +70.8%), Terri Sewell (D-AL, +67.9%), Bryan Steil (R-WI, +62.5%), Sen. Alex Padilla (D-CA, +61.7%).
- **Largest single 2026 disclosures** in this repo's data: Sen. Jim Justice's sale of Greenbrier Hotel stock (over $50M, private), Jefferson Shreve's structured notes ($5M–$25M), Chip Roy's purchase of Atlas Energy Solutions (AESI, $5M–$25M, 30 Apr 2026), and Pelosi's December AAPL sales ($5M–$25M each).

A useful heuristic from the academic work below: weight trades by the filer's committee relevance and leadership role, by size relative to that filer's usual lot, and by whether several members bought the same name in the same month. Ignore dividend reinvestments, "professionally managed account" rows and anything under $15K.

## 3. Does copying them work? The evidence

| Study | Data | Finding |
| --- | --- | --- |
| Ziobrowski et al. (2004, 2011) | Senate 1993–1998, House 1985–2001 | Senators' portfolios beat the market by about 12 points a year, House members' by about 6. This is the origin of the "Congress beats the market" claim; it predates the STOCK Act. |
| Eggers and Hainmueller (2013), "Capitol Losses" | 2004–2008 | Members underperformed; they would have done better in index funds. |
| Belmont, Sacerdote, Sehgal and Van Hoek (2022), [Journal of Public Economics](https://www.sciencedirect.com/science/article/abs/pii/S0047272722000044) | STOCK Act era | No average abnormal returns for senators or House members; the pre-2012 edge is gone from the aggregate. |
| Wei and Zhou (Nov 2025), [NBER w34524, "Captain Gains on Capitol Hill"](https://www.nber.org/papers/w34524) | transaction level | Members who gain leadership positions earn roughly 47 points a year more than matched peers afterwards, through political influence (selling before regulatory actions, buying government contractors) and corporate access. |
| Equibles (2025), [17,859 disclosure events, Jan 2020–Aug 2025](https://equibles.com/research/what-happens-after-congress-buys-or-sells-a-stock-evidence-from-17-859-disclosures) | copy-trading simulation | Buying on the first close after a filing trailed the S&P 500 by 5.4 points over one year; sells trailed by 6.4. Only 43% of purchases beat the index. Median lag 28.5 days; using the true trade date instead of the filing date did not create an edge. |
| Unusual Whales annual reports (2024, 2025) | all disclosed portfolios | 2025: of 311 portfolios, about 32% beat the S&P 500's 16.6%; Democrats averaged 14.4%, Republicans 17.3%. Returns are estimated from bracket values at year start and end. |

Two funds let you own the idea without doing any of this: NANC (copies Democratic members' disclosures) and GOP, renamed from KRUZ in March 2025 (Republican members). As of 25 September 2026 NANC had about $288M in assets, a year-to-date return of 15.6% and a three-year annualised return of 25.3% ([Yahoo Finance](https://finance.yahoo.com/quote/NANC/)). NANC's outperformance is largely a large-cap tech tilt, which Pelosi-style holdings dominate.

**Practical conclusion.** Treat the feed as a watchlist generator and a conflict-of-interest lens, not a trading signal. The parts worth attention are (a) unusually large or option-leveraged trades by senior members, (b) clusters of distinct members buying the same stock in the same window, and (c) trades in sectors the filer's committee oversees. Position sizing cannot be inferred: a "$1M–$5M" bracket is the same line whether it is 1% or 30% of the filer's wealth.

## 4. Data sources compared

| Source | Cost | Coverage | Notes |
| --- | --- | --- | --- |
| House Clerk (disclosures-clerk.house.gov) | Free | House PTRs, same day they are accepted | Yearly ZIP with a tab-separated index; one PDF per filing. E-filed PDFs have a text layer and parse cleanly with `pdftotext -layout`; about 11% are paper scans. No CORS headers, so a browser page cannot read it directly. Used by this repo. |
| Senate eFD (efdsearch.senate.gov) | Free | Senate PTRs | Requires accepting a prohibition notice (one POST), then a JSON search endpoint and HTML report pages. Paper filings are images. Used by this repo. |
| White House disclosures / OGE | Free | President, VP, senior staff | PTRs are scanned PDFs; the annual 278e is also scanned. Open Cabinet parses them by hand. Metadata only in this repo. |
| unitedstates/congress-legislators | Free (public domain) | Party, state, district, bioguide IDs | Used for the party labels. |
| House/Senate Stock Watcher S3 datasets | Free | Historical | Both buckets now return 403; dead as of October 2026. |
| Capitol Trades | Free website | Both chambers, cleaned | No API and blocks automated requests. |
| Unusual Whales | Website, paid tiers | Both chambers plus performance estimates | Source of the annual reports; no open API. |
| Quiver Quantitative API | Hobbyist about $30/month, Trader $75/month | Both chambers, holdings, net worth, lobbying, contracts | No free API tier; the website subscription does not include API access ([Quiver](https://www.quiverquant.com/api/)). |
| Finnhub `/stock/congressional-trading` | API key required; tier not confirmed | Per-ticker | Endpoint exists (returns 401 without a key) but is per symbol, not per politician. |
| Financial Modeling Prep | API key; plans restructured in 2025 | `senate-trades`, `house-disclosure` endpoints | Not verified here (site blocks scripted fetches). |

Why this repo scrapes the primary sources: it is the only route that is free, has no key to leak from a static site, and has no terms-of-service problem. The cost is parsing PDFs, which turned out to be reliable for e-filed reports.

## 5. What was built

- **`scripts/fetch_trades.py`** (standard library only, needs `pdftotext`). Downloads the Clerk's yearly index, fetches each new House PTR PDF, converts it to text and parses the transaction table (owner, asset, ticker, asset-type code, type, dates, bracket, description, account). Accepts the Senate portal's notice, pages through its PTR search for the year and parses each report's HTML table. Lists the President's PTRs. Joins party and state from congress-legislators. Incremental: a filing already in the output is skipped.
- **`data/`**: `house-2025.json`, `house-2026.json`, `senate-2025.json`, `senate-2026.json`, `president.json`, `index.json`. First run on 4 October 2026:

  | File | Filings | Transactions | Paper scans (unparsed) |
  | --- | --- | --- | --- |
  | house-2025 | 515 | 7,667 | 66 |
  | house-2026 | 407 | 3,414 | 47 |
  | senate-2025 | 141 | 754 | 21 |
  | senate-2026 | 128 | 1,572 | 9 |

  Every filing matched a sitting member for party and state. The House row count equals the number of filing-status labels in the PDFs, so no transaction rows were dropped by the parser.
- **`.github/workflows/update-trades.yml`**: daily at 14:17 UTC and on demand; commits changed JSON to the branch, which redeploys the Pages site.
- **`trades.html`**: search by politician, ticker or asset; chips for watchlist, buys only, stocks-and-options only, House or Senate; time window by filing date; year filter. Signals tab aggregates the current selection: most bought and most sold by distinct buyers and sellers, most active filers, largest disclosures. President tab lists the White House PTRs with the press-reported facts. How-it-works tab carries the rules, the evidence and the data-source notes.

Limitations: no price data, so no "what happened next" column yet; scanned filings (about 10% of House, under 10% of Senate) are linked but empty; option details come from free-text descriptions and parse for House rows and Senate "Stock Option" rows only; the President's rows are not parsed; "late" is measured from the trade date rather than the notification date the law uses.

## 6. Next steps worth doing

1. **Price overlay and backtest.** Add daily closes (Stooq is free and keyless) so each disclosure shows the return since filing versus the S&P 500, and the Signals tab can be checked against the Equibles finding on this very data.
2. **Alerts.** A step in the workflow that diffs `data/` and sends a push or email when a watchlist name files (the IFTTT or Gmail connectors would do), since the value of a Pelosi filing is highest in the first hours.
3. **OCR for scans.** `tesseract` on the paper House and Senate filings and on the President's 278-T PDFs would close the coverage gap.
4. **Better de-noising.** Flag rows whose description says "professionally managed", "dividend reinvestment" or "automatic", and hide them by default.
5. **Committee overlay.** Join the `committee-membership-current` file from congress-legislators to flag trades in sectors the filer's committees oversee, the one factor the academic work says matters.

## Sources

- CRS, [Stock Trading in Congress](https://www.congress.gov/crs_external_products/TE/HTML/TE10073.html)
- Senate Select Committee on Ethics, [Financial Disclosure](https://www.ethics.senate.gov/public/index.cfm/financialdisclosure)
- Roll Call, [Congressional stock-trading bill passes the House](https://rollcall.com/2026/07/22/congressional-stock-trading-bill-passes-the-house/) (22 Jul 2026)
- 24/7 Wall St, [The Senate just voted down a ban on congressional stock trading](https://247wallst.com/investing/2026/10/01/the-senate-just-voted-down-a-ban-on-congressional-stock-trading/) (1 Oct 2026)
- CBS News, [Nancy Pelosi to retire from Congress after this term](https://www.cbsnews.com/news/nancy-pelosi-former-house-speaker-retire-congress/)
- Yahoo Finance, [Nancy Pelosi discloses new stock trades](https://finance.yahoo.com/markets/options/articles/nancy-pelosi-discloses-stock-trades-133103278.html)
- Polytick, [Nancy Pelosi recent stock trades 2026](https://www.polytick.us/blog/nancy-pelosi-best-stock-trades-2026-analysis)
- CNBC, [Trump's municipal bond portfolio reaches as much as $1 billion](https://www.cnbc.com/2026/09/29/trump-municipal-bond-portfolio.html) (29 Sep 2026)
- Fortune/Bloomberg, [Trump reports flurry of March bond purchases](https://fortune.com/2026/04/25/trump-bond-purchases-ethics-disclosure-netflix-boeing-nvidia/) (25 Apr 2026)
- CNBC, [Trump's annual financial disclosure shows more than $580M in crypto-related income](https://www.cnbc.com/2026/06/30/trump-financial-disclosure-released.html) (30 Jun 2026)
- Open Cabinet, [Donald J. Trump financial trades](https://open-cabinet.org/officials/trump-donald-j)
- Motley Fool, [Congressional stock trading: who trades the most](https://www.fool.com/research/congressional-stock-trading-who-trades-and-makes-the-most/)
- Equibles, [What happens after Congress buys or sells a stock](https://equibles.com/research/what-happens-after-congress-buys-or-sells-a-stock-evidence-from-17-859-disclosures)
- Wei and Zhou, [“Captain Gains” on Capitol Hill, NBER w34524](https://www.nber.org/papers/w34524)
- Belmont et al., [Do senators and house members beat the stock market? Evidence from the STOCK Act](https://www.sciencedirect.com/science/article/abs/pii/S0047272722000044)
- Yahoo Finance, [NANC](https://finance.yahoo.com/quote/NANC/), [KRUZ/GOP](https://finance.yahoo.com/quote/KRUZ/)
- Quiver Quantitative, [API](https://www.quiverquant.com/api/)
- House Clerk, [asset type codes](https://fd.house.gov/reference/asset-type-codes.aspx)
