"""
IBCDFO: Interpolation-Based Composite Derivative-Free Optimization
This package contains methods to solve structured blackbox optimization
problems of the form:
    minimize h(F(x))
where x is the n-dimensional optimization variable, F(x) is the m-dimensional
output of blackbox, and h is a known scalar-valued mapping.
"""

from importlib.metadata import version

__version__ = version("ibcdfo")

# constants
from .constants import (
    LOG_LEVEL_NONE, LOG_LEVEL_BASIC, LOG_LEVEL_BASIC_DEBUG,
    LOG_LEVEL_MAX,
    LOG_LEVELS
)

# functions
from . import manifold_sampling, pounders

# classes
from .AbcLogger import AbcLogger
from .BasicLogger import BasicLogger

# ----- Python unittest-based test framework
# Used for automatic test discovery
from .load_tests import load_tests

# Allow users to run full test suite as mytemplate.test()
from .test import test
