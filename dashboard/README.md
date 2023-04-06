# streamlit
Demo Data Quality Score dashboard using Streamlit & DuckDB

### Export DQ MART to duckdb
  ```bash
  cd dq-demo
  python dashboard/jobs/export_dq_marts.py [False]
  ```

### Serve dashboard locally
  ```bash
  streamlit run dashboard/data_quality_score.py

  # You can now view your Streamlit app in your browser.

  # Local URL: http://localhost:8502
  # Network URL: http://192.168.1.5:8502

  # For better performance, install the Watchdog module:

  # $ xcode-select --install
  # $ pip install watchdog
  ```

  Live Dashboard :tada: is [HERE](https://infinitelambda-data-quality-score.streamlit.app/)