WITH datetime_dim_cte AS(
    SELECT
        row_number() OVER () AS time_id,
        month,
        day_of_week,
        dt_year as year
    FROM {{ source('bank_marketing', 'bank_additional') }}
)
SELECT
    dt.*
FROM datetime_dim_cte dt