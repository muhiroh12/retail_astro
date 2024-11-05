from airflow.decorators import dag, task
from datetime import datetime
from bank_transform import clean_transform_filter
from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateEmptyDatasetOperator

from astro import sql as aql
from astro.files import File
from airflow.models.baseoperator import chain
from astro.sql.table import Table, Metadata
from astro.constants import FileType



@dag(
    start_date=datetime(2024, 10, 1),
    schedule=None,
    catchup=False,
    tags=['bank_additional'],
)
def bank_additional_dag():
    
    @task
    def bank_add_transform():
        transformed_file_path = clean_transform_filter('include/dataset/bank-additional-full.csv')
        return transformed_file_path
    
    transformed_file_path = bank_add_transform() 
    
    upload_bank_data_to_gcs = LocalFilesystemToGCSOperator(
        task_id='upload_bank_data_to_gcs',
        src='include/dataset/bank-additional-full-cleaned.csv',  
        dst='raw/bank_additional_cleaned.csv',
        bucket='bank_marketing_astro',
        gcp_conn_id='gcp',
        mime_type='text/csv',
    )
    
    create_bank_dataset = BigQueryCreateEmptyDatasetOperator(
        task_id='create_bank_dataset',
        dataset_id='bank_marketing',
        gcp_conn_id='gcp',
    )
    
    gcs_bank_to_raw = aql.load_file(
        task_id='gcs_bank_to_raw',
        input_file=File(
            'gs://bank_marketing_astro/raw/bank_additional_cleaned.csv',
            conn_id='gcp',
            filetype=FileType.CSV,
        ),
        output_table=Table(
            name='bank_additional',
            conn_id='gcp',
            metadata=Metadata(schema='bank_marketing')
        ),
        use_native_support=False,
    )
    
    @task.external_python(python='/usr/local/airflow/soda_venv/bin/python')
    def check_load(scan_name='check_load', checks_subpath='sources'):
        from include.soda.check_function_bank import check

        return check(scan_name, checks_subpath)
    
    transformed_file_path >> upload_bank_data_to_gcs >> create_bank_dataset >> gcs_bank_to_raw >> check_load()
    
bank_additional_dag()