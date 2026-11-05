"""Burry's deterministic checks on shared annual rows."""


def checks(rows):
    pairs = [(row["operating_cash_flow"]["value"], row["net_income"]["value"]) for row in rows]
    if len(pairs) != 5 or any(cash is None or income is None for cash, income in pairs):
        backing = "not known"
    else:
        backing = "pass" if all(cash >= income for cash, income in pairs) else "fail"
    leverage = rows[-1]["liabilities_to_equity"] if rows else None
    return {"Operating cash flow at least net income every year": backing,
            "Liabilities no more than twice equity, latest year":
                "not known" if leverage is None else "pass" if leverage <= 2 else "fail"}
