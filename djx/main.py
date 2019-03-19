"""
Usage:
    djx add <exp-file>
    djx run <exp-id>
    djx add-run <exp-file>
"""
import logging
import djx
from docopt import docopt
from djx.exp import add_exp
from djx.job import run_next

log = logging.getLogger(djx.__name__)

log.setLevel(logging.DEBUG)
if not log.handlers:
    ch = logging.StreamHandler()
    log.addHandler(ch)


def main():
    args = docopt(__doc__)
    if args.get('add'):
        add_exp(args['<exp-file>'])

    elif args.get('run'):
        while run_next(int(args['<exp-id>'])):
            pass

    elif args.get('add-run'):
        exp_id = add_exp(args['<exp-file>'])
        while run_next(exp_id):
            pass


if __name__ == "__main__":
    main()
