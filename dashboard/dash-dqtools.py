
import streamlit as st
import duckdb
from utils import dqtools

st.set_page_config(layout="wide")
conn = duckdb.connect("dashboard/dq_mart.duckdb")

st.markdown(
    """<style>
    .block-container {
        padding-top: 0rem;
    }
    .stPlotlyChart {
        height: 12.5rem
    }
    </style>""",
    unsafe_allow_html=True
)

# Overall Scores
dqtools.add_overall_statistics(conn)

# KPI Cards
dqtools.add_kpi_cards(conn)

# Overtime Score
dqtools.add_overtime_score(conn)