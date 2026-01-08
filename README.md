# djx

A lightweight experimental framework for reproducible and traceable data science experiments.

## Overview

djx helps you run parameterized experiments with automatic job generation, execution tracking, and result organization. Define your experiment in YAML or JSON, specify parameter grids, and djx handles the rest.

## Key Features

- **Multiple Formats**: Support for YAML and JSON configuration files
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

1. **Create an experiment configuration** in YAML (see `example/config/iris.yml`) or JSON (see `example/config/iris.json`):

**YAML format:**
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

**JSON format:**
```json
{
  "define": {
    "config_file": "<<cwd>>/experiments/<<project_id>>/<<datetime>>/<<job_idx>>/config.json"
  },
  "meta": {
    "project_id": "my_experiment"
  },
  "config": {
    "model_args": {
      "n_estimators": 100,
      "max_depth": 2
    }
  },
  "grid": [
    {
      "model_args.max_depth": [2, 3, 4]
    }
  ]
}
```

2. **Run the experiment**:

```bash
# Run with YAML
djx example/config/iris.yml

# Run with JSON
djx example/config/iris.json
```

3. **Check results** in `experiments/<project_id>/<datetime>/`

## Experiment Configuration

### File Formats

djx supports both **YAML** (`.yml`, `.yaml`) and **JSON** (`.json`) configuration files:
- Use the format that best suits your workflow
- Both formats support all djx features (placeholders, grids, includes)
- Include files can mix formats (YAML can include JSON and vice versa)

### Output Formats

Configure the output format for job configs via the `config_file` path extension:
- `.yml` or `.yaml`: YAML format (default)
- `.json`: JSON format

### Basic Structure

- `define`: Variables used in placeholders (e.g., file paths)
- `script_template`: Shell script template to execute
- `meta`: Experiment metadata (project_id, name, etc.)
- `config`: Parameters passed to your code
- `grid`: Parameter grid for job generation (optional)
- `include`: Other config files to merge (optional, supports both YAML and JSON)

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

See the example configurations:
- `example/config/iris.yml` - YAML format with complex grid
- `example/config/iris.json` - JSON format with simple grid

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
