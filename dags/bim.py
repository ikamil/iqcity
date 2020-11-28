from datetime import datetime

from airflow import DAG
from airflow.models import Variable
from airflow.operators.dummy_operator import DummyOperator
from pipeline.bim import BIMOperator

args = {
    'owner': 'iqcity',
    'start_date': datetime(2020, 11, 27),
    'depends_on_past': False,
    'retries': 0,
}

BIM_BUCKET = Variable.get("BIM_BUCKET", default_var="roide-pipeline")
BIM_PATH = Variable.get("BIM_PATH", default_var="kroger/_tmp/rt/chelny/")

dag = DAG(dag_id='bim_excel_processing', default_args=args, schedule_interval="@once")
extract_bim_data = BIMOperator(
    task_id='extract_bim_data',
    default_args=args,
    bim_bucket=BIM_BUCKET,
    bim_path=BIM_PATH,
    dag=dag
)

finish = DummyOperator(task_id='wb_finish', dag=dag)

extract_bim_data >> finish
