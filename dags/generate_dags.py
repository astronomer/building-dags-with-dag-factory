"""
Create a single DAG using dag-factory and the EmptyOperator.
"""

# Including the word 'airflow' so this file is parsed
from dagfactory import load_yaml_dags

load_yaml_dags(globals_dict=globals(), suffix=[".yml"])
