from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from workers.gold_data_extractor import GoldDataExtractor
from workers.retrieve_data import Retriever
from workers.gold_data_updater import Updater
import os 
from dotenv import load_dotenv
load_dotenv()

def my_task():
    print("Running my task")
    extractor = GoldDataExtractor()
    retriever = Retriever(
        mongo_url="",
        database_name="test_streaming",
        collection_name="test2"
    )
    comments, full_data = retriever.retrieve_latest_reviews(5)
    label_update = extractor.extract_gold_data(comments)
    updater = Updater(
        mongo_url="",
        database_name="test_streaming",
        collection_name="test3"
    )
    updater.update_data(full_data, label_update)

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

dag = DAG(
    dag_id='run_task_every_minute',
    default_args=default_args,
    description='A simple DAG to run my_task every minute',
    start_date=datetime(2025, 3, 31),
    schedule_interval='* * * * *',  # every 1 minute
    catchup=False,
    tags=['example'],
)

# run_my_task = PythonOperator(
#     task_id='run_my_python_task',
#     python_callable=my_task,
#     dag = dag
# )

# run_my_task
