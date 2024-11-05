FROM quay.io/astronomer/astro-runtime:12.2.0

RUN python -m venv dbt_venv && source dbt_venv/bin/activate && \
    pip install --no-cache-dir dbt-bigquery && deactivate

    RUN python -m venv dbt_venv2 && source dbt_venv2/bin/activate && \
    pip install --no-cache-dir dbt-bigquery && deactivate