# Lab 19 - Legend Panel

## Question and build request

When investor skills read the same annual facts, where do they agree, where
do they split, and would I trust the panel?

AI-assisted request: extend the working Lab 18 app with Graham and Burry skills,
preserve Buffett and the original view, and compute all checks from a shared SEC
snapshot. Add current assets/current liabilities and their ratio, retain the
liabilities/equity rule, compare the panel against COST, and run SOXX's largest
holding. Show separate model-written verdicts and memos, check every memo's
numeric literals, and test Graham's threshold without changing source facts.

## Run

```powershell
cd C:\Users\pmeix\FIN43900-Fall2026
.\.venv\Scripts\python.exe -m streamlit run buffett_app.py
```

The app defaults to the panel. Uncheck **Show Graham and Burry panel** for the
original Lab 18 view. Use COST or AMD in the ticker box. Saved SEC snapshots
work without new network requests or re-entering contact details. Other tickers
can use Download from SEC with the student's authorized name/email.

```powershell
.\.venv\Scripts\python.exe panel.py COST --facts Lab18/output/COST-companyfacts.json --check-memos
.\.venv\Scripts\python.exe panel.py AMD --facts Lab19/output/AMD-companyfacts.json --check-memos
.\.venv\Scripts\python.exe validate_lab19.py
```

Install dependencies from `requirements-lab18.txt` in a new environment.

## Skills, facts, and provenance

The installed skills are `.agents/skills/buffett-sec`, `graham-sec`, and
`burry-sec`. Submission copies live in `Lab18/buffett-sec` and `Lab19/skills`.
The new skills bundle their check scripts and route to `panel.py` for shared
facts. If installed skills exist, the panel uses those; otherwise it uses the
submission copies. Keep these copies synchronized when editing a skill.

The shared engine reuses the Lab 18 annual extraction without modifying its
calculations. Current assets use `AssetsCurrent`; current liabilities use
`LiabilitiesCurrent`; total liabilities use `Liabilities`. Fiscal-year-end
dates, annual flows, preferred tags, 10-K-only eligibility, latest filing,
year-end equity, and missing-value handling remain the same as Lab 18.
Current ratio is not known when either input is missing or current liabilities
are nonpositive. Comparisons use full precision; displays round ratios.

The facts are latest-restated values, not values known at a historical trading
date. COST reuses the November 3 SEC snapshot; AMD was downloaded November 5.
Every extracted value has its tag and filing provenance in the printed report.

Reading, not installed software or financial data services:

- [Graham's assigned page](https://github.com/CinderZhang/FAskills/blob/main/financial-researcher/experts/ben_graham.md)
- [Burry's assigned page](https://github.com/CinderZhang/FAskills/blob/main/financial-researcher/experts/michael_burry.md)
- [Buffett's assigned page](https://github.com/CinderZhang/FAskills/blob/main/financial-researcher/experts/warren_buffett.md)

Graham emphasizes defensive liquidity and earnings evidence; Burry emphasizes
cash backing and skeptical investigation. The lab supplies narrower checks
than their complete philosophies. No price, valuation, or prediction is added.

## COST verification

| Fiscal year end | Current ratio | Liabilities / equity |
|---|---:|---:|
| 2022-08-28 | 1.02 | 2.11 |
| 2023-09-03 | 1.07 | 1.75 |
| 2024-09-01 | 0.97 | 1.96 |
| 2025-08-31 | 1.03 | 1.64 |
| 2026-08-30 | 1.06 | 1.49 |

| Investor | Check | Result |
|---|---|---|
| Buffett | ROE at least 15% every year | pass |
| Buffett | Owner earnings positive every year | pass |
| Buffett | Owner earnings grew, first to last | pass |
| Graham | Latest current ratio at least 2.0 | fail |
| Graham | Net income positive every year | pass |
| Graham | Net income grew, first to last | pass |
| Burry | Operating cash flow at least net income every year | pass |
| Burry | Latest liabilities no more than twice equity | pass |

All values and checks match: **Buffett 3/3, Graham 2/3, Burry 2/2**.
See [computed report](Lab19/output/COST.md) and [executed validation](Lab19-validation.txt).
The old COST benchmark and JPM missing-value behavior are also preserved.

### Threshold probe

The validation changed `current_ratio_threshold = 2.0` to `1.0` in an isolated
copy of Graham's actual skill text, then passed that skill to the same engine.
Graham changed from 2/3 to 3/3 on COST; Buffett and Burry were unchanged.
The retained installed threshold is **2.0**, preserving a defensive liquidity
cushion rather than adjusting it merely to approve Costco. This line is also
under each Graham memo. A threshold change alters the check, not the business.

To repeat manually, change the line in the installed Graham SKILL.md and rerun
the panel; restore the retained threshold afterward. Memos are saved judgments,
not automatic rewrites when thresholds change. The app warns when the report
fingerprint differs from the report used for a memo.

## Company selection and result

Using **SOXX**, a fund in the Lab 15 Project 2 universe, the issuer's
[holdings CSV](https://www.ishares.com/us/products/239705/ishares-semiconductor-etf/latest-holdings.csv)
dated **November 3, 2026** lists **AMD at 8.98%**, the largest equity holding,
ahead of NVDA at 8.18%. The source was checked November 5. Here "largest"
means largest fund holding by portfolio weight. AMD files 10-Ks, so no fallback
company was needed. This selection was made during the lab, not claimed as
completed student prework.

The [AMD computed report](Lab19/output/AMD.md) covers fiscal years ending
2021-12-25 through 2025-12-27.

| Investor | Checks | Memo verdict | Main reason |
|---|---|---|---|
| Buffett | 2 pass, 1 fail | watch it | ROE fails the annual threshold despite positive, growing endpoint owner earnings |
| Graham | 3 pass | own the business, provisionally | Current ratio 2.85; positive net income throughout and higher endpoint income |
| Burry | 1 pass, 1 not known | watch it | Cash flow covers income, but total liabilities are missing under the required tag |

AMD's total liabilities remain **not found**, and liabilities/equity and Burry's
leverage check remain **not known**. No subtraction from assets or alternative
tag was used to fill the gap. That is an extraction limitation, not a claim
that AMD has no liabilities. Buffett's ROE values are 42.2%, 2.4%, 1.5%, 2.9%,
and 6.9%; Graham's current ratios are 2.02, 2.36, 2.51, 2.62, and 2.85.

## Memos and numeric checks

| Company | Buffett | Graham | Burry |
|---|---|---|---|
| COST | [watch it](Lab19/memos/COST/Buffett.md) | [pass](Lab19/memos/COST/Graham.md) | [watch it](Lab19/memos/COST/Burry.md) |
| AMD | [watch it](Lab19/memos/AMD/Buffett.md) | [own the business](Lab19/memos/AMD/Graham.md) | [watch it](Lab19/memos/AMD/Burry.md) |

All numeric literals in all six memos appear in the corresponding printed
report. Automated UI tests inserted `40.0%` into each investor's memo in turn;
every column flagged it. The injected values were not saved. These flags do
not prove correct attribution, units, or qualitative conclusions, and do not
parse quantities spelled out as words. Verdicts are model judgments, not a
mechanical translation of pass counts or opinions from the actual investors.

## Code explanation preparation

Open `Lab19/skills/graham-sec/scripts/checks.py`, function `checks`:

1. `latest_ratio` selects the last annual row's ratio; with no rows it is `None`.
2. `income` collects annual net income values in chronological order.
3. `liquidity` is `not known` if the ratio is missing; otherwise it compares the
   full-precision ratio with the threshold and returns `pass` or `fail`.
4. The next `if` requires five income values and checks for missing observations.
5. If incomplete, `positive` is `not known`; otherwise `all(value > 0 ...)`
   determines whether every year has positive net income.
6. The growth `if` requires five rows and both endpoint incomes. Intermediate
   missing income affects the every-year check but is not an input to endpoint growth.
7. The growth comparison requires the last value to be strictly greater than
   the first; equality fails.
8. The returned dictionary gives each check its descriptive name and status.

Practice question: "What happens when an input is missing?" Answer: the code
tests for `None` before comparison and reports `not known` for any check that
requires that missing input; it never silently substitutes zero.

This is preparation, not a claim of a completed partner explanation.

## Prepared bull and bear arguments on AMD

**Bull, two sentences:** AMD passes Graham's liquidity and earnings checks,
with a latest current ratio of 2.85 and positive net income throughout the
period. Operating cash flow covers net income in every year and owner earnings
rise from 3,220 to 6,735 between endpoints, supporting further business research.

**Bear, two sentences:** AMD fails Buffett's consistent-ROE test, and the
owner-earnings path drops to 1,121 before recovering, so endpoint growth hides
volatility. Burry's leverage check is not known because the required liabilities
input is missing, so the panel cannot establish that balance-sheet condition.

These are prepared arguments for the partner exchange; actual completion has
not been reported.

## Proposed decision

Only with a condition: use the panel to prioritize research, retain missing
checks as not known, and resolve AMD's liabilities gap and investigate its
inconsistent ROE before allowing the screen to influence portfolio holdings;
do not treat a majority of passes as a buy signal.

The same line is displayed in the app from [decision.md](Lab19/decision.md).

## Learn and reflect

A panel applies different decision rules and perspectives to common evidence.
Here the skills run sequentially against one shared report; they are not
independent data sources or votes by the actual investors. Agreement is not
independent confirmation because all share the same extraction and its limits.

On AMD, the positive earnings and cash-flow evidence supports further research
across the panel. Graham is more favorable because liquidity and earnings pass
his checks; Buffett focuses on inconsistent ROE, and Burry cannot clear leverage.
The COST threshold probe shows that a screen's verdict depends partly on a
chosen policy. Standards should be justified in advance, not adjusted to fit
a preferred company.

## Checkout

Technical build, COST verification, AMD run, memo flags, and threshold probe are
complete. The student still needs to adopt or revise the proposed decision,
complete the partner code explanation and bull/bear exchange, and submit links.

Upload `buffett_app.py`, `panel_app.py`, `panel.py`, `validate_lab19.py`,
`requirements-lab18.txt`, `Lab19.md`, `Lab19-validation.txt`, and the entire
`Lab18` and `Lab19` folders (excluding `__pycache__`). Preserve nested folders.
Include `.agents/skills` to preserve installed discovery, or copy the provided
skill folders into `.agents/skills` after downloading the repository.
