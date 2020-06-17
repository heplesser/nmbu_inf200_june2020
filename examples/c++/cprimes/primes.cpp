/*
 * primes.cpp
 *
 *  Created on: Jan 18, 2013
 *      Author: plesser
 */

#include <iostream>    // for output
#include <iomanip>     // for setting the number of digits on output

#include <vector>      // for vector data type

#include <ctime>       // for taking time
#include <limits>      // for finding the largest possible double value


std::vector<int> primes(int n_primes)
{
  std::vector<int> primes(n_primes);

  int k = 0;  // number of primes found so far
  int n = 2;  // next candidate to test for primality

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


int main()
{
  const int num_reps = 5;
  const int num_runs = 1000;

  double t_min = std::numeric_limits<double>::max();

  for ( int rep = 0 ; rep < num_reps ; ++rep )
  {
    std::clock_t tic = std::clock();

    for ( int runs = 0 ; runs < num_runs ; ++runs )
      primes(1000);

    std::clock_t toc = std::clock();

    double t_sec = (toc - tic) /
      (static_cast<double>(num_runs) * CLOCKS_PER_SEC) * 1000;

    if ( t_sec < t_min )
      t_min = t_sec;
  }

  std::cout << std::fixed << std::setprecision(3)
	    << "Time per 1000 primes: "
	    << t_min << "ms" << std::endl;

  return 0;
}
