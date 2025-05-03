from docplex.mp.model import Model

w = [3, 5, 7, 6, 2]
C = 12
N = M = len(w)
set_I = range(0, N)
set_J = range(0, M)

binpacking_model = Model('binpacking')
x_vars = {(i, j):
              binpacking_model.binary_var(name="x_{0}_{1}".format(i, j)) for i in set_I for j in set_J}
# y = binpacking_model.binary_var_list(M, name="y")
y_vars = {(j):
              binpacking_model.binary_var(name="y_{0}".format(j)) for j in set_J}

# == constraints
constraints1 = {i:
    binpacking_model.add_constraint(
        ct=binpacking_model.sum(x_vars[i, j] for j in set_J) == 1,
        ctname="constraint_{0}".format(i))
    for i in set_I}

# <= constraints
constraints2 = {j:
    binpacking_model.add_constraint(
        ct=binpacking_model.sum(w[i] * x_vars[i, j] for i in set_I) <= C * y_vars[j],
        ctname="constraint_{0}".format(j))
    for j in set_J}

obj_fn = binpacking_model.sum(y_vars[j] for j in set_J)
binpacking_model.set_objective("min", obj_fn)
binpacking_model.print_information()
sol = binpacking_model.solve()
binpacking_model.print_solution()
if sol is None:
    print("Infeasible")
