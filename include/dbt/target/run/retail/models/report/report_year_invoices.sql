
  
    

    create or replace table `northern-shield-437204-m0`.`retail`.`report_year_invoices`
      
    
    

    OPTIONS()
    as (
      -- report_year_invoices.sql
SELECT
  dt.year,
  dt.month,
  COUNT(DISTINCT fi.invoice_id) AS num_invoices,
  SUM(fi.total) AS total_revenue
FROM `northern-shield-437204-m0`.`retail`.`fct_invoices` fi
JOIN `northern-shield-437204-m0`.`retail`.`dim_datetime` dt ON fi.datetime_id = dt.datetime_id
GROUP BY dt.year, dt.month
ORDER BY dt.year, dt.month
    );
  