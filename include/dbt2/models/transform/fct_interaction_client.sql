-- fct_invoices.sql

-- Create the fact table by joining the relevant keys from dimension table
WITH fct_interaction_client_cte AS (
    SELECT
        row_number() OVER () AS interaction_id,
        {{ dbt_utils.generate_surrogate_key(['age', 'job', 'marital', 'education', 'housing', 'loan', 'euribor3m']) }} as client_id,
        row_number() OVER () AS time_id,
        row_number() OVER () AS economic_id,
        contact_target AS contact_method,
        duration,
        previous_count,
        target_decision
    FROM {{ source('retail', 'raw_invoices') }}
)
SELECT
    interaction_id,
    client_id,
    time_id,
    economic_id,
    contact_method,
    duration,
    previous_count,
    target_decision
FROM fct_interaction_client_cte fi
