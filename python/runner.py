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
import pandas as pd


if __name__ == '__main__':
    data_folder = "./data/"
    arguments = docopt(__doc__, version='Runner 1.0')
    # print(arguments)

    pv_locations = pd.read_csv(data_folder + "pv_location.csv")
    print('')
    print('== pv_location.csv ==')
    print("pv_location = ", pv_locations['pv_location'].to_list())
    print("distance = ", pv_locations['distance'].to_list())
    print("max_MW = ", pv_locations['max_MW'].to_list())
    print("collection_cost = ", pv_locations['collection_cost'].to_list())

    pv_generation = pd.read_csv(data_folder + "pv_generation.csv")
    print('')
    print('== pv_generation.csv ==')
    print("month = ", pv_generation['month'].to_list())
    print("pv_generation = ", pv_generation['pv_generation'].to_list())

    type_of_construction = pd.read_csv(data_folder + "type_of_construction.csv")
    print('')
    print('== type_of_construction.csv ==')
    print("type = ", type_of_construction['type'].to_list())
    print("cost = ", type_of_construction['cost'].to_list())

    opt_model = plp.LpProblem(name="MIP_Model", sense=plp.LpMinimize)

    locations = pv_locations['pv_location'].to_list()
    time = pv_generation['month'].to_list()
    pv_gen = pv_generation['pv_generation'].to_list()
    pv_kWh = dict(zip(time, pv_gen))

    print('')
    print("pv_kWh = ", pv_kWh)

    max_pv = dict(zip(locations, pv_locations['max_MW'].to_list()))
    print("max_pv = ", max_pv)

    # ZMIENNE
    # number of PV per location
    Pv_n = plp.LpVariable.dicts("pv_count",
                                locations,
                                lowBound=0,
                                cat=plp.LpInteger)

    # number of energy storage units per location
    Accu_n = plp.LpVariable.dicts("accu_count",
                                  locations,
                                  lowBound=0,
                                  cat=plp.LpInteger)

    # number of hydrogen storage units per location
    Storage_n = plp.LpVariable.dicts("storage_count",
                                     locations,
                                     lowBound=0,
                                     cat=plp.LpInteger)

    # energy production per location and time
    E_production_pv = plp.LpVariable.dicts("E_production_pv",
                                           ((l, dt) for l in locations for dt in time),
                                           lowBound=0,
                                           cat=plp.LpContinuous)

    # energy in storage per location and time
    E_stored_pv = plp.LpVariable.dicts("E_stored_pv",
                                       ((l, dt) for l in locations for dt in time),
                                       lowBound=0,
                                       cat=plp.LpContinuous)

    # hydrogen in storage per location and time
    H2_stored_pv = plp.LpVariable.dicts("H2_stored_pv",
                                        ((l, dt) for l in locations for dt in time),
                                        lowBound=0,
                                        cat=plp.LpContinuous)

    # energy used from pv
    E_used_pv = plp.LpVariable.dicts("E_used_pv",
                                     ((l, dt) for l in locations for dt in time),
                                     lowBound=0,
                                     cat=plp.LpContinuous)
    # energy used from accu
    E_used_accu_pv = plp.LpVariable.dicts("E_used_accu_pv",
                                          ((l, dt) for l in locations for dt in time),
                                          lowBound=0,
                                          cat=plp.LpContinuous)
    # hydrogen used from storage
    H2_used_storage_pv = plp.LpVariable.dicts("H2_used_storage_pv",
                                              ((l, dt) for l in locations for dt in time),
                                              lowBound=0,
                                              cat=plp.LpContinuous)

    # opt_df = pd.DataFrame.from_dict(Pv_n, orient="index",
    #                                 columns=["variable_object"])
    #
    # # opt_df.index = pd.Index(opt_df.index)
    #
    # opt_df.reset_index(inplace=True)
    # opt_df["solution_value"] = opt_df["variable_object"].apply(lambda item: item.varValue)
    # opt_df.drop(columns=["variable_object"], inplace=True)
    # opt_df.to_csv("./optimization_solution.csv")
    #
    #
    # objs = [2, 3, 2, 5, 3]
    # weights = [1, 2, 2, 1, 3]
    # knapweight = 5
    #
    # prob = plp.LpProblem('Knapsack', plp.LpMaximize)
    # xs = [plp.LpVariable("x{}".format(i + 1), cat="Binary") for i in range(len(objs))]
    #
    # # add objective
    # total_prof = sum(x * obj for x, obj in zip(xs, objs))
    # prob += total_prof
    #
    # # add constraint
    # total_weight = sum(x * w for x, w in zip(xs, weights))
    # prob += total_weight <= knapweight
    #
    # status = prob.solve()
    # print(plp.LpStatus[status])
    # print("Objective value:", plp.value(prob.objective))
    # print('\nThe values of the variables : \n')
    # for v in prob.variables():
    #     print(v.name, "=", v.varValue)

    # # if x is Integer
    # x_vars = {(i, j):
    #               plp.LpVariable(cat=plp.LpInteger,
    #                              lowBound=l[i, j], upBound=u[i, j],
    #                              name="x_{0}_{1}".format(i, j))
    #           for i in set_I for j in set_J}
    #
    # # Less than equal constraints
    # constraints = {j: opt_model.addConstraint(
    #     plp.LpConstraint(
    #         e=plp.lpSum(a[i, j] * x_vars[i, j] for i in set_I),
    #         sense=plp.LpConstraintLE,
    #         rhs=b[j],
    #         name="constraint_{0}".format(j)))
    #     for j in set_J}
    #
    # objective = plp.lpSum(x_vars[i, j] * c[i, j]
    #                       for i in set_I
    #                       for j in set_J)
    #
    # opt_model += objective

    # solving with CBC
    # status = opt_model.solve()

    # print("status = " + plp.LpStatus[status])
    # print("x = " + str(plp.value(x)))
    # print("y = " + str(plp.value(y)))
