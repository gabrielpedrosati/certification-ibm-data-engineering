from datetime import timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago

default_args ={
    'owner':'Gabriel Pedrosa',
    'start_date':days_ago(0),
    'email':['gabriel@gmail.com'],
    'email_on_failure': True,
    'email_on_retry':True,
    'retries':1,
    'retry_delay':timedelta(minutes=5)
}

dag = DAG(
    'ETL_toll_data',
    description='Apache Airflow Final Assignment',
    schedule_interval=timedelta(days=1),
    default_args=default_args
)


unzip_data = BashOperator(
    task_id='unzip_data',
    bash_command='cd /home/projects/airflow/dags/finalassignment/ ; tar -xvzf tolldata.tgz',
    dag=dag
)

extract_data_from_csv = BashOperator(
    task_id='extract_csv_file',
    bash_command='cut -d"," -f1,2,3,4 vehicle-data.csv > csv_data.csv',
    dag=dag
)

extract_data_from_tsv = BashOperator(
    task_id='extract_data_from_tsv',
    bash_command="cut -f5,6,7 -d$'\t' tollplaza-data.tsv | tr '\t' ',' > tsv_data.csv",
    dag=dag
)

extract_data_from_fixed_width = BashOperator(
    task_id="extract_data_from_fixe_width",
    bash_command='cat payment-data.txt | tr -s " " |  tr " " "," | cut -d"," -f11,12 > fixed_width_data.csv',
    dag=dag
)

consolidate_data = BashOperator(
    task_id="consolidate_data",
    bash_command="paste -d ',' csv_data.csv tsv_data.csv fixed_width_data.csv > extracted_data.csv",
    dag=dag
)

transform_data = BashOperator(
    task_id="transform_data",
    bash_command="cat extracted_data.csv | tr '[:lower:]' '[:upper:]' > transformed_data.csv",
    dag=dag
)

unzip_data >> extract_data_from_csv >> extract_data_from_tsv >> extract_data_from_fixed_width >> consolidate_data >> transform_data