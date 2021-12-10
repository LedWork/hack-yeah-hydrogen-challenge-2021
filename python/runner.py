"""Naval Fate.

Usage:
  runner.py (-h | --help)
  runner.py --version

Options:
  -h --help     Show this screen.
  --version     Show version.

"""
from docopt import docopt


if __name__ == '__main__':
    arguments = docopt(__doc__, version='Runner 1.0')
    print(arguments)