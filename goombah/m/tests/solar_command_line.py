import numpy as np
import sys, os
from subprocess import run, PIPE


def call_solar(x):
    print(x)
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
        # print(command)
        result = run(command, stdout=PIPE, stderr=PIPE, text=True)
        # print(result)
        # print(result.stdout)
        # print(result.stderr)
        intermediate_output = result.stdout.splitlines()[-2]
        vecout = np.array([float(i) for i in intermediate_output.split(" ")[-7:]])

        to_save = {"vecout": vecout, "var_vals": x}
        DB = np.append(DB, to_save)
        np.save(database, DB)

    coeffs = np.append([1e-6], 0.5*np.ones((1,6)))
    coeffs[2] *= 2e-6

    # FOR GOOMBAH
    coeffs = np.sqrt(coeffs)
    coeffs[0] = 1e-6
    output = coeffs*vecout

    # # FOR POUNDERS
    # coeffs[0] = 1e-6
    # coeffs = np.sqrt(coeffs)
    # output = np.maximum(vecout*coeffs,0)
    # print(np.sum(output**2))

    return output


if __name__ == "__main__":
    x = np.array([float(i) for i in sys.argv[1:]])
    output = call_solar(x)
    np.savetxt("vecout.out", output)
