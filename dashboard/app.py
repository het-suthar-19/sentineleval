import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

import json

import streamlit as st

from eval.run_eval import run_full_eval


BASE_DIR = os.path.dirname(__file__)
RESULTS_PATH = os.path.abspath(os.path.join(BASE_DIR, "..", "results", "eval_results.json"))
DEFAULT_SYSTEM_PROMPT = (
    "You are a customer support assistant for a software company. Be helpful, professional, concise, and focused on resolving customer issues."
)


st.title("Evaluation Dashboard")


def render_results(results: list[dict]) -> None:
    total_tests = len(results)
    passed_tests = sum(1 for result in results if result.get("passed"))
    pass_rate = (passed_tests / total_tests * 100) if total_tests else 0.0

    st.metric("Total Tests", total_tests)
    st.metric("Pass Rate", f"{pass_rate:.1f}%")

    st.subheader("All Results")
    st.dataframe(results, use_container_width=True)

    failed_cases = [
        {
            "test_case": result.get("test_case", ""),
            "reason": result.get("reason", ""),
        }
        for result in results
        if not result.get("passed", False)
    ]

    st.subheader("Failed Cases")
    if failed_cases:
        st.dataframe(failed_cases, use_container_width=True)
    else:
        st.success("No failed cases.")


test_case_count = st.text_input("Number of test cases", value="10")
system_prompt = st.text_area("Custom system prompt", value=DEFAULT_SYSTEM_PROMPT, height=150)
run_clicked = st.button("Run Evaluation")

if run_clicked:
    try:
        n = int(test_case_count)
    except ValueError:
        st.error("Please enter a valid integer for the number of test cases.")
        st.stop()

    with st.spinner("Running evaluation..."):
        results = run_full_eval(n, system_prompt=system_prompt)
    st.session_state["latest_results"] = results
elif os.path.exists(RESULTS_PATH):
    with open(RESULTS_PATH, "r", encoding="utf-8") as file_handle:
        results = json.load(file_handle)
else:
    st.error(f"Results file not found: {RESULTS_PATH}")
    st.stop()

render_results(results)
