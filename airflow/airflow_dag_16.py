from airflow import DAG
from airflow.operators.python import PythonOperator
from clickhouse_driver import Client
import psycopg2
import time

from datetime import datetime


default_args = {
    'owner': 'Kornev',
    'start_date': datetime(2024, 7, 28)
}

dag = DAG(
    dag_id='airflow_dag_16',
    default_args=default_args,
    schedule_interval='14 */1 * * *',
    description='Первый локальный даг',
    catchup=False,
    max_active_runs=1,
    tags=['test']
)


def main():

    ch_client = Client('local-clickhouse-server',
                        user='default',
                        password='default',
                        port=9000,
                        verify=False,
                        database='default',
                        settings={"numpy_columns": False, 'use_numpy': True},
                        compression=False)
        
    pg_client = psycopg2.connect(host='local-postgres',
                                user='default',
                                password='default',
                                port=5432,
                                dbname='postgres')
    
    ch_client.execute("""
        INSERT INTO report.tares_load
        select toStartOfHour(dt) dt_h
             , office_id
             , uniq(tare_id) qty_tares
        from tareLoad
        where tare_type = 'TBX'
        and is_load = 1
        group by dt_h, office_id
    """)

    print('Витрина в ClickHouse обновлена')
    time.sleep(5)

    df = ch_client.query_dataframe(f"""
        select dt_h
             , office_id
             , qty_tares
        from report.tares_load final
        where dt_load >= toStartOfHour(now()) - interval 2 hour
    """)

    df = df.to_json(orient='records', date_format='iso')

    cursor = pg_client.cursor()
    cursor.execute(f"CALL sync.tares_load_import(_src := '{df}')")
    pg_client.commit()
    cursor.close()
    pg_client.close()

    print('Витрина в Postgres обновлена')


task1 = PythonOperator(task_id='task1', python_callable=main, dag=dag)