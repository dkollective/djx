# djx

A experimental library towards a reproducible, traceable and convenient data science
platform. This library is in a very early state, you are very welcome to contribute
to bring it to the next level.

# idea

DJX is based on three tables to organize data science experiments:
* experiments, this is what you as researcher define
* jobs, an experiment usually require multiple tasks to be executed
* records, each task usually creates a (large) number of results

Each experiment usually consists of the mulitple task. For each task, the same code is executed, however with a different set of parameters. The typical use case is a scan over hyperparameter i.e. grid search, or training the model on different subsets of the data i.e. cross-validation. Additional to the parameter a task also typically requires one or multiple datasets. Each task emits results, these results can contain artifacts, such as a trained model.

A experiment can be defined as a YAML. Have a look at the [example](djx/example/experiments/iris.yml).

The code you want to run takes a (possible nested) parameters as input. There are library
method to get data, to write metrics and to store artifacts, such as a trained model.
Have a look at the [example code](djx/example/src/iris.py).

# enviroment
djx runs currently on postgres. You need to provide credentials as enviroment variables.
Additional three folders, one local temporary, one for persistant storage of datasets and
one for persistent storage of artifacts need to be defined.

```
export DJX_PG_HOST=
export DJX_PG_PORT=
export DJX_PG_USER=
export DJX_PG_PASSWORD=
export DJX_PG_DBNAME=
export DJX_PG_SCHEMA=

export DJX_DATA_TEMP=
export DJX_DATA_STORE=
export DJX_ARTIFACT_STORE=
```

# use it

### add an experiment to the system.
```
djx add djx/example/experiments/iris.yml

```
### run jobs from an experiment
```
djx run 1

```

# credits

This library originated in discussions by Levin Brinkmann,
Stefan Matting and Sebastian Jäger about the setup of a lightweight experimental
framework for reproducible and traceable data science research.
