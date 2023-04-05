import streamlit as st


def st_header():
    st.set_page_config(
        page_title="Data Quality Score",
        page_icon="👋",
        layout="wide",
    )

    st.markdown(
        """<style>
        .block-container {
            padding-top: 0rem;
        }
        .stPlotlyChart {
            height: 12.5rem
        }
        </style>""",
        unsafe_allow_html=True,
    )
    
    
def felicitation():
    st.balloons()