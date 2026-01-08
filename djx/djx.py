import argparse
import json
import os
import re
import subprocess
import sys
import uuid
from datetime import datetime
from time import sleep

import yaml

from djx.grid import parse_grid
from djx.merge import deepermerge


def get_uuid():
    return str(uuid.uuid4())


def write_file(string, filename):
    with open(filename, 'w') as f:
        f.write(string)


def save_yaml(obj, filename):
    with open(filename, 'w') as f:
        yaml.dump(obj, f)


def load_yaml(filename):
    with open(filename) as f:
        data = yaml.safe_load(f)
    return data


def load_json(filename):
    with open(filename) as f:
        data = json.load(f)
    return data


def save_json(obj, filename):
    with open(filename, 'w') as f:
        json.dump(obj, f, indent=2)


def load_config(filename):
    """Load a config file, detecting format by extension (.yml, .yaml, or .json)."""
    ext = os.path.splitext(filename)[1].lower()
    if ext in ['.yml', '.yaml']:
        return load_yaml(filename)
    elif ext == '.json':
        return load_json(filename)
    else:
        raise ValueError(f"Unsupported config file format: {ext}. Use .yml, .yaml, or .json")


def replace_placeholder(element, replacements=None):
    """Replace placeholders in the format <<type:variable|default>> with values from replacements dict."""
    if replacements is None:
        replacements = {}

    if isinstance(element, dict):
        for key, value in element.items():
            element[key] = replace_placeholder(value, replacements)
    elif isinstance(element, list):
        return [replace_placeholder(item, replacements) for item in element]
    elif isinstance(element, str):

        def replacement_function(match):
            placeholder_type = match.group(1) if match.group(1) else "str"
            placeholder_variable = match.group(2)
            default_value = match.group(3) if match.group(3) else None
            replacement_value = replacements.get(placeholder_variable, default_value if default_value else match.group(0))

            # Convert replacement value to specified type
            if placeholder_type == "float" and replacement_value is not None:
                try:
                    replacement_value = float(replacement_value)
                except ValueError:
                    replacement_value = None
            elif placeholder_type == "int" and replacement_value is not None:
                try:
                    replacement_value = int(replacement_value)
                except ValueError:
                    replacement_value = None
            elif placeholder_type == "bool" and replacement_value is not None:
                replacement_value = True if str(replacement_value).lower() == "true" else False
            elif placeholder_type == "list_int" and replacement_value is not None:
                try:
                    replacement_value = list(map(int, str(replacement_value).split(",")))
                except ValueError:
                    replacement_value = None

            return replacement_value

        pattern = r"<<(?:(\w+): )?(\w+)(?:\|([^>]+))?>>"
        matches = list(re.finditer(pattern, element))

        # If exactly one match and it spans the entire string, perform type conversion
        if len(matches) == 1 and matches[0].span() == (0, len(element)):
            return replacement_function(matches[0])

        # For strings with multiple placeholders or additional text, replace without type conversion
        def string_replacement_function(match):
            return str(replacement_function(match))
        result = re.sub(pattern, string_replacement_function, element)
        return result

    return element


def parse_unknown_args(unknown_args, argv):
    """Parse unknown command-line arguments (--key value) into a dictionary."""
    dynamic_args = {}
    for arg in unknown_args:
        if arg.startswith("--"):
            key = arg.lstrip("-")
            if argv.index(arg) + 1 < len(argv):
                value = argv[argv.index(arg) + 1]
                dynamic_args[key] = value

    return dynamic_args


def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def queue_job(job, dry_run=False):
    """Generate script and config files for a job, then execute it (unless dry_run=True)."""
    script_template = job.pop('script_template')
    script_file = job.pop('script_file')
    config_file = job.pop('config_file')
    command = job.pop('command')

    script_dir = os.path.dirname(script_file)
    ensure_dir(script_dir)
    write_file(script_template, script_file)

    config_dir = os.path.dirname(config_file)
    ensure_dir(config_dir)
    
    # Save config in the appropriate format based on file extension
    ext = os.path.splitext(config_file)[1].lower()
    if ext == '.json':
        save_json(job['config'], config_file)
    else:
        save_yaml(job['config'], config_file)

    if not dry_run:
        sleep(1)
        subprocess.run(command, stdout=subprocess.PIPE, shell=True, check=True)


def include_files(exp):
    """Load and merge config files (YAML or JSON) specified in the 'include' field into the experiment config."""
    if 'include' in exp:
        include = exp.pop('include')
        for inc in include:
            new = load_config(inc)
            exp = deepermerge(exp, new)
    return exp


def main():
    parser = argparse.ArgumentParser(
        description='DJX is a tool for running experiments',
    )
    parser.add_argument('exp_file', type=str, help='The experiment file to run')
    parser.add_argument('--dry-run', action='store_true', help='Dry run the experiment')

    argv = sys.argv[1:]
    known_args, unknown_args = parser.parse_known_args(sys.argv[1:])
    dynamic_args = parse_unknown_args(unknown_args, argv)
    args_dict = vars(known_args)
    args_dict.update(dynamic_args)

    args_dict = {
        'exp_uid': get_uuid(),
        'date': datetime.now().strftime('%Y-%m-%d'),
        'datetime': datetime.now().strftime('%Y-%m-%d--%H-%M-%S'),
        'cwd': os.getcwd(),
        **args_dict,
    }


    exp = load_config(args_dict['exp_file'])
    exp = include_files(exp)

    if 'grid' in exp:
        base_job = {k: v for k, v in exp.items() if k != 'grid'}
        configs = parse_grid(exp['grid'], base_job['config'])
        jobs = [{**base_job, 'config': c} for c in configs]
    else:
        jobs = [exp]

    for idx, j in enumerate(jobs):
        define = j.pop('define').copy()
        args_dict = {**args_dict, **j['meta'], 'job_uid': get_uuid(), 'job_idx': idx}
        define = replace_placeholder(define, args_dict)
        args_dict = {**args_dict, **define}
        j = replace_placeholder(j, args_dict)
        queue_job(j, dry_run=args_dict['dry_run'])


if __name__ == '__main__':
    main()
