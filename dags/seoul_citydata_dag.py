from datetime import datetime, timedelta
import sys
import os
import logging
from airflow import DAG
from airflow.operators.python import PythonOperator

# Add the project root to sys.path to allow importing from src
# The project is now located within the Apache_Airflow directory
PROJECT_ROOT = "/opt/airflow/seoul-citydata"
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from src.api_client import CityDataAPIClient
from src.db_client import DBClient

logger = logging.getLogger("airflow.task")

def run_collection_job():
    """Wrapper function for data collection to be used in Airflow"""
    logger.info("Starting Seoul City Data Collection Task")
    try:
        api_client = CityDataAPIClient()
        db_client = DBClient()
        
        # Fetch data
        data_map = api_client.get_data_for_all_targets()
        
        if not data_map:
            logger.warning("No data fetched.")
            return

        # Save data
        db_client.process_and_save(data_map)
        logger.info(f"Successfully processed {len(data_map)} areas.")
        
    except Exception as e:
        logger.error(f"Task failed: {e}")
        raise

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'seoul_citydata_collector',
    default_args=default_args,
    description='Collects Real-time Seoul City Data every 10 minutes',
    schedule='*/10 * * * *',  # Every 10 minutes
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['seoul', 'citydata'],
) as dag:

    collect_data_task = PythonOperator(
        task_id='collect_seoul_data',
        python_callable=run_collection_job,
    )

    collect_data_task
