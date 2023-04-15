# 1 & 2. Run: transform, test and capture test results
cd dbt
dbt build --exclude package:dq_tools --vars '{dq_tools_enable_store_test_results: true}'

# 3. Build mart of Data Quality
dbt build -s package:dq_tools
cd ..
python dashboard/jobs/export_dq_marts.py

# 4. Get the dashboard
streamlit run dashboard/data_quality_score.py