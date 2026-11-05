"""Graham's deterministic checks on shared annual rows."""
from pathlib import Path
import math
import re


def threshold(skill_path=None):
    path = Path(skill_path) if skill_path else Path(__file__).resolve().parents[1] / "SKILL.md"
    match = re.search(r"^current_ratio_threshold\s*=\s*(\d+(?:\.\d+)?)\s*$", path.read_text(encoding="utf-8"), re.M)
    if not match:
        raise ValueError("Graham skill must specify current_ratio_threshold.")
    value = float(match.group(1))
    if not math.isfinite(value) or value <= 0:
        raise ValueError("Graham threshold must be positive and finite.")
    return value


def checks(rows, minimum):
    latest_ratio = rows[-1]["current_ratio"] if rows else None
    income = [row["net_income"]["value"] for row in rows]
    liquidity = "not known" if latest_ratio is None else "pass" if latest_ratio >= minimum else "fail"
    if len(income) != 5 or any(value is None for value in income):
        positive = "not known"
    else:
        positive = "pass" if all(value > 0 for value in income) else "fail"
    if len(income) != 5 or income[0] is None or income[-1] is None:
        growth = "not known"
    else:
        growth = "pass" if income[-1] > income[0] else "fail"
    return {f"Current ratio at least {minimum:.1f}, latest year": liquidity,
            "Net income positive every year": positive,
            "Net income grew, first year to last": growth}
