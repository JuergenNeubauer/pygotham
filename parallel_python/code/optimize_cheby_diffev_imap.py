#!/usr/bin/env python
"""
Solve Nth-order Chebyshev polynomial coefficients with Differential Evolution.
Launch optimizers in parallel with itertools map.

Requires: development version of mystic
  http://pypi.python.org/pypi/mystic
"""

def optimize(solver, mapper, nodes, target='rosen', **kwds):
    if target == 'rosen': # 3d-rosenbrock
        ndim = 3
        actual_coeffs = [1.0] * ndim
        pprint = list
    else: # 4th-order chebyshev
        from poly import chebyshev4coeffs as actual_coeffs
        ndim = len(actual_coeffs)
        from mystic.math import poly1d as pprint

    # number of trials
    N = nodes
    print "Number of trials: %s" % N
    print "==============="

    # initial guess
    import random
    x0 = ([random.uniform(-100,100) for i in xrange(ndim)] for i in xrange(N))

    # minimize the function
    results = mapper(solver, x0, **kwds)

    # find the results with the lowest energy
    from optimize_helper import best_results
    solution = best_results(results)

    print "==============="
    print "Actual params:\n %s" % pprint(actual_coeffs)
    print "Solved params:\n %s" % pprint(solution[0])
    print "Function value: %s" % solution[1]
    print "Total function evals: %s" % solution[4]
    return 


# build the solver-model pairs
def diffev_chebyshev(x0, *args, **kwds):
    # Differential Evolution solver
    from optimize_helper import diffev as the_solver
    # Chebyshev cost function
    from poly import chebyshev4cost as the_model
    return the_solver(the_model, x0, monitor=True, *args, **kwds)

# get the map functions
from itertools import imap                   # itertools


if __name__ == '__main__':
    target = 'cheby'
    print "Function: %s" % target
    print "Solver: %s" % 'diffev'
    optimize(diffev_chebyshev, imap, nodes=1, target=target)

 
# end of file
