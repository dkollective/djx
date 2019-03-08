"""
Usage:
    djx add <plan-file>
    djx run <plan-id>
    djx add-run <plan-file>
"""

from docopt import docopt
from djx.plan import add_plan
from djx.task import run_next


def main():
    args = docopt(__doc__)
    if args.get('add'):
        add_plan(args['<plan-file>'])

    elif args.get('run'):
        run_next(int(args['<plan-id>']))

    elif args.get('add-run'):
        plan_id = add_plan(args['<plan-file>'])
        run_next(plan_id)


if __name__ == "__main__":
    main()
