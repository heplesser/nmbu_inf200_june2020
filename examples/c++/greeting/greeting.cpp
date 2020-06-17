/*
  hils.cpp:
  Hils en person med navn

  Autor: Hans Ekkehard Plesser
  Epost: hans.ekkehard.plesser
  Kilde: Basert paa Koenig/Moo, kap 0
  Dato : 2006-02-08
 */

#include <iostream>
#include <string>


int main()
{
  // be om brukerens navn
  std::cout << "Tast inn fornavnet ditt: ";

  // les navnet
  std::string navn;     // definer `navn'
  std::cin >> navn;     // les inn til `navn'

  // skriv ut hilsen
  std::cout << "Hei " << navn  << "!" << std::endl;

  return 0;
}
