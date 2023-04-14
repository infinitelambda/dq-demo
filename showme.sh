# 1. transform and test data
cd dbt
dbt build --exclude package:dq_tools --vars '{dq_tools_enable_store_test_results: true}'
dbt build -s package:dq_tools

# 2. run data quality dashboard
cd ..
python dashboard/jobs/export_dq_marts.py
streamlit run dashboard/data_quality_score.py