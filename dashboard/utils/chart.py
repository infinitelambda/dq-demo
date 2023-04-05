from utils import db
import streamlit as st
import plotly.graph_objects as go


def get_color(value):
    if value < 50:
        return "#ff4136"  # red
    if value < 70:
        return "orange"
    if value < 90:
        return "yellow"
    return "#3d9970"  # green


def add_overall_statistics():
    data = db.get_overall_statistics_data()
    figs = [
        go.Figure(
            [
                go.Indicator(
                    mode="number+delta",
                    title="Data Quality Score",
                    value=data["score"],
                    domain=dict(row=0, column=0),
                    delta=dict(reference=data["score_prev"]),
                )
            ]
        ),
        go.Figure(
            [
                go.Indicator(
                    mode="number+delta",
                    title="Rows Passed",
                    value=data["total_rows_passed"],
                    domain=dict(row=0, column=1),
                    delta=dict(reference=data["total_rows_passed_prev"]),
                )
            ]
        ),
        go.Figure(
            [
                go.Indicator(
                    mode="number+delta",
                    title="Rows Proceeeded",
                    value=data["total_rows_processed"],
                    domain=dict(row=0, column=2),
                    delta=dict(reference=data["total_rows_processed_prev"]),
                )
            ]
        ),
        go.Figure(
            [
                go.Indicator(
                    mode="number+delta",
                    title="Rows Failed",
                    value=data["total_rows_failed"],
                    domain=dict(row=0, column=3),
                    delta=dict(
                        reference=data["total_rows_failed_prev"],
                        increasing=dict(color="#ff4136"),
                        decreasing=dict(color="#3d9970"),
                    ),
                )
            ]
        ),
    ]

    for index, col in enumerate(st.columns(len(figs))):
        with col:
            figs[index].update_layout(grid=dict(rows=1, columns=1), height=300)
            st.plotly_chart(figs[index], use_container_width=True)


def add_kpi_cards():
    data = db.get_kpi_cards_data()
    figs = []
    for index, row in data.iterrows():
        figs.append(
            go.Figure(
                go.Indicator(
                    mode="gauge+number+delta",
                    value=row["score"],
                    domain=dict(row=0, column=index),
                    title=dict(text=row["kpi"]),
                    delta=dict(reference=row["score_prev"]),
                    gauge=dict(
                        axis=dict(range=[None, 100], visible=False),
                        bar=dict(color=get_color(row["score"])),
                    ),
                )
            )
        )

    for index, col in enumerate(st.columns(len(figs))):
        with col:
            figs[index].update_layout(grid=dict(rows=1, columns=1), height=300)
            st.plotly_chart(figs[index], use_container_width=True)


def add_overtime_score():
    data = db.get_overtime_score_data()
    fig = go.Figure()
    run_time = [row["run_time"] for _, row in data.iterrows()]
    score = [row["score"] for _, row in data.iterrows()]
    failed_count = [row["failed_count"] for _, row in data.iterrows()]

    fig.add_trace(
        go.Scatter(
            name="Score",
            x=run_time,
            y=score,
            fill="tozeroy",
            mode="lines+markers+text",
            marker=dict(color="#4d7596"),
            text=score,
            texttemplate="%{text:.2f}", 
            textposition="bottom center",
        )
    )
    fig.add_trace(
        go.Scatter(
            name="# Failed",
            x=run_time,
            y=failed_count,
            mode="lines+markers+text",
            marker=dict(color="#8A4C49"),
            text=failed_count,
            texttemplate="%{text:f}", 
            textposition="top center"
        )
    )
    fig.update_layout(title="Data Quality over Time", height=350)
    st.plotly_chart(fig, use_container_width=True)
