"""
Cython version of prime number program.
This file must be imported as a Cython module.

Based on http://docs.cython.org/src/tutorial/cython_tutorial.html
"""


def primes(int n_primes):

    cdef int n, k, i
    cdef int primes[1000]

    if n_primes > 1000:
        raise ValueError('k <= 1000 required.')

    k = 0
    n = 2
    while k < n_primes:
        i = 0
        while i < k and n % primes[i] != 0:
            i += 1
        if i == k:
            primes[k] = n
            k += 1

        n += 1

    # We cannot return the C-style integer array primes to Python,
    # so we convert the valid entries to a list.
    return [p for p in primes[:n_primes]]
