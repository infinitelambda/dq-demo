# dbt
Demo dbt project using dq-tools package
```bash
cd dq-demo/dbt
```


- Try to configure your snowflake connection with env vars:
  ```bash
  export DBT_SNOWFLAKE_TEST_ACCOUNT=your_value
  export DBT_SNOWFLAKE_TEST_USER=your_value
  export DBT_ENV_SECRET_SNOWFLAKE_TEST_PASSWORD=your_value
  export DBT_SNOWFLAKE_TEST_ROLE=your_value
  export DBT_SNOWFLAKE_TEST_WAREHOUSE=your_value
  ```
- Then, running the following commands:
  ```bash
  export DBT_PROFILES_DIR=.
  dbt debug # Configure your dbt profiles.yml until it's green
  dbt deps # Install dq-tools package
  dbt run
  dbt test
  ```

### Build the dbt project with storing test results:
  ```bash
  dbt build --vars '{dq_tools_enable_store_test_results: true}' [--exclude package:dq_tools]
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
    dbt build -s package:dq_tools
    ```
  - Check the docs site
    ```bash
    dbt docs generate && dbt docs serve
    ```

### Resources:
- Learn more about dbt [in the docs](https://docs.getdbt.com/docs/introduction)
- Check out [Discourse](https://discourse.getdbt.com/) for commonly asked questions and answers
- Join the [chat](https://community.getdbt.com/) on Slack for live discussions and support
- Find [dbt events](https://events.getdbt.com) near you
- Check out [the blog](https://blog.getdbt.com/) for the latest news on dbt's development and best practices
