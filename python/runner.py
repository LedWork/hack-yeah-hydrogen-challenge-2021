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
import random
import pandas as pd


if __name__ == '__main__':
    arguments = docopt(__doc__, version='Runner 1.0')
    print(arguments)

    n = 10
    m = 5
    set_I = range(1, n + 1)
    set_J = range(1, m + 1)
    c = {(i, j): random.normalvariate(0, 1) for i in set_I for j in set_J}
    a = {(i, j): random.normalvariate(0, 5) for i in set_I for j in set_J}
    l = {(i, j): random.randint(0, 10) for i in set_I for j in set_J}
    u = {(i, j): random.randint(10, 20) for i in set_I for j in set_J}
    b = {j: random.randint(0, 30) for j in set_J}

    opt_model = plp.LpProblem(name="MIP Model", sense=plp.LpMinimize)

    # if x is Integer
    x_vars = {(i, j):
                  plp.LpVariable(cat=plp.LpInteger,
                                 lowBound=l[i, j], upBound=u[i, j],
                                 name="x_{0}_{1}".format(i, j))
              for i in set_I for j in set_J}

    # Less than equal constraints
    constraints = {j: opt_model.addConstraint(
        plp.LpConstraint(
            e=plp.lpSum(a[i, j] * x_vars[i, j] for i in set_I),
            sense=plp.LpConstraintLE,
            rhs=b[j],
            name="constraint_{0}".format(j)))
        for j in set_J}

    # constraints2 = {j: opt_model.addConstraint(
    #     plp.LpConstraint(
    #         e=plp.lpSum(a[i, j] * x_vars[i, j] for i in set_I),
    #         sense=plp.LpConstraintLE,
    #         rhs=b[j],
    #         name="constraint_{0}".format(j)))
    #     for j in set_J}

    objective = plp.lpSum(x_vars[i, j] * c[i, j]
                          for i in set_I
                          for j in set_J)

    opt_model += objective

    # solving with CBC
    status = opt_model.solve()

    print("status = " + plp.LpStatus[status])
    # print("x = " + str(plp.value(x)))
    # print("y = " + str(plp.value(y)))
