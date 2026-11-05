"""Lab 18 Streamlit viewer. Code computes; a saved model-written memo judges."""
from datetime import date
import importlib.util
import json
import os
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent
SCRIPT = ROOT / "Lab18/buffett-sec/scripts/buffett_facts.py"
spec = importlib.util.spec_from_file_location("buffett_facts", SCRIPT)
engine = importlib.util.module_from_spec(spec)
spec.loader.exec_module(engine)
OUTPUT = ROOT / "Lab18/output"
MEMOS = ROOT / "Lab18/memos"


@st.cache_data(ttl=3600, show_spinner=False)
def live_report(ticker, user_agent, day):
    facts, source = engine.download_facts(ticker, user_agent, OUTPUT)
    report = engine.build_report(facts, ticker, source)
    engine.save_report(report, OUTPUT)
    return report


def main():
    st.set_page_config(page_title="Buffett Business Review", layout="wide")
    if st.sidebar.checkbox("Show Graham and Burry panel", value=True):
        import panel_app
        panel_app.show()
        return
    st.title("Buffett Business Review")
    st.caption("Data from SEC EDGAR; built with AI help, a learning demonstration, not investment advice.")
    ticker = st.sidebar.text_input("Ticker", "COST").strip().upper()
    mode = st.sidebar.radio("Data", ["Saved SEC snapshot", "Download from SEC"])
    contact = st.sidebar.text_input("SEC User-Agent: your name and email", value=os.environ.get("SEC_USER_AGENT", ""), type="password")
    if not engine.re.fullmatch(r"[A-Z0-9.-]+", ticker):
        st.error("Enter a valid ticker.")
        return
    try:
        if mode == "Download from SEC":
            report = live_report(ticker, contact, date.today())
        else:
            path = OUTPUT / f"{ticker}-companyfacts.json"
            if not path.exists():
                st.info("No saved SEC download for this ticker. Supply your SEC contact information and select Download from SEC.")
                return
            source_path = OUTPUT / f"{ticker}-source.json"
            source = json.loads(source_path.read_text(encoding="utf-8")) if source_path.exists() else {"local_snapshot": path.name}
            report = engine.build_report(json.loads(path.read_text(encoding="utf-8")), ticker, source)
        printed = engine.render_report(report)
    except Exception as error:
        st.error(f"{ticker}: {error}")
        return
    st.subheader(f"{ticker} — {report['company']}")
    st.caption(f"Download provenance: {report['source']}")
    if len(report["rows"]) != 5:
        st.warning("Fewer than five annual periods were found; the full screening checks are not known.")
    chart = pd.DataFrame([{"FY end": pd.Timestamp(row["fiscal_year_end"]),
                           "Owner earnings": row["owner_earnings"] / 1e6 if row["owner_earnings"] is not None else None,
                           "Net income": row["net_income"]["value"] / 1e6 if row["net_income"]["value"] is not None else None}
                          for row in report["rows"]])
    if not chart.empty:
        st.write("Annual earnings — USD millions")
        st.line_chart(chart.set_index("FY end"))
    st.markdown(printed.split("XBRL provenance")[0])
    with st.expander("XBRL tags, filing dates, and accessions"):
        st.markdown(printed.split("XBRL provenance")[1])
    st.subheader("Model-written business memo")
    memo_path = MEMOS / f"{ticker}.md"
    saved = memo_path.read_text(encoding="utf-8") if memo_path.exists() else ""
    memo = st.text_area("Memo text — edit here to test a number", value=saved, height=280,
                        key=f"memo-{ticker}-{saved}")
    if not memo:
        st.info("Run the buffett-sec skill for this ticker to create its memo. The app computes facts but does not fabricate a model judgment.")
    else:
        st.markdown(memo)
        flags = engine.unsupported_numbers(memo, printed)
        if flags:
            st.error("Unsupported numbers: " + "; ".join(f"{item['number']} (line {item['line']})" for item in flags))
        else:
            st.success("Every numeric literal in this memo appears in the script's printed report.")
        st.caption("This checks numeric literals, including percentages; it cannot establish that a permitted number is attached to the correct metric or year. Keep USD amounts in millions, as printed. Edits here are temporary unless saved.")
        if st.button("Save memo"):
            MEMOS.mkdir(parents=True, exist_ok=True)
            memo_path.write_text(memo, encoding="utf-8")
            st.success("Memo saved.")
    decision = ROOT / "Lab18/COST-decision.md"
    if ticker == "COST" and decision.exists():
        st.markdown(decision.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
