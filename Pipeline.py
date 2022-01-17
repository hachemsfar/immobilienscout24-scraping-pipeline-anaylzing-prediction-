from airflow.models import DAG
from datetime import datetime
from airflow.operators.python import PythonOperator
from airflow.operators.dummy_operator import DummyOperator




from textwrap import dedent

import Extract_Transform,Transform,Load


def custom_success_function(context):
    "Define custom success notification behavior"
    dag_run = context.get('dag_run')
    task_instances = dag_run.get_task_instances()
    print("These task instances succeeded:", task_instances)
    
default_arguments = {
    'owner': 'Hachem SFAR',
    'email': 'hachem.sfar@supcom.tn'
    ,'start_date': datetime(2022, 1, 17)
    ,	'email': ['hachem.sfar@supcom.tn']
    ,'email_on_failure': True
    }

etl_dag = DAG( 'etl_workflow', default_args=default_arguments )




with DAG('Immobilienscout24 Pipeline',description='Immobilienscout24',schedule_interval="@daily",start_date=datetime(2022, 1, 17),catchup=False) as dag:
    # [END instantiate_dag]
    # [START documentation]
    dag.doc_md = __doc__
    # [END documentation]
    
    
    # [START main_flow]
    ExtractTransform_task = PythonOperator(
        task_id='extract_Transform',
        python_callable=Extract_Transform.Extract_and_Transform(),
    )
    extract_task.doc_md = dedent(
        """\
    #### Extract/Transform task
    The Extract task is to get data ready for the rest of the data pipeline.
    In this case, getting data is simulated by scraping data from immobilienscout24 website
    
    The Transform task is to parse the json response and collected the features into dictionnary file
    """
    )
    
    
    
    load_task = PythonOperator(
        task_id='Load',
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
    A simple sucess task which send an email, when the pipeline doesn't work fine
    """
    )    
    
    ExtractTransform_task >> load_task >> success_task