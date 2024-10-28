# Overview

DAG Factory ([`dag-factory`](https://github.com/astronomer/dag-factory)) is an open-source library to define DAGs using configuration files, typically using 
YAML. Leveraging this tools allows for data teams to author DAGs in a declarative manner and easily migrate workloads 
from legacy systems in an efficient and scalable way. In this guide, we’ll outline the key steps to writing DAGs with 
DAG Factory and explore how this tool enables bulk DAG creation without introducing code sprawl or having to write 
extensive code.


### What You'll Build



### What You'll Learn

- How to author DAGs using DAG Factory and YAML files.
- How to use Airflow-provider packages, as well as user-defined functions to instantiate DAGs using YAML.
- How to dynamically-generate YAML files using a single template file.


### What You'll Need

To get started with this project, you'll need the following:

- The [`astro`](https://www.astronomer.io/docs/astro/cli/install-cli) CLI
- Docker Desktop
- Your favorite IDE/text editor


## Getting Started

To pull this code down onto your local machine, create a new directory and run the command `git clone XXXX`. To spin up 
your own local instance of this project, run `astro dev start`. This will spin up an instance of Airflow on your 
machine, available via `localhost:8080`.

There are two packages needed to get started with this project, which are both listed in your `requirements.txt` file. 
The first is `dag-factory`, which will be used to define DAGs using YAML. The second is `PyYAML`, which we'll use in 
`include/scripts/generate_dynamic_dag.py` script to dynamically create YAML file using a template. You don't have to 
install these locally; running `astro dev start` will do so in your Docker containers.

Awesome, let's get started!


### Building a Basic DAG

Authoring a DAG with DAG Factory requires two files; a `.yml` file, and `.py` file. The `.yml` file contains things
like a DAG ID, start date, schedule interval, as well as Task definitions and their dependencies. The `.py` file reads
this YAML file, and generates the resulting DAG.

In the `dags/` directory, we've defined DAG using the `basic_dag.yml` and `basic_dag.py` files. This DAG is quite 
simple; it has three Tasks (`extract`, `transform`, and `load`) each implemented with the `EmptyOperator`. The syntax 
of the YAML file might feel quite similar to defining a DAG using the `with()` context manager in Python.

```yaml
basic_etl:
  default_args:
    start_date: "2024-01-01"
  schedule_interval: "0 0 * * *"
  catchup: False
  tasks:
    extract:
      operator: airflow.operators.empty.EmptyOperator
    transform:
      operator: airflow.operators.empty.EmptyOperator
    load:
      operator: airflow.operators.empty.EmptyOperator
```

Once the YAML file has been populated, we'll need a `.py` file to make sure the DAG is generated properly. This code is 
mostly boilerplate, and will remain the same for almost all DAGs authored using DAG Factory. Here's what that looks 
like:

```python
from dagfactory import DagFactory

# Pass in an exact config file name
dag_factory: DagFactory = DagFactory("/usr/local/airflow/dags/basic_dag.yml")

# Clean and generate DAGs
dag_factory.clean_dags(globals())
dag_factory.generate_dags(globals())
```


### Building an ETL Pipeline


### Dynamically-Generating DAGs Using Templating


## Resources

- https://www.astronomer.io/docs/learn/dag-factory
