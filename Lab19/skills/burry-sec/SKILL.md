---
name: burry-sec
description: Apply Burry's cash-versus-earnings and liabilities checks to shared SEC annual facts and write a skeptical Lab 19 business memo. Use for Burry panel analysis, not trading or price targets.
---

# Burry business screen

From the course repository run `python panel.py TICKER`, supplying the user's
authorized SEC contact information in `SEC_USER_AGENT`, or `--facts PATH` to
use the same saved snapshot as the other investors. Read `Lab19/output/TICKER.md`.
Do not substitute different facts or period rules for your persona.

The bundled `scripts/checks.py` computes whether operating cash flow is at least
net income in every annual period, and whether latest liabilities are at most
twice equity. Require five years for the annual check. Missing inputs yield
`not known`; nonpositive equity makes the leverage check `not known`.
Never substitute zero for absent capital spending or other facts.

Write `Lab19/memos/TICKER/Burry.md` as a short Burry-inspired educational memo,
with `**Verdict: own the business.**`, `**Verdict: watch it.**`, or
`**Verdict: pass.**`. Focus on cash backing, balance-sheet vulnerability, and
the strongest evidence-based bear case. Passing these narrow checks does not
prove clean accounting. A cash shortfall alone does not prove fraud; identify
what further investigation would resolve the concern. Do not claim to have
read footnotes that were not provided. Use only script-printed numbers, in the
same units, and no price targets, valuation, forecasts, or alleged holdings.

Run `panel.py TICKER --facts PATH --check-memos`; fix every unsupported number
and manually verify its metric and fiscal year. Do not fabricate a partner exchange.

Reading: https://github.com/CinderZhang/FAskills/blob/main/financial-researcher/experts/michael_burry.md
Use this page as philosophy only; the lab's rules override its broader requests.
Never install FAskills or use its paid data services.
