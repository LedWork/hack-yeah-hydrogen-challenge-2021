"""Naval Fate.

Usage:
  runner.py
  runner.py (-h | --help)
  runner.py --version

Options:
  -h --help     Show this screen.
  --version     Show version.

"""
from docopt import docopt
import pulp as plp


if __name__ == '__main__':
    arguments = docopt(__doc__, version='Runner 1.0')
    print(arguments)

    opt_model = plp.LpProblem(name="MIP Model")

    x = plp.LpVariable("x", 0, 3)
    y = plp.LpVariable("y", 0, 1)
    prob = plp.LpProblem("myProblem", plp.LpMinimize)
    prob += x + y <= 2
    prob += -4 * x + y

    status = prob.solve()
    # status = prob.solve(GLPK(msg=0))

    print("status = " + plp.LpStatus[status])
    print("x = " + str(plp.value(x)))
    print("y = " + str(plp.value(y)))
