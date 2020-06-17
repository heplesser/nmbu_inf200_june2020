#include "random.h"
#include <cstdlib>
#include <stdexcept>

toolbox::RandomGenerator::RandomGenerator(unsigned int seed)
{
  if ( seed > RAND_MAX )
    throw std::domain_error("toolbox::RandomGenerator::RandomGenerator(): Argument is out of range.");

  srand(seed);
}

toolbox::RandomGenerator& toolbox::randomGen(unsigned int seed)
{
  static bool seeded = false;

  // ensure rng is seeded on first call
  if ( !seeded && seed == 0 )
    throw std::logic_error("toolbox::randomGen(): rng must be seeded on first call.");

  // the one and only RandomGenerator instance
  // is constructed first time we pass here
  static RandomGenerator rng(seed);  

  // ensure function was called without argument later
  // NOTE: we set seeded only at end, so on first call, this will not throw
  if ( seeded && seed != 0 )
    throw std::logic_error("toolbox::randomGen(): rng must be seeded on first call ONLY.");
  
  seeded = true;

  return rng;
}
