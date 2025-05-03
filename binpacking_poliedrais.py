from docplex.mp.model import Model

w = [3, 5, 7, 6, 2]
w_d = [5, 5, 5, 5, 5]
gamma = [100, 100, 100, 100, 100] # 0, 1, 2, 3
C = 12
N = M = len(w)
set_I = range(0, N)
set_J = range(0, M)

binpacking_model = Model('binpacking')
x_vars = {(i, j):
    binpacking_model.binary_var(name="x_{0}_{1}".format(i, j)) for i in set_I for j in set_J}
y_vars = {j:
    binpacking_model.binary_var(name="y_{0}".format(j)) for j in set_J}
z_vars = {j:
    binpacking_model.continuous_var(name="z_{0}".format(j)) for j in set_J}
rho_vars = {(i, j):
    binpacking_model.continuous_var(name="rho_{0}_{1}".format(i, j)) for i in set_I for j in set_J}

# == constraints
constraints1 = {i:
    binpacking_model.add_constraint(
        ct=binpacking_model.sum(x_vars[i, j] for j in set_J) == 1,
        ctname="constraint_{0}".format(i))
    for i in set_I}

# <= constraints
constraints2 = {j:
    binpacking_model.add_constraint(
        ct=binpacking_model.sum(w[i] * x_vars[i, j] + rho_vars[i, j] for i in set_I) + gamma[j] * z_vars[j] <= C *
           y_vars[j],
        ctname="constraint_{0}".format(j))
    for j in set_J}

# >= constraints
constraints3 = {(i, j):
    binpacking_model.add_constraint(
        ct=z_vars[j] + rho_vars[i, j] >= w_d[i] * x_vars[i, j],
        ctname="constraint_{0}_{1}".format(i, j))
    for i in set_I
    for j in set_J}

constraints4 = {j:
    binpacking_model.add_constraint(
        ct=z_vars[j] >= 0,
        ctname="constraint_{0}".format(j))
    for j in set_J}

constraints5 = {(i, j):
    binpacking_model.add_constraint(
        ct=rho_vars[i, j] >= 0,
        ctname="constraint_{0}_{1}".format(i, j))
    for i in set_I
    for j in set_J}

obj_fn = binpacking_model.sum(y_vars[j] for j in set_J)
binpacking_model.set_objective("min", obj_fn)
binpacking_model.print_information()
sol = binpacking_model.solve()
binpacking_model.print_solution()
if sol is None:
    print("Infeasible")
