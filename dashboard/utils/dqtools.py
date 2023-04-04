import streamlit as st
import plotly.graph_objects as go


def get_color(value):
    if value < 50:
        return "#ff4136" # red
    if value < 70:
        return "orange"
    if value < 90:
        return "yellow"
    return "#3d9970" # green


def add_overall_statistics(conn):
    data = conn.sql("""
        with today as (
            select  avg(rows_passed * 100.00 / rows_processed) as score,
                    sum(rows_passed) as total_rows_passed,
                    sum(rows_processed) as total_rows_processed,
                    sum(rows_failed) as total_rows_failed,
                    max(date_trunc('day', run_time)) as run_date
            from    bi_dq_metrics
            where   1=1
                and date_trunc('day', run_time) = (select max(date_trunc('day', run_time)) from bi_dq_metrics)
        ),
        prev as (
            select  avg(rows_passed * 100.00 / rows_processed) as score,
                    sum(rows_passed) as total_rows_passed,
                    sum(rows_processed) as total_rows_processed,
                    sum(rows_failed) as total_rows_failed
            from    bi_dq_metrics
            where   1=1
                and date_trunc('day', run_time) = (
                    select  max(date_trunc('day', run_time)) 
                    from    bi_dq_metrics 
                    where   run_time < (select run_date from today)
                )
        )
        select      today.score,
                    prev.score as score_prev,
                    today.total_rows_passed,
                    prev.total_rows_passed as total_rows_passed_prev,
                    today.total_rows_processed,
                    prev.total_rows_processed as total_rows_processed_prev,
                    today.total_rows_failed,
                    prev.total_rows_failed as total_rows_failed_prev
        from        today
        cross join  prev
    """).to_df().iloc[0]
    figs = [
        go.Figure([go.Indicator(
            mode="number+delta",
            title="Data Quality Score",
            value=data['score'],
            domain=dict(row=0, column=0),
            delta=dict(reference=data["score_prev"])
        )]),
        go.Figure([go.Indicator(
            mode="number+delta",
            title="Rows Passed",
            value=data['total_rows_passed'],
            domain=dict(row=0, column=1),
            delta=dict(reference=data["total_rows_passed_prev"])
        )]),
        go.Figure([go.Indicator(
            mode="number+delta",
            title="Rows Proceeeded",
            value=data['total_rows_processed'],
            domain=dict(row=0, column=2),
            delta=dict(reference=data["total_rows_processed_prev"])
        )]),
        go.Figure([go.Indicator(
            mode="number+delta",
            title="Rows Failed",
            value=data['total_rows_failed'],
            domain=dict(row=0, column=3),
            delta=dict(
                reference=data["total_rows_failed_prev"],
                increasing=dict(color='#ff4136'),
                decreasing=dict(color='#3d9970'))
        )])
    ]
    
    for index, col in enumerate(st.columns(len(figs))):
        with col:
            figs[index].update_layout(
                grid = dict(rows=1, columns=1),
                height=300
            )
            st.plotly_chart(figs[index], use_container_width=True)


def add_kpi_cards(conn):
    data = conn.sql("""
        with today as (
            select  dq_dimension as kpi,
                    avg(rows_passed * 100.00 / rows_processed) as score,
                    max(date_trunc('day', run_time)) as run_date
            from    bi_dq_metrics
            where   1=1
                and date_trunc('day', run_time) = (select max(date_trunc('day', run_time)) from bi_dq_metrics)
            group by 1
        ),
        prev as (
            select  dq_dimension as kpi,
                    avg(rows_passed * 100.00 / rows_processed) as score
            from    bi_dq_metrics
            where   1=1
                and date_trunc('day', run_time) = (
                    select  max(date_trunc('day', run_time)) 
                    from    bi_dq_metrics 
                    where   run_time < (select run_date from today)
                )
            group by 1
        )
        select      today.kpi,
                    today.score,
                    coalesce(prev.score, 100) as score_prev
        from        today
        left join   prev 
            on      prev.kpi = today.kpi
    """).to_df()
    figs = []
    for index, row in data.iterrows():
        figs.append(go.Figure(
            go.Indicator(
                mode="gauge+number+delta",
                value=row['score'],
                domain=dict(row=0, column=index),
                title=dict(text=row['kpi']),
                delta=dict(reference=row['score_prev']),
                gauge=dict(
                    axis=dict(range=[None,100], visible=False),
                    bar=dict(color=get_color(row['score']))
                )
            )
        ))
    
    for index, col in enumerate(st.columns(len(figs))):
        with col:
            figs[index].update_layout(
                grid = dict(rows=1, columns=1),
                height=300
            )
            st.plotly_chart(figs[index], use_container_width=True)


def add_overtime_score(conn):
    data = conn.sql("""
        select  run_time as run_time,
                avg(rows_passed * 100.00 / rows_processed) as score
        from    BI_DQ_METRICS
        group by run_time
        order by 1
    """).to_df()
    fig = go.Figure()
    xs = [row['run_time'] for index, row in data.iterrows()]
    ys = [row['score'] for index, row in data.iterrows()]
    fig.add_trace(
        go.Scatter(x=xs, y=ys, fill='tozeroy')
    )
    fig.update_layout(
        title='Data Quality over Time',
        height=350
    )
    st.plotly_chart(fig, use_container_width=True)


def add_raw_data(conn):
    st.markdown("Raw Data:")
    data = conn.table("BI_DQ_METRICS").to_df()
    st.write(data)