import numpy as np
from ibcdfo.pounders import general_h_funs, pounders

import io
import sys
from ibcdfo import (
    LOG_LEVEL_NONE, LOG_LEVEL_BASIC, LOG_LEVEL_BASIC_DEBUG,
    BasicLogger
)
import subprocess
from contextlib import (
    contextmanager, redirect_stdout
)



def run_and_log_subprocess(cmd, logger, log_tag, log_level):
    """
    .. todo::
        * This should error check the subprocess command itself and respond
          appropriately to difficulties
    """
    result = subprocess.run(cmd, capture_output=True)

    # Log empty lines as that might be the developer's intention
    for line in result.stdout.decode().split("\n"):
        logger.log(log_tag, line, log_level)

    # No need for empty error messages
    result_stderr = result.stderr.decode().split("\n")
    result_stderr = [line for line in result_stderr if line != ""]
    for line in result_stderr:
        logger.error(log_tag, line)
    if result_stderr:
        raise RuntimeError(f"Failure running subprocess command - {cmd}")


@contextmanager
def run_and_log_pyminq(logger, log_level):
    """
    NOT CLEAR IF THIS IS A GOOD IDEA!

    From the contextlib.redirect_stdout documentation:
        Note that the global side effect on sys.stdout means that this context
        manager is not suitable for use in library code and most threaded
        applications. It also has no effect on the output of subprocesses.
        However, it is still a useful approach for many utility scripts.
    """
    LOG_TAG = "PyMINQ"

    try:
        with redirect_stdout(io.StringIO()) as msg:
            yield
    except Exception as e:
        # Log all stdout generated so far to aid in debugging
        for line in msg.getvalue().split("\n"):
            logger.log(LOG_TAG, line, log_level)
        raise RuntimeError(e)

    for line in msg.getvalue().split("\n"):
        logger.log(LOG_TAG, line, log_level)


def pyminq(x):
    print(f"PyMINQ x arguments - {x}")
    print("")
    print("I will now pretent to do something")
    print("")
    raise NotImplementedError("This functionality does not exist")


def call_beamline_simulation(x):
    LOG_TAG = "IBCDFO Test"
    # Uncomment to see no logging at all
    # logger = BasicLogger(LOG_LEVEL_NONE)
    # Uncomment to see default logging
    logger = BasicLogger(LOG_LEVEL_BASIC)
    # Uncomment to see minimal debug logging
    # logger = BasicLogger(LOG_LEVEL_BASIC_DEBUG)

    logger.log(LOG_TAG, "", LOG_LEVEL_BASIC)
    logger.log(
        LOG_TAG, "Let's love lively logging lessons",
        LOG_LEVEL_BASIC_DEBUG
    )
    logger.log(LOG_TAG, "-" * 80, LOG_LEVEL_BASIC_DEBUG)
    msg = f"I am running my simulation with parameters {x}"
    logger.log(LOG_TAG, msg, LOG_LEVEL_BASIC)

    # Run a command with subprocess
    #
    # I would put the try/except block at one of the highest levels of the
    # application.
    try:
        run_and_log_subprocess(["./a.out"], logger, "Jeff/C++", LOG_LEVEL_BASIC)
    except Exception as e:
        logger.error(LOG_TAG, e)
        #exit(1)
    logger.log(LOG_TAG, "", LOG_LEVEL_BASIC)

    # Run a command that we have direct access to but have no logging control
    # over
    try:
        with run_and_log_pyminq(logger, LOG_LEVEL_BASIC):
            pyminq(x)
    except Exception as e:
        logger.error("PyMINQ", e)
        exit(1)
    logger.log(LOG_TAG, "", LOG_LEVEL_BASIC)

    # In here, put your call to your simulation that takes in the
    # parameters x and returns the three values used in the calculation of
    # emittance.
    # out = put_your_sim_call_here(x)

    out = x.squeeze()[:3]  # This is not doing any beamline simulation!

    assert len(out) == 3, "Incorrect output dimension"
    return np.squeeze(out)


# Adjust these:
n = 4  # Number of parameters to be optimized
X_0 = np.random.uniform(0, 1, (1, n))  # starting parameters for the optimizer
nf_max = int(100)  # Max number of evaluations to be used by optimizer
Low = -1 * np.ones((1, n))  # 1-by-n Vector of lower bounds
Upp = np.ones((1, n))  # 1-by-n Vector of upper bounds
printf = True

# Not as important to adjust:
hfun = general_h_funs.emittance_h
combinemodels = general_h_funs.emittance_combine
m = 3  # The number of outputs from the beamline simulation. Should be 3 for emittance minimization
g_tol = 1e-8  # Stopping tolerance
delta_0 = 0.1  # Initial trust-region radius
F_0 = np.zeros((1, m))  # Initial evaluations (parameters with completed simulations)
F_0[0] = call_beamline_simulation(X_0)
nfs = 1  # Number of initial evaluations
xk_in = 0  # Index in F_0 for starting the optimization (usually the point with minimal emittance)

Options = {}
Options["hfun"] = hfun
Options["combinemodels"] = combinemodels

Prior = {"X_init": X_0, "F_init": F_0, "nfs": nfs, "xk_in": xk_in}

# The call to the method
[Xout, Fout, hFout, flag, xk_inout] = pounders(call_beamline_simulation, X_0, n, nf_max, g_tol, delta_0, m, Low, Upp, Options=Options, Model={})

assert flag >= 0, "pounders crashed"

assert hFout[xk_inout] == np.min(hFout), "The minimum emittance is not at xk_inout"
