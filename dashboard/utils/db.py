import duckdb

_conn = duckdb.connect("dashboard/dq_mart.duckdb")


def get_overall_statistics_data():
    return (
        _conn.sql(
            """
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
    """
        )
        .to_df()
        .iloc[0]
    )


def get_kpi_cards_data():
    return _conn.sql(
        """
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
    """
    ).to_df()


def get_overtime_score_data():
    return _conn.sql(
        """
        select  run_time as run_time,
                avg(rows_passed * 100.00 / rows_processed) as score,
                sum(case when rows_failed > 0 then 1 else 0 end) as failed_count
        from    BI_DQ_METRICS
        group by run_time
        order by 1
    """
    ).to_df()
