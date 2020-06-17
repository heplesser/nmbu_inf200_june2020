#ifndef DYR_H
#define DYR_H

/*
  Eksempelklasse: et dyr

  Hans Ekkehard Plesser, 2003-03-10, 2006-04-03

  Definisjon av klassen Dyr
*/

class Dyr {

public:

  // konstruktør: dyret må skapes med vekt
  Dyr(double vekt = v_fod_) : vekt_(vekt) {} 

  ~Dyr() {}  // destruktør

  // lever tilbake hvor mye du har spist
  double spis(double mat = 0);
  void slank();
  double hent_vekt() const { return vekt_; }

  bool dor() const;   // true hvis dyret doer
  bool gaar() const;  // true hvis dyret vil gaa


  // static member function: fct for hele klasse
  static void sett_param(double v_fod, double v_tap, double F, double mu);

private:

  double vekt_;  // medlemsvariable til enkeltdyr
   
  // klassevariabler, gjelder alle dyr
  static double v_tap_;   // aarlig vekttap
  static double v_fod_;   // foedevekt
  static double F_;       // oensket aarlig matmengde
  static double mu_;      // parameter for mobilitet
};

#endif

