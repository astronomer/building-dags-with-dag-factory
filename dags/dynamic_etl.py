"""
Create a single DAG using dag-factory and the PythonOperator.
"""

from dagfactory import DagFactory

# Pass in an exact config file name
dag_factory: DagFactory = DagFactory("/usr/local/airflow/dags/etl.yml")

# Clean and generate DAGs
dag_factory.clean_dags(globals())
dag_factory.generate_dags(globals())

# Last line of file
