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
# from djx.job import run_next


def main():
    args = docopt(__doc__)
    add_exp(args['<exp-file>'])



if __name__ == "__main__":
    main()
