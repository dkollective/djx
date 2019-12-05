"""
Usage:
    djx add <exp-file>
    djx run <job-file>
"""
import djx
from docopt import docopt
from djx.exp import add_exp
from djx.run import run_job


def main():
    args = docopt(__doc__)
    if args.get('add'):
        add_exp(args['<exp-file>'])

    elif args.get('run'):
        run_job(args['<job-file>'])



if __name__ == "__main__":
    main()
