'''
Created on Nov 29, 2012

@author: plesser
'''

import timeit
import numpy as np

# We run the pure Python version first: primes_py.py
pp_time = timeit.timeit('primes(1000)',
                        'from primes_py import primes',
                        number=10) / 10. * 1000
print("Pure Python: {:.3f} ms".format(pp_time))

# We run the jitted Python version: primes_py_jit.py
pp_time = timeit.timeit('primes(1000)',
                        'from primes_py_jit import primes',
                        number=10) / 10. * 1000
print("Python JIT: {:.3f} ms".format(pp_time))

# Finally, we run the "full Cython" version: primes_cy.pyx
fc_timer = timeit.Timer('primes(1000)', 'from primes_cy import primes')
n_exec = 1000
fc_times = np.array(fc_timer.repeat(repeat=5, number=n_exec)) / n_exec * 1000
print("Full Cython: {:.3f} ms".format(min(fc_times)))

# Finally, CPP via Cython
fc_timer = timeit.Timer('primes(1000)', 'from primes import primes')
n_exec = 1000
fc_times = np.array(fc_timer.repeat(repeat=5, number=n_exec)) / n_exec * 1000
print("C++ via Cython: {:.3f} ms".format(min(fc_times)))

