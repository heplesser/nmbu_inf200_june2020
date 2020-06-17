#include "sted.h"

/* destrukt�r for sted: alle dyrene p� stedet m� "avlives"
   f�r pekerne til dyrene fjernes */

Sted::~Sted()
{
  for ( auto animal : dyr_ )
    delete animal;   // it er peker p� *it, *it er peker p� dyr
}

// -------------------------------------------

// standardversjon
bool Sted::plasser(Dyr *nytt_dyr)
{
  dyr_.push_back(nytt_dyr);
  return true;
}

// versjon for Hus: nekter aa ta imot
bool Hus::plasser(Dyr *)
{
  return false;
}

// -------------------------------------------

void Sted::dod()
{
  // OBS: ikke bruk for-l�kke her, it kan endre seg paa to maater i loekken!
  auto it = dyr_.begin();
  while ( it != dyr_.end() ) 
  {
    if ( (*it)->dor() ) 
    {
      delete *it;           // avliv dyret forst
      it = dyr_.erase(it);  // fjern pekeren til avlivete dyret
    }
    else
    {
      ++it;
    }
  }
}

// -------------------------------------------

void Hus::mat()
{
  // gjoer ingenting
  return;
}

void Beite::mat()
{
  for ( auto dyr : dyr_ )
    dyr->spis(50);
  return;
}

void Pplass::mat()
{
  // gjoer ingenting
  return;
}

// -------------------------------------------
