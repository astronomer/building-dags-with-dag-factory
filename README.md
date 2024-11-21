# Overview

DAG Factory ([`dag-factory`](https://github.com/astronomer/dag-factory)) is an open-source library used to define DAGs 
via configuration files. Leveraging this tool allows for data teams to author DAGs in a declarative manner and easily 
migrate workloads from legacy systems in an efficient and scalable way. In this guide, we’ll outline the key steps to 
writing DAGs with DAG Factory and explore how this tool enables bulk DAG creation using YAML.


### What You'll Learn

- How to author DAGs using DAG Factory and YAML files.
- How to use Airflow provider packages, as well as user-defined functions to instantiate DAGs using YAML.
- How to dynamically-generate YAML files using a single template file.


### What You'll Need

To get started with this project, you'll need the following:

- The [`astro`](https://www.astronomer.io/docs/astro/cli/install-cli) CLI
- Docker Desktop
- Your favorite IDE/text editor


## Getting Started

To pull this code down onto your local machine, create a new directory and run the command 
`git clone https://github.com/astronomer/building-dags-with-dag-factory.git`. To spin up your own local instance of this 
project, run `astro dev start`. This will spin up an instance of Airflow on your machine, available via 
`localhost:8080`.

To get started with this tutorial, you'll need to add the `dag-factory` package to your `requirements.txt` file. You 
don't have to install `dag-factory` locally; running `astro dev start` will do so in your Docker containers.

Awesome, let's get started!


### Building a Basic DAG

Authoring a DAG with DAG Factory requires two files; a `.yml` file, and `.py` file. The `.yml` file contains things
like a DAG ID, start date, schedule interval, as well as Task definitions and their dependencies. This is the 
information that will be used to generate your DAG. The `.py` file reads this YAML file, and generates the resulting 
DAG.

In the `dags/` directory, we've defined DAG using the `basic_dag.yml` and `generate_dags.py` files. This DAG is quite 
simple; it has three Tasks (`extract`, `transform`, and `load`) each implemented with the `EmptyOperator`. The syntax 
of the YAML file might feel quite similar to defining a DAG using the `with()` context manager in Python.

```yaml
basic_etl:
  default_args:
    start_date: "2024-01-01"
  schedule_interval: "0 0 * * *"
  catchup: False
  tasks:
    task_a:
      operator: airflow.operators.empty.EmptyOperator
    task_b:
      operator: airflow.operators.empty.EmptyOperator
    task_c:
      operator: airflow.operators.empty.EmptyOperator
```

Once the YAML file has been populated, we'll need a `.py` file to make sure the DAG is generated. **The code in this
`.py` file ensures that all files with the extension `.yml` are parsed.** Here's what that code snippet looks like. 

```python
# Including the word 'airflow' so this file is parsed
from dagfactory import load_yaml_dags

load_yaml_dags(globals_dict=globals(), suffix=[".yml"])
```

That's it! In just two lines of Python, and a little bit of YAML, you've authored a DAG using DAG Factory. When you 
open your local instance of Airflow, you'll see a graph view that looks like the snip below. Now, you can interact with 
this DAG just like you would any other.

![Graph view of a basic DAG built using DAG Factory.](assets/basic_dag__graph_view.png)


### Building an ETL Pipeline

The DAG we created above was quite simple; it contained only three tasks, each of which were `EmptyOperator`'s that ran
in parallel. Just like with traditional DAG authoring, we can use tools like the `PythonOperator`. To do this, we'll 
need to first define "callables". These are functions that we'll eventually pass to `python_callable` to be executed.

For this tutorial, you'll use quite simple Python functions as "callables". These are stored in the 
`inlucde/etl_helpers.py` file, shown below. Note that `transform_helper` and `load_helper` both take at least one 
parameter, which we'll take a closer look at shortly.

```python
def extract_helper():
    pass


def transform_helper(ds_nodash):
    print(f"ds_nodash: {ds_nodash}")


def load_helper(database_name, table_name):
    print(f"database_name: {database_name}, table_name: {table_name}")
```

Like before, we'll also go ahead and create a new YAML file. This time, there's a bit more complexity than before. Here, 
we're using the `PythonOperator`, which takes a couple of parameters. These include the `python_callable_name`, and 
the `python_callable_file`. The `transform` and `load` tasks also take the parameter `op_kwargs` where we pass in the 
`ds_nodash` templated field and the `database_name` and `table_name`, respectively.

If you look closely, we're also setting dependencies between tasks. The `transform` task won't execute until the
`extract` task successfully completes, and `load` is dependent on `transform`.

```yaml
etl:
  default_args:
    start_date: "2024-01-01"
  schedule_interval: "0 0 * * *"
  catchup: False
  tasks:
    extract:
      operator: airflow.operators.python.PythonOperator
      python_callable_name: extract_helper
      python_callable_file: /usr/local/airflow/include/etl_helpers.py
    transform:
      operator: airflow.operators.python.PythonOperator
      python_callable_name: transform_helper
      python_callable_file: /usr/local/airflow/include/etl_helpers.py
      op_kwargs:
        ds_nodash: "{{ds_nodash}}"
      dependencies:
        - extract
    load:
      operator: airflow.operators.python.PythonOperator
      python_callable_name: load_helper
      python_callable_file: /usr/local/airflow/include/etl_helpers.py
      op_kwargs:
        database_name: "DE"
        table_name: "raw"
      dependencies:
        - transform
```


Since we pointed our `generate_dags.py` file to all files ending with `.yml`, there's nothing else that we need to do
in order to generate our DAG. The resulting graph view should look something like this!

![Graph view of an ETL DAG built using DAG Factory.](assets/etl__graph_view.png)


### Dynamically-Generating DAGs Using `default`

Fantastic! Now that we've mastered creating DAGs using DAG Factory, we're going to try to do something a little more 
difficult; generating DAGs dynamically. To do this, we'll be using the `dynamic_etl.yml` file.

At first glance, this file might feel quite similar to `etl.yml`. However, there's one big difference; at the top of 
`dynamic_etl.yml`, you'll see `default`, followed by YAML configuration that closely mirrors what we had seen in 
`etl.yml`. We're going to use a single "default" configuration to build multiple DAGs. 

`default` offers a sort of template to more easily define multiple DAGs without having to copy-and-paste. How does this 
work? DAG Factory uses the configuration defined in `default` and applies it to each of the `business_analytics`, 
`data_science`, and `machine_learning` DAGs outlined below. Then, the default values are supplemented with the values 
provide for each implementation of the default configuration. Since the only real difference between these DAGs are the 
`op_kwargs` passed into the `load_helper()` function, there's no need to copy and paste the entire configuration three 
times. This allows for us to use a single "templated" DAG configuration to define three similar, but distinct, DAGs.

```yaml
default:
  catchup: false
  default_args:
    start_date: '2024-01-01'
  schedule_interval: 0 0 * * *
  tasks:
    extract:
      operator: airflow.operators.python.PythonOperator
      python_callable_file: /usr/local/airflow/include/etl_helpers.py
      python_callable_name: extract_helper
    load:
      dependencies:
      - transform
      operator: airflow.operators.python.PythonOperator
      python_callable_file: /usr/local/airflow/include/etl_helpers.py
      python_callable_name: load_helper
    transform:
      dependencies:
      - extract
      op_kwargs:
        ds_nodash: '{{ds_nodash}}'
      operator: airflow.operators.python.PythonOperator
      python_callable_file: /usr/local/airflow/include/etl_helpers.py
      python_callable_name: transform_helper


business_analytics:
  tasks:
    load:
      op_kwargs:
        database_name: BA
        table_name: inventory

data_science:
  tasks:
    load:
      op_kwargs:
        database_name: DS
        table_name: daily_sames

machine_learning:
  tasks:
    load:
      op_kwargs:
        database_name: ML
        table_name: training_data

```

Using a single set of default values, we now have spawned three DAGs each with the same tasks, but different parameters 
passed to those tasks. Your DAGs view in Airflow should now look a little something like the view below.

![Dynamically-generated DAGs.](assets/dynamically_generated_dags.png)

Congrats! Using DAG Factory, you've dynamically-generated DAGs using a single set of default values and injected 
parameters for each DAG.

## Resources

- https://www.astronomer.io/docs/learn/dag-factory
- https://github.com/astronomer/dag-factory
- https://registry.astronomer.io/providers/apache-airflow/versions/latest/modules/pythonoperator
