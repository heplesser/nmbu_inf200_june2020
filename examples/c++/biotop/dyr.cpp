#include <cmath>      // for exp
#include "dyr.h"   
#include "random.h"

// statiske data members må defineres et sted
double Dyr::v_tap_ = 0;
double Dyr::v_fod_ = 0;
double Dyr::F_     = 0;
double Dyr::mu_    = 0;

double Dyr::spis(double mat)
{
  double spist;
  if ( mat < F_ )
    spist = mat;
  else 
    spist = F_;

  vekt_ += spist;

  return spist;
}

void Dyr::slank()
{
  vekt_ *= v_tap_;
}

bool Dyr::dor() const
{
  return toolbox::randomGen().drand() < 1 - std::exp(-0.1 * vekt_);
}

bool Dyr::gaar() const
{
  return toolbox::randomGen().drand() < mu_;
}

void Dyr::sett_param(double v_tap, double v_fod, double F, double mu)
{
  v_tap_ = v_tap;
  v_fod_ = v_fod;
  F_ = F;
  mu_ = mu;
}
