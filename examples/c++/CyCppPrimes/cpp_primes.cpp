#include "cpp_primes.h"

std::vector<int> cpp_primes(int n_primes)
{
  std::vector<int> primes(n_primes);
  
  int k = 0;
  int n = 2;
  
  while ( k < n_primes )
  {
    int i = 0;
    while ( i < k and n % primes[i] != 0 )
      ++i;
    if ( i == k )
    {
      primes[k] = n;
      ++k;
    }
    ++n;
  }

  return primes;
}

