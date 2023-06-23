import sys, os

import ibcdfo.pounders as pdrs
import numpy as np
from calFun import calFun
from subprocess import run, PIPE

sys.path.append("../../../../minq/py/minq5/")  # Needed for spsolver=2


def call_solar(x):
    database = "solar_10_database.npy"
    DB = []
    match = 0
    if os.path.exists(database):
        DB = np.load(database, allow_pickle=True)
        for db_entry in DB:
            if np.allclose(db_entry["var_vals"], x, rtol=1e-12, atol=1e-12):
                vecout = db_entry["vecout"]
                match = 1
                break

    if match == 0:
        np.savetxt("./x.txt", x, fmt="%16.16f", delimiter=" ", newline=" ")
        command = ["./solar", "10", "x.txt", "-v"]
        result = run(command, stdout=PIPE, stderr=PIPE, text=True)
        intermediate_output = result.stdout.splitlines()[-2]
        vecout = np.array([float(i) for i in intermediate_output.split(" ")[-7:]])

        to_save = {"vecout": vecout, "var_vals": x}
        DB = np.append(DB, to_save)
        np.save(database, DB)

    vecout[0] = np.sqrt(vecout[0])
    coeffs = np.append([1e-6], 0.5 * np.ones((1, 6)))
    coeffs[2] *= 2e-6
    coeffs = np.sqrt(coeffs)
    output = np.maximum(vecout * coeffs, 0)

    print(np.sum(output**2))

    return output


# Sample calling syntax for pounders
# func is a function imported from calFun.py as calFun
func = call_solar
# n [int] Dimension (number of continuous variables)
n = 5
# X0 [dbl] [min(fstart,1)-by-n] Set of initial points  (zeros(1,n))
X0 = np.array([900.0, 10.0, 12.0, 0.20, 0.20])
mpmax = int(0.5 * (n + 1) * (n + 2))
# nfmax [int] Maximum number of function evaluations (>n+1) (100)
nfmax = 50
# gtol [dbl] Tolerance for the 2-norm of the model gradient (1e-4)
gtol = 10**-13
# delta [dbl] Positive trust region radius (.1)
delta = 0.1
# nfs [int] Number of function values (at X0) known in advance (0)
nfs = 1
# m [int] number of residuals
m = 7
# F0 [dbl] [fstart-by-1] Set of known function values  ([])
F0 = np.zeros((1, 7))
# xind [int] Index of point in X0 at which to start from (1)
xind = 0
# Low [dbl] [1-by-n] Vector of lower bounds (-Inf(1,n))
Low = np.array([793.0, 2.0, 2.0, 0.01, 0.01])
# Upp [dbl] [1-by-n] Vector of upper bounds (Inf(1,n))
Upp = np.array([995.0, 50.0, 30.0, 5.00, 5.00])
# printf [log] 1 Indicates you want output to screen (1)
printf = True
spsolver = 2

F0[0, :] = func(X0)

[X, F, flag, xkin] = pdrs.pounders(func, X0, n, mpmax, nfmax, gtol, delta, nfs, m, F0, xind, Low, Upp, printf, spsolver)

print(np.sum(F**2, axis=1))
