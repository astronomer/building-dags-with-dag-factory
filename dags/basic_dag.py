"""
Create a single DAG using dag-factory and the EmptyOperator.
"""

from dagfactory import DagFactory

# Pass in an exact config file name
dag_factory: DagFactory = DagFactory("/usr/local/airflow/dags/basic_dag.yml")

# Clean and generate DAGs
dag_factory.clean_dags(globals())
dag_factory.generate_dags(globals())

# Last line of file
