# Currently crudely copypasted from my notes of the commands I ran while developing. Needs tidying up and testing (and probably lots more sudo)

FROM ubuntu:latest
RUN apt-get update -y
RUN apt-get install software-properties-common -y
RUN apt-get install python3-pip -y && \
    apt-get install python3-venv -y && \
    python3  -m venv ~/venvs/pipeline_venv && \
    source ~/venvs/pipeline_venv/bin/activate

RUN sudo apt-get install libmariadb-dev-compat libmariadb-dev

# Airflow needs a home. `~/airflow` is the default, but you can put it
# somewhere else if you prefer (optional)
RUN export AIRFLOW_HOME=~/airflow
# Install Airflow using the constraints file
RUN AIRFLOW_VERSION=2.5.0
RUN PYTHON_VERSION="$(python3 --version | cut -d " " -f 2 | cut -d "." -f 1-2)"
# For example: 3.7
RUN CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
# For example: https://raw.githubusercontent.com/apache/airflow/constraints-2.5.0/constraints-3.7.txt
RUN pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"

RUN pip install apache-airflow-providers-google --constraint "${CONSTRAINT_URL}"
RUN pip install apache-airflow-providers-mysql --constraint "${CONSTRAINT_URL}"
# The Standalone command will initialise the database, make a user,
# and start all components for you.
RUN export AIRFLOW_VAR_CURRENT_GAME_WEEK=current_game_week
RUN airflow db init
RUN airflow users create \
    --username admin \
    --firstname Joe \
    --lastname Warriner \
    --role Admin \
    --email joewarriner40@gmail.com
