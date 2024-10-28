"""
Use a dynamically-generated YAML file to create multiple DAGs.
"""

from dagfactory import DagFactory

# Pass in an exact config file name
dag_factory: DagFactory = DagFactory("/usr/local/airflow/dags/dynamic_etl.yml")

# Clean and generate DAGs
dag_factory.clean_dags(globals())
dag_factory.generate_dags(globals())

# Last line of file
