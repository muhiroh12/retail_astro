WITH campaign_dim_cte AS (
    SELECT
        DISTINCT campaign_id,
        contact_target
    FROM {{ source('bank_marketing', 'bank_additional') }}
)
SELECT
    cp.*
FROM campaign_dim_cte cp