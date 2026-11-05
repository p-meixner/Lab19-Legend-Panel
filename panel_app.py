"""Panel view embedded in the existing Lab 18 app."""
from datetime import date
import hashlib
import json
import os

import pandas as pd
import streamlit as st
import panel

ROOT = panel.ROOT
OUTPUT = ROOT / "Lab19/output"
MEMOS = ROOT / "Lab19/memos"


@st.cache_data(ttl=3600, show_spinner=False)
def download(ticker, contact, day):
    return panel.base.download_facts(ticker, contact, OUTPUT)


def show():
    st.title("Legend Investor Panel")
    st.caption("Data from SEC EDGAR; built with AI help, a learning demonstration, not investment advice.")
    ticker = st.sidebar.text_input("Ticker", "COST").strip().upper()
    mode = st.sidebar.radio("Data", ["Saved SEC snapshot", "Download from SEC"])
    contact = st.sidebar.text_input("SEC User-Agent: your name and email", value=os.environ.get("SEC_USER_AGENT", ""), type="password")
    if not panel.re.fullmatch(r"[A-Z0-9.-]+", ticker):
        st.error("Enter a valid ticker.")
        return
    try:
        if mode == "Download from SEC":
            facts, source = download(ticker, contact, date.today())
        else:
            path = OUTPUT / f"{ticker}-companyfacts.json"
            if not path.exists():
                path = ROOT / "Lab18/output" / path.name
            if not path.exists():
                st.info("No saved SEC snapshot. Supply SEC contact information and select Download from SEC.")
                return
            facts = json.loads(path.read_text(encoding="utf-8"))
            source_path = path.with_name(f"{ticker}-source.json")
            source = json.loads(source_path.read_text(encoding="utf-8")) if source_path.exists() else {"local_snapshot": str(path)}
        report = panel.build_report(facts, ticker, source)
        printed = panel.render_report(report)
    except Exception as error:
        st.error(f"{ticker}: {error}")
        return
    st.subheader(f"{ticker} — {report['company']}")
    st.caption(f"SEC snapshot downloaded: {source.get('downloaded_utc', 'not recorded')}. All investors use the same facts. Latest-restated analysis; not a historical trading vintage.")
    if len(report["rows"]) != 5:
        st.warning("Fewer than five annual periods found. Multi-year checks remain not known.")
    chart = pd.DataFrame([{"FY end": pd.Timestamp(row["fiscal_year_end"]),
                           "Owner earnings": row["owner_earnings"] / 1e6 if row["owner_earnings"] is not None else None,
                           "Net income": row["net_income"]["value"] / 1e6 if row["net_income"]["value"] is not None else None}
                          for row in report["rows"]])
    if not chart.empty:
        st.write("Annual earnings — USD millions")
        st.line_chart(chart.set_index("FY end"))
    st.markdown(printed.split("XBRL provenance")[0])
    st.markdown(printed.split("## Liquidity and liabilities")[1].split("## Panel checks")[0])
    with st.expander("XBRL tags and filing provenance"):
        st.markdown(printed.split("XBRL provenance")[1].split("## Liquidity and liabilities")[0])
    st.subheader("Panel checks")
    check_rows = [{"Investor": investor, "Check": name, "Result": result}
                  for investor, checks in report["panel"].items() for name, result in checks.items()]
    st.dataframe(pd.DataFrame(check_rows), hide_index=True)
    st.caption(f"Graham's skill threshold is {report['graham_threshold']:.1f}. Checks compare full-precision ratios; the display rounds to two decimals.")
    st.subheader("Investor verdicts and memos")
    summaries = []
    fingerprint = hashlib.sha256(printed.encode()).hexdigest()
    for column, (investor, checks) in zip(st.columns(3), report["panel"].items()):
        with column:
            st.markdown(f"### {investor}")
            st.write(f"{sum(value == 'pass' for value in checks.values())} of {len(checks)} checks pass")
            memo_path = MEMOS / ticker / f"{investor}.md"
            saved = memo_path.read_text(encoding="utf-8") if memo_path.exists() else ""
            if not saved and investor == "Buffett":
                old = ROOT / "Lab18/memos" / f"{ticker}.md"
                saved = old.read_text(encoding="utf-8") if old.exists() else ""
            memo = st.text_area(f"{investor} memo — edit to test", saved, height=230,
                                key=f"panel-memo-{ticker}-{investor}-{saved}")
            verdict = panel.verdict(memo)
            st.write(f"Verdict: {verdict}")
            summaries.append({"Investor": investor, "Verdict": verdict})
            if not memo:
                st.info(f"Run the {investor} skill to write a memo from this printed report.")
                continue
            st.markdown(memo)
            flags = panel.base.unsupported_numbers(memo, printed)
            if flags:
                st.error(f"{investor} unsupported numbers: " + "; ".join(f"{item['number']} (line {item['line']})" for item in flags))
            else:
                st.success(f"{investor}: no unprinted numeric literals.")
            metadata = memo_path.with_suffix(".json")
            recorded = json.loads(metadata.read_text(encoding="utf-8")) if metadata.exists() else {}
            if recorded.get("report_sha256") != fingerprint:
                st.warning("This memo has not been recorded against the current report and threshold. Review before relying on it.")
            if st.button(f"Save {investor} memo"):
                memo_path.parent.mkdir(parents=True, exist_ok=True)
                memo_path.write_text(memo, encoding="utf-8")
                metadata.write_text(json.dumps({"report_sha256": fingerprint}, indent=2), encoding="utf-8")
                st.success("Memo saved against the current report.")
    st.dataframe(pd.DataFrame(summaries), hide_index=True)
    st.caption("Numbers are checked across every memo. The check detects unprinted numeric literals, not incorrect labels, units, written-out quantities, or unsupported qualitative claims. Memos are model judgments, not votes from the actual investors.")
    decision = ROOT / "Lab19/decision.md"
    if decision.exists():
        st.markdown(decision.read_text(encoding="utf-8"))


if __name__ == "__main__":
    st.set_page_config(page_title="Legend Investor Panel", layout="wide")
    show()
