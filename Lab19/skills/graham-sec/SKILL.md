---
name: graham-sec
description: Apply Graham's defensive liquidity and earnings checks to the shared SEC annual facts and write a grounded Lab 19 business memo. Use for Graham panel analysis, not price valuation.
---

# Graham business screen

current_ratio_threshold = 2.0

The assignment's liquidity threshold above is executable configuration: the
bundled `scripts/checks.py` reads it. For the probe, change it to 1.0, rerun,
record the result, then restore the chosen threshold. Do not tune it to obtain
a desired verdict. A threshold change requires reconsidering the saved memo.

From the course repository run `python panel.py TICKER` with the user's
authorized name/email in `SEC_USER_AGENT`, or pass `--facts PATH` for an existing
SEC snapshot. Use the shared report at `Lab19/output/TICKER.md`, not another
download or a different period definition for your own analysis.

Code computes current assets / current liabilities (positive denominator only),
latest-year current ratio versus the threshold, positive net income every year,
and net income growth from first to last year. Require five years for the
multi-year checks. Missing required inputs yield `not known`, not a guess.
Keep all Lab 18 tag, period, filing, and nonpositive-equity rules.

Read the printed report; write `Lab19/memos/TICKER/Graham.md` with
`**Verdict: own the business.**`, `**Verdict: watch it.**`, or
`**Verdict: pass.**` and a short Graham-inspired educational judgment.
Emphasize liquidity protection and demonstrated earnings, not an optimistic
growth story. A failed liquidity screen need not mean imminent insolvency.
Use only printed numbers in their printed units. Do not invent valuations,
price comparisons, dividends, forecasts, or claimed investor holdings.
The lab's checks are a narrow adaptation of the reading, not Graham's full system.
End with one line recording the retained threshold and its rationale.

Validate every memo number with `panel.py TICKER --facts PATH --check-memos`.
The number flag does not verify semantic attribution; check each metric/year.
Do not present a fictional partner discussion as completed.

Reading: https://github.com/CinderZhang/FAskills/blob/main/financial-researcher/experts/ben_graham.md
Read only; never install FAskills or use its data services.
