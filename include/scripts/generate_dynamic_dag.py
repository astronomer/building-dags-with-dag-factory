"""
generate_dynamic_dag.py

Script that is run to generate a .yml file to be used to source a dag-factory DAG.
"""

# Import modules here
import yaml
import json

# Read in the template file
with open("include/scripts/template.yml", "r") as yaml_file:
    template: dict = yaml.load(yaml_file, yaml.SafeLoader)

# Update the template file with the variables
TEMPLATE_VARIABLES: list = [
    {
        "<< dag_id >>": "business_analytics",
        "<< database_name >>": "BA",
        "<< table_name >>": "inventory"
    }, {
        "<< dag_id >>": "data_science",
        "<< database_name >>": "DS",
        "<< table_name >>": "daily_sales"
    }, {
        "<< dag_id >>": "machine_learning",
        "<< database_name >>": "ML",
        "<< table_name >>": "training_data"
    }
]

# Create a list of populated templates
populated_templates: dict = {}

# Loop through each of the variables, update the template, and add to populated_templates
for variables in TEMPLATE_VARIABLES:
    populated_template: dict = template.copy()
    populated_template__str: str = json.dumps(populated_template)

    for key, value in variables.items():
        populated_template__str = populated_template__str.replace(key, str(value))

    # Assert that the first key-value pair is the DAG
    populated_template = json.loads(populated_template__str)
    populated_template__keys = list(populated_template.keys())
    if len(populated_template__keys) == 1:
        populated_templates[populated_template__keys[0]] = populated_template[populated_template__keys[0]]
    else:
        raise Exception("Unexpected format from populated template.")


# Write the YAML file
with open("dags/dynamic_etl.yml", "w") as ingestion__config:
    ingestion__config.write(yaml.dump(populated_templates))
