"""
Pure Python version of prime number program with numba.jit.
This file is to be imported as a pure Python module.

Based on http://docs.cython.org/src/tutorial/cython_tutorial.html
"""

import numba

@numba.jit
def primes(n_primes):
    "Returns list of the first n_primes primes."

    primes = []
    k = 0  # index of next prime in primes
    n = 2  # next candidate number
    while k < n_primes:
        i = 0
        while i < k and n % primes[i] != 0:
            i += 1
        if i == k:
            primes.append(n)
            k += 1
        n += 1
    return primes
