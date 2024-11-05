WITH client_dim_cte AS (
    SELECT
        {{ dbt_utils.generate_surrogate_key(['age', 'job', 'marital', 'education', 'housing', 'loan', 'euribor3m']) }} as client_key,
        age,
        job,
        marital,
        education,
        housing,
        loan
    FROM {{ source('bank_marketing', 'bank_additional') }}
)
SELECT
    cd.*
FROM client_dim_cte cd