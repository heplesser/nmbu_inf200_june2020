# distutils: language = c++
# distutils: sources = cpp_primes.cpp

from libcpp.vector cimport vector

cdef extern from "cpp_primes.h":
    vector[int] cpp_primes(int n_primes)

cpdef primes(n_primes):
    return cpp_primes(n_primes)
