/*
  A program illustrating inheritance

  Programmet viser en endimensjonal verden med
  tre landskapstyper, men uten bevegelse.

  Hans Ekkehard Plesser, 2003-03-25, 2006-04-03
*/

#include <cstdlib>
#include <iomanip>
#include <iostream>
#include <string>
#include <vector>

#include "random.h"
#include "dyr.h"
#include "sted.h"

using namespace std;

typedef vector<Sted*> lp_vec;

int main(int argc, char *argv[])
{
  
  if ( argc != 5 ) {
    cout << "\n Bruk: biotop verden nDyr nAar froe\n" << endl;
    return -1;
  }

  string geography(argv[1]);
  unsigned int n_dyr = atoi(argv[2]);
  unsigned int n_year = atoi(argv[3]);

  toolbox::randomGen(atoi(argv[4])); // seed

  // build world from geography string:
  // each character in the string is one cell
  // initialize with zero-pointers
  lp_vec verden(geography.size(), 0);

  for ( unsigned int c = 0 ; c < geography.size() ; ++c )
    {
      switch ( geography[c] ) {
      case 'H':
	verden.at(c) = new Hus(c);
	break;
      case 'B':
	verden.at(c) = new Beite(c);
	break;
      case 'P':
	verden.at(c) = new Pplass(c);
	break;
      default:
	cout << "\nError: geography description can only contain H, B, P\n"
	     << endl;
	return -2;
	break;
      }
    }

  // set class parameters
  Dyr::sett_param(5, 0.5, 10, 0.2);

  // fill cells with animals
  for ( auto cell : verden )
    {
      auto n = toolbox::randomGen().nrand(n_dyr+1);
      for ( unsigned int j = 0 ; j < n ; ++j )
	{
	  Dyr *newdyr = new Dyr;
	  if ( not cell->plasser(newdyr) )
	    delete newdyr;
	}
    }

  // simulate
  unsigned int year = 0;
  cout << endl;

  do {

    // print out year and number of animals in each cell
    cout << setw(3) << year << " : ";

    unsigned int total = 0;
    for ( auto cell : verden )
      {
	cout << setw(3) << cell->antall_dyr();
	total += cell->antall_dyr();
      }

    cout << "   [" << setw(3) << total << "]" << endl;

    // mating, doed
    for ( auto cell : verden )
      cell->mat();

    for ( auto cell : verden )
      cell->dod();
    
    ++year;

  } while ( year < n_year );

  cout << "\nHa det bra!\n" << endl;
  
  return 0;

}
