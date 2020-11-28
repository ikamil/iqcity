from airflow.operators.bash_operator import BaseOperator
from psycopg2.extras import Json
import random, json
from airflow.hooks.postgres_hook import PostgresHook


class DoubleGisOperator(BaseOperator):
    def __init__(self, url, api_request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = url
        self.api_request = api_request

    def execute(self, context):
        pg_hook = PostgresHook('pg_default')
        conn = pg_hook.get_conn()
        c = conn.cursor()
        respond_2gis_example = """{
    "meta": {
        "api_version": "3.0.448950",
        "code": 200,
        "issue_date": "20200626"
    },
    "result": {
        "items": [
            {
                "address_comment": "3, 5 этаж",
                "address_name": "Никольская, %(id)s",
                "id": "%(id)s",
                "name": "Велопрокат №1",
                "type": "branch"
            }
        ],
        "total": 5926
    }
}""" % {"id": random.randint(1, 20000)}
        try:
            c.execute("BEGIN")
            pdata = json.loads(respond_2gis_example).get('result', {'items': []}).get('items', [])
            params = Json(pdata)
            c.callproc("fset_2gis", [params])
            results = c.fetchone()[0]
            c.execute("COMMIT")
        # except Exception as e:
        #     results = {"error": str(e)}
        finally:
            c.close()
        return results
