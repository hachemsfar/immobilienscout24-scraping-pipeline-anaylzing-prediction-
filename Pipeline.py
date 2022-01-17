from airflow.models import DAG
from datetime import datetime
from airflow.operators.python import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from textwrap import dedent

import Extract,Transform,Load


def custom_success_function(context):
    "Define custom success notification behavior"
    dag_run = context.get('dag_run')
    task_instances = dag_run.get_task_instances()
    print("These task instances succeeded:", task_instances)
    
default_arguments = {
    'owner': 'Hachem SFAR',
    'email': 'hachem.sfar@supcom.tn'
    ,'start_date': datetime(2021, 12, 19)
    ,	'email': ['hachem.sfar@supcom.tn']
    ,'email_on_failure': True
    }

etl_dag = DAG( 'etl_workflow', default_args=default_arguments )




with DAG('TLC Trip Pipeline',description='TLC Trip',schedule_interval="@monthly",start_date=datetime(2021, 12, 1),catchup=False,tags=['example'],) as dag:
    # [END instantiate_dag]
    # [START documentation]
    dag.doc_md = __doc__
    # [END documentation]


    # [START main_flow]
    extract_task = PythonOperator(
        task_id='extract',
        python_callable=Extract.Extract(),
    )
    extract_task.doc_md = dedent(
        """\
    #### Extract task
    A simple Extract task to get data ready for the rest of the data pipeline.
    In this case, getting data is simulated by reading from a hardcoded JSON string.
    This data is then put into xcom, so that it can be processed by the next task.
    """
    )

    transform_task = PythonOperator(
        task_id='transform',
        python_callable=Transform.Transform(),
    )
    transform_task.doc_md = dedent(
        """\
    #### Transform task
    A simple Transform task which takes in the collection of order data from xcom
    and computes the total order value.
    This computed value is then put into xcom, so that it can be processed by the next task.
    """
    )

    load_task = PythonOperator(
        task_id='load',
        python_callable=Load.load()
    )
    load_task.doc_md = dedent(
        """\
    #### Load task
    A simple Load task which takes in the result of the Transform task, by reading it
    from xcom and instead of saving it to end user review, just prints it out.
    """
    )
        
    success_task = DummyOperator(
  		task_id='success_task',
  		on_success_callback=custom_success_function
      )
    
    success_task.doc_md = dedent(
        """\
    #### success task
    A simple sucess task which send an email, when the pipeline worked fine.
    """
    )    
    
    extract_task >> transform_task >> load_task >> success_task