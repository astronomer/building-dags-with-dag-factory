# Overview



### What You'll Build



### What You'll Learn

- How to author DAGs using `dag-factory` and YAML files.
- How to use Airflow-provider packages, as well as user-defined functions to instantiate DAGs using YAML.
- How to dynamically-generate YAML files using a single template file.


### What You'll Need

To get started with this project, you'll need the following:

- The [`astro`](https://www.astronomer.io/docs/astro/cli/install-cli) CLI
- Docker Desktop
- Your favorite IDE/text editor


## Getting Started

To pull down this code onto your local machine, create a new directory and run the command `git clone XXXX`. To spin up 
your own local instance of this project, run `astro dev start`. This will spin up an instance of Airflow on your 
machine, available via `localhost:8080`.

There are two packages needed to get started with this project, which are both listed in your `requirements.txt` file. 
The first is `dag-factory`, which will be used to define DAGs using YAML. The second is `PyYAML`, which we'll use in 
`include/scripts/generate_dynamic_dag.py` script to dynamically create YAML file using a template. You don't have to 
install these locally; running `astro dev start` will do so in your Docker containers.

Awesome, let's get started!


### Building a Basic DAG


### Building an ETL Pipeline


### Dynamically-Generating DAGs Using Templating


## Resources

