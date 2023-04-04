import os
import sys
from utils import yaml
from pathlib import Path
import snowflake.connector as sf
import pandas as pd
import duckdb

DBT_PROFILE_DIR = str(Path.cwd() / "dbt")
DBT_PROFILE_NAME = "dq_demo"

# Read config from dbt profiles.yml
profile_config = None
with open(f"{DBT_PROFILE_DIR}/profiles.yml", 'r') as file:
    profile_config = yaml.load_yaml_text(file.read())
profile_config = profile_config.get(DBT_PROFILE_NAME, {})
target = profile_config.get("target")
config = profile_config.get("outputs", {}).get(target, {})
for key, value in config.items():
    if "env_var" in str(value):
        config[key] = os.environ.get(value.split("'")[1])
# print(config)

# Export table configured at args[1]
with sf.connect(**config) as conn:
    data = pd.read_sql(sql=f"select * from {config.get('database')}.{config.get('schema')}.BI_DQ_METRICS", con=conn)
print("--data:", data.shape)

# Write to Duck DB
db_file = f"./dashboard/dq_mart.duckdb"
incremental = eval(sys.argv[1]) if len(sys.argv) > 1 else True
assert isinstance(incremental, bool)
print("--incremental:", incremental)
with duckdb.connect(db_file) as duckdb_conn:
    existed = not duckdb_conn\
        .sql(f"select * from information_schema.tables where table_name='BI_DQ_METRICS'")\
        .to_df().empty
    if existed:
        if not incremental:
            duckdb_conn.sql(f"truncate table BI_DQ_METRICS")
    else:
        duckdb_conn.sql(f"create table BI_DQ_METRICS as select * from data")
    duckdb_conn.sql(f"insert into BI_DQ_METRICS select * from data")
    
    duckdb_conn.table("BI_DQ_METRICS").show()
print("Duck DB created/updated:", db_file)