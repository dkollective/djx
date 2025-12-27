# djx

A lightweight experimental framework for reproducible and traceable data science experiments.

## Overview

djx helps you run parameterized experiments with automatic job generation, execution tracking, and result organization. Define your experiment in YAML, specify parameter grids, and djx handles the rest.

## Key Features

- **Grid Search**: Automatically generate jobs from parameter grids
- **Placeholder System**: Dynamic values using `<<variable>>` syntax
- **Config Includes**: Reuse configurations across experiments
- **Job Tracking**: Unique IDs and timestamps for each experiment and job
- **Dry Run**: Test experiment setup without execution

## Installation

```bash
python3.13 -m venv .venv
source .venv/bin/activate 
pip install -e ".[example]"
```

## Quick Start

1. **Create an experiment YAML** (see `example/config/iris.yml`):

```yaml
define:
  config_file: <<cwd>>/experiments/<<project_id>>/<<datetime>>/<<job_idx>>/config.yml
  script_file: <<cwd>>/experiments/<<project_id>>/<<datetime>>/<<job_idx>>/run.sh
script_template: |
  python example/src/iris.py <<config_file>> > <<log_file>>
meta:
  project_id: my_experiment
config:
  model_args:
    n_estimators: 100
    max_depth: 2
grid:
  - model_args.max_depth: [2, 3, 4]
```

2. **Run the experiment**:

```bash
djx example/config/iris.yml
```

3. **Check results** in `experiments/<project_id>/<datetime>/`

## Experiment Configuration

### Basic Structure

- `define`: Variables used in placeholders (e.g., file paths)
- `script_template`: Shell script template to execute
- `meta`: Experiment metadata (project_id, name, etc.)
- `config`: Parameters passed to your code
- `grid`: Parameter grid for job generation (optional)
- `include`: Other YAML files to merge (optional)

### Placeholders

Use `<<variable>>` syntax for dynamic values:
- `<<cwd>>`: Current working directory
- `<<datetime>>`: Timestamp (YYYY-MM-DD--HH-MM-SS)
- `<<date>>`: Date (YYYY-MM-DD)
- `<<job_idx>>`: Job index
- `<<job_uid>>`: Unique job ID
- `<<exp_uid>>`: Unique experiment ID
- Custom variables from `define` and `meta`

Type conversion: `<<int:variable>>`, `<<float:variable>>`, `<<bool:variable>>`

### Grid Search

Two grid formats supported:

**Simple grid** (cartesian product):
```yaml
grid:
  - model_args.max_depth: [2, 3, 4]
    model_args.n_estimators: [50, 100]
```

**List grid** (explicit combinations):
```yaml
grid:
  - - model_args:
        max_depth: 2
        n_estimators: 50
    - model_args:
        max_depth: 3
        n_estimators: 100
```

## Example

See `example/config/iris.yml` for a complete cross-validation example with grid search over hyperparameters.

## Usage

```bash
# Run experiment
djx example/config/iris.yml

# Dry run (generate files without execution)
djx example/config/iris.yml --dry-run

# Verbose output
djx example/config/iris.yml --verbose

# Pass additional variables
djx example/config/iris.yml --custom_var value
```

## Credits

This library originated in discussions by Levin Brinkmann, Stefan Matting and Sebastian Jäger about the setup of a lightweight experimental framework for reproducible and traceable data science research.
