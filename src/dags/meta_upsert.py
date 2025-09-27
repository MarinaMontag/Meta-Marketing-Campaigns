from datetime import timedelta

import pendulum
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator


def run_meta():
    from services.marketing import MetaMarketingAPIService
    from services.pipelines import MetaPipeline
    from settings import settings

    pipeline = MetaPipeline(MetaMarketingAPIService(settings.META_ACCESS_TOKEN, settings.META_AD_ACCOUNT_ID))
    pipeline.upsert_meta_data()

with DAG(
    dag_id="meta_pipeline_test",
    schedule="0 * * * *",
    start_date=pendulum.datetime(2025, 9, 26, tz="Europe/Kyiv"),
    catchup=False,
    default_args={"owner": "meta-etl", "retries": 1, "retry_delay": timedelta(minutes=1)},
) as dag:
    PythonOperator(
        task_id="run_meta_pipeline",
        python_callable=run_meta,
    )
