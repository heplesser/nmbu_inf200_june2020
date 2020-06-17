#ifndef RANDOM_H
#define RANDOM_H

/** @file random.h
    Tools for random number generation.
    
    This file contains tool for the generation of random numbers.

    This file is part of BioSim.

    (C) 2003-2006 Hans Ekkehard Plesser <hans.ekkehard.plesser@umb.no>

    This file is public software under GPL2.

*/

#include <cstdlib>
#include <stdexcept>

/** @defgroup toolbox The Biosim Toolbox.
    This group collects all toolbox classes provided for the BioSim project.
*/

/** Namespace for all toolbox functions.
    @ingroup toolbox
 */

namespace toolbox {

  /** Random generator for use with BioSim.
      This class provides a comfortable random generator interface for the
      BioSim project. If the generator itself should be updated later, the
      BioSim software need not be changed, since the interface does not
      change.  The random generator should be used like this:

      @code
      #include "random.h"
      using toolbox::randomGen;

      int main()
      {
        unsigned int seed = 0;
        cin >> seed;
        randomGen(seed);  // seed random generator

        for ( int j = 0 ; j < 5 ; ++j )
          cout << randomGen().drand() << ' '   // [0,1) double tall
               << randomGen().nrand(3)         // tall fra {0, 1, 2, 3} 
               << endl;

        return 0;
      }
      @endcode

      @c randomGen() is a function declared in @c random.h.

      @note RandomGenerator employs the Singleton pattern (Meyers
      Singleton) to ensure that there is exactly one RNG instance per
      program, and that there is a single, globally accessible access
      point to this instance. Some additional checks are added to
      handle seeding gracefully, but safe.  This may reduce in loss of
      efficiency.

      @see For more on the Singleton pattern, see
      - Scott Meyers, More Effective C++, ch. 26, Addison-Wesley 1996
      - Erich Gamma et al, Design Patterns, pp 127ff, Addison-Wesley 1994
      - Andrei Alexandrescu, Modern C++ Design, ch. 6, Addison-Wesley 2001

      @todo Check out how much performance we loose through this
      carefully controlled singleton setup.

      @note RandomGenerator presently wraps the system RNG. This is a bad
      idea generally. Replace with something better (eg Mersenne-Twister)
      before using the RandomGenerator class for serious research.

      @see The NEST simulator's librandom for a very flexible RNG interface
      (http://www.nest-initiative.org).

      @ingroup toolbox
  */

  class RandomGenerator {

  public:
    
    //! Draw random number uniformly distributed on \f$[0, 1)\f$
    double drand();

    /** Draw integer random number uniformly distributed on \f$[0, n)\f$
	@param n Upper limit, not include: numbers are chosen from 0, 1, ..., n-1
	@throws domain_error if n is out of range
    */
    unsigned int nrand(unsigned int n);

    /** Access function.
	@see Meyers, More Exceptional C++, Item 26, p 130, AW, 1996.
    */
    friend RandomGenerator& randomGen(unsigned int seed);

  private:

    /** Create generator with given seed.
	@param seed Seed value for the generator.
	@throws domain_error if seed is out of range
	@note No re-seeding is possible.
	@note Private as consequence of singleton pattern.
    */
    RandomGenerator(unsigned int seed); 

    /// @note prohibit copying by making copy constructor private
    RandomGenerator(const RandomGenerator&);

    /// @note prohibit assignment by making operator private
    RandomGenerator& operator=(const RandomGenerator&);
    
    /// @note Private as consequence of singleton pattern.
    ~RandomGenerator() {}

  }; // class RandomGenerator


  // -- Access function --------------------------------------------

  /** Function providing access to the random generator.
      This function provides controlled access to the single random
      generator instance. On first call, the generator is created as a
      static function variable. This first call MUST be with a seed
      value as argument. The seed MUST differ from 0. All later calls
      MUST be without argument.
      @param seed non-zero, to be used on first call only
      @throw logic_error if called without seed on first call or with
      seed on later calls
      @see Meyers, More Exceptional C++, Item 26, p 130, AW, 1996.
  */
  RandomGenerator& randomGen(unsigned int seed = 0);

} // namespace toolbox 


// -- RandomGenerator function definitions -----------------------

/*
  All random generator functions are implemented inline, except the constructor.
*/

inline
double toolbox::RandomGenerator::drand() 
{
  unsigned int r;

  // rand() returns within [0, RAND_MAX], we want [0, 1)
  do {
    r = std::rand();
  } while ( r == RAND_MAX );  

  return r / static_cast<double>(RAND_MAX);
}

inline
unsigned int toolbox::RandomGenerator::nrand(unsigned int n) 
{
  if ( n > RAND_MAX )
    throw std::domain_error("toolbox::RandomGenerator::nrand(): Argument is out of range.");

  // see ACC++, sec 7.4.4
  const unsigned int scale = RAND_MAX / n;

  unsigned int r;

  do {
    r = std::rand() / scale;
  } while (r >= n); 

  return r;
}

#endif
