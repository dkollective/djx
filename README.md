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

This library originated in discussions and test implementation by Levin Brinkmann,
X and Y about the setup of a lightweight experimental
framework for reproducable and traceable data science research.
