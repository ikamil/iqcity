from datetime import datetime

from airflow import DAG
from airflow.models import Variable
from airflow.operators.dummy_operator import DummyOperator

from pipeline.dblgis import DoubleGisOperator

args = {
    'owner': 'iqcity',
    'start_date': datetime(2020, 11, 27),
    'depends_on_past': False,
    'retries': 0,
}


URL_2GIS = Variable.get("URL_2GIS", default_var="https://catalog.api.2gis.com/3.0/items")

dag = DAG(dag_id='2gis_api_import', default_args=args, schedule_interval="@once")
extract_2gis_data = DoubleGisOperator(
    task_id='extract_2gis_data',
    default_args=args,
    api_request='велопрокат',
    url=URL_2GIS,
    dag=dag
)

finish = DummyOperator(task_id='dblgis_finish', dag=dag)

extract_2gis_data >> finish
