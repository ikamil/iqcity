from airflow.operators.bash_operator import BaseOperator
from airflow.hooks.S3_hook import S3Hook
from psycopg2.extras import Json
import random, json, io
from airflow.hooks.postgres_hook import PostgresHook
from airflow.hooks.S3_hook import S3Hook
from multiprocessing.pool import Pool
from typing import List
from pandas import DataFrame
from functools import partial
import pandas as pd


class BIMOperator(BaseOperator):
    def __init__(self, bim_bucket, bim_path, s3_conn='s3_default', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bim_bucket = bim_bucket
        self.bim_path = bim_path
        self.s3_conn = s3_conn

    def process_xlsx(self, s3_hook, bim_bucket, key):
        with pd.ExcelFile(io.BytesIO(s3_hook.get_key(key, bim_bucket).get()['Body'].read())) as excel_file:
            datas: dict = excel_file.parse(sheet_name=0)
        result = []
        for k, v in datas.items():
            result.extend(v.to_dict('records'))
        return result


    def execute(self, context):
        s3_hook: S3Hook = S3Hook(self.s3_conn)
        keys: List[str] = s3_hook.list_keys(prefix=self.bim_path, bucket_name=self.bim_bucket)
        keys = list(filter(lambda key: key.endswith('.xlsx'), keys))
        result = []
        with Pool() as pool:
            records = pool.map(partial(self.process_xlsx, s3_hook=s3_hook, bucket=self.bim_bucket), keys)
        for recs in records:
            result.extend(recs)

        pg_hook = PostgresHook('pg_default')
        conn = pg_hook.get_conn()
        c = conn.cursor()
        try:
            c.execute("BEGIN")
            pdata = json.dumps(result)
            params = Json(pdata)
            c.callproc("fset_bim", [params])
            results = c.fetchone()[0]
            c.execute("COMMIT")
        except Exception as e:
            results = {"error": str(e)}
        finally:
            c.close()
        return results
