WITH economic_dim_cte AS(
    SELECT
        row_number() OVER () AS economic_id,
        emp_var_rate,
        cons_price_idx,
        cons_conf_idx,
        euribor3m,
        nr_employed
    FROM {{ source('bank_marketing', 'bank_additional') }}
)
SELECT
    ec.*
FROM datetime_dim_cte ec