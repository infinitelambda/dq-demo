# Data Quality with dbt
Demonstration of Data Quality with dbt


![Streamlit dashboard](https://raw.githubusercontent.com/il-dat/dq-demo/main/dashboard/assets/simple-dashboard.png)

**Clone repo**
```
git clone git@github.com:il-dat/dq-demo.git
cd dq-demo
```

## Activate Demo environment in your local
In this demo, we're gonna use `poetry` to setup the virtual environment with Python 3.9+
> Assuming your local python alias is `python3`
```bash
python3 -m poetry install  # Install dependencies
python3 -m poetry shell    # Enter shell
```

## Run dbt
```bash
dbt debug # Configure your dbt profiles.yml until it's green
dbt deps # Install dq-tools package
dbt build --vars '{dq_tools_enable_store_test_results: true}' # Build the dbt project with storing test results
```

### Enable dq models and build it
  - Enable dq models within `dbt_project.yml` file
    ```yaml
    models:
      dq_tools:
        +enabled: true
    ```
  - Build it
    ```bash
    dbt build -s ???
    ```
  - Check the docs site
    ```bash
    dbt docs generate && dbt docs serve
    ```

## Check Dashboard
In the poetry shell, run:
```bash
streamlit run dashboard/dash-dqtools.py

# You can now view your Streamlit app in your browser.

# Local URL: http://localhost:8502
# Network URL: http://192.168.1.5:8502

# For better performance, install the Watchdog module:

# $ xcode-select --install
# $ pip install watchdog
```
