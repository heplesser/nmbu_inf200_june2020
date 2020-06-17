/*
  Eksempel for klasse med ikke-triviell destruktør

  Eksempel for arv og polymorfi med foelgende klassestruktur:

                          Sted
                            |
                ------------------------
		|           |          |
               Hus        Beite     Pplass


  Hans Ekkehard Plesser, 2003-03-10, 2006-04-03
*/

#include <list>
#include "dyr.h"

class Sted {

public:
  
  // ingen default-verdi for x, kan ikke skape Sted uten
  // å oppgi koordinate
  Sted(unsigned x) : x_(x) {}

  // destruktør: må avlive alle dyr på stedet
  virtual ~Sted();
  
  /* plasser dyr på stedet
     returnerer true hvis dyret ble tatt imot
     omdefiner i klasser som ikke tar imot dyr
  */
  virtual bool plasser(Dyr*);  

  unsigned antall_dyr() const { return dyr_.size(); }

  void dod();

  /* Mat dyrene.
     Hvordan matingen foregaar, er helt avhengig av de
     konkrete klassene, saa vi definerer funksjonen som
     pure virtual.
  */
  virtual void mat() =0;


protected:  // tilgjengelig for deriverte klasser
  std::list<Dyr*> dyr_;

private:
  
  // Vi oensker ikke kopi av steder, saa vi forbyr dem simpelthen
  // ved aa gjoere kopi- og tilordningsoperatorer privat
  Sted(const Sted&);
  Sted& operator=(const Sted&);

  unsigned       x_;      // x-koordinate

};

// -------------------------------------------

// Hus: dyr kan ikke vaere her
class Hus : public Sted {
public:
  Hus(unsigned x) : Sted(x) {}

  bool plasser(Dyr*);
  void mat();
};

// Beite: dyr kan vaere her og finne mat
class Beite : public Sted {
public:
  Beite(unsigned x) : Sted(x) {}

  // standard for plasser() holder
  void mat();
};

// Hus: dyr kan vaere her, men faar ikke mat
class Pplass : public Sted {
public:
  Pplass(unsigned x) : Sted(x) {}

  // standard for plasser() holder
  void mat();
};
