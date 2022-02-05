"""
Usage:
    djx <exp-file>
"""
import djx
from docopt import docopt
from djx.exp import add_exp


def main():
    args = docopt(__doc__)
    add_exp(args['<exp-file>'])


if __name__ == "__main__":
    main()
