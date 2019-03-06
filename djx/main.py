import docopt
from djx.utils import load_yaml
import uuid
from djx.plan import parse_pipeline
from djx.pandas_backend import write_plan, write_task, get_batch, get_next_task
from djx.run_task import run_task
from docopt import docopt


def djx_add(plan_file):
    plan = load_yaml(plan_file)
    plan['plan_id'] = uuid.uuid4().hex
    write_plan(plan)
    tasks = parse_pipeline(**plan)
    write_task(tasks)
    return plan['plan_id']


def djx_run(plan_id):
    try:
        while True:
            this_task = get_next_task(plan_id)
            this_task = run_task(this_task)
            write_task(this_task)
    except StopIteration:
        print('Finished!!!')
    except BaseException as e:
        raise e

def main():
    """
Usage:
    djx add <plan-file>
    djx run <plan-id>

Options:
    """
    args = docopt(__doc__)
    if args.get('add'):
        djx_add(args['<batch-file>'])

    elif args.get('run'):
        djx_work(int(args['<plan-id>']))

if __name__ == "__main__":
    main()
