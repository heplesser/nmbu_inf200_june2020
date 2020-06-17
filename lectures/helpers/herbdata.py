# -*- coding: utf-8 -*-

"""
- The file contains only data for animals that died before the end of the simulation time.
    - Animals are ordered by year of death
- Dictionary with the following NumPy arrays
    - `cycle`: simulation cycle/year
    - `age`, `weight`, `fitness`: animal's age, weight, fitness in given year
- All four arrays have the same size
- Each column corresponds to one animal
    - Each entry is data at end of year
    - First entry `age` column is always 1
    - First entry in `weight` column is $w_0(1-\eta)$ where $w_0$ is the actual birthweight
    - All entries after the animals death are NaN.

#### Filter data
- Keep only animals born after year 50, when we are in stationary state
- Create masked arrays excluding the NaN values
- For safety's sake check that all arrays have the same mask

- The file contains only data for animals that died before the end of the simulation time.
    - Animals are ordered by year of death
- Dictionary with the following NumPy arrays
    - `cycle`: simulation cycle/year
    - `age`, `weight`, `fitness`: animal's age, weight, fitness in given year
- All four arrays have the same size
- Each column corresponds to one animal
    - Each entry is data at end of year
    - First entry `age` column is always 1
    - First entry in `weight` column is $w_0(1-\eta)$ where $w_0$ is the actual birthweight
    - All entries after the animals death are NaN.


"""

__author__ = 'Hans Ekkehard Plesser'
__email__ = 'hans.ekkehard.plesser@nmbu.no'

import pickle
from numpy import ma
import numpy as np
from collections import Counter


def q(sgn, x, xhalf, phi):
    return 1. / (1. + np.exp(sgn * phi * (x - xhalf)))


def Phi(a, w, p):
    return (q(+1, a, p['a_half'], p['phi_age'])
            * q(-1, w, p['w_half'], p['phi_weight']))


class HerbData:
    """Represents one Herbivore simulation experiment."""

    def __init__(self, fname, params, yr_min=100, yr_max=400):
        """All animal data from years [yr_min, yr_max)."""

        # Load raw data from detailed logger
        self._d = pickle.load(open(fname + '.pkl', 'rb'))
        if self._d['cycle'][0, self._d['alive']].min() <= yr_max:
            raise ValueError('Some traces incomplete, reduce yr_max!')

        # Prepare masked data with complete years
        y = ma.masked_invalid(self._d['cycle'])
        a = ma.masked_invalid(self._d['age'])
        w = ma.masked_invalid(self._d['weight'])
        f = ma.masked_invalid(self._d['fitness'])
        a_death = a.max(axis=0).ravel()  # keep full year-of-death information
        with np.errstate(invalid='ignore'):
            excl = (self._d['cycle'] < yr_min) | (yr_max <= self._d['cycle'])
        for d in [y, a, w, f]:
            d[excl] = ma.masked

        # Keep only columns which contain at least one valid entry
        # Columns for animals alive before yr_min, the first entries are invalid
        ix_valid = np.argwhere(~np.all(a.mask, axis=0)).ravel()
        self.y_all = y[:, ix_valid]
        self.a_all = a[:, ix_valid]
        self.w_all = w[:, ix_valid]
        self.f_all = f[:, ix_valid]
        self.n_all = len(ix_valid)
        self.a_death_all = a_death[ix_valid].ravel()

        # Compressed version simplify some operations (1d, only valid values)
        self.yc_all = self.y_all.compressed()
        self.ac_all = self.a_all.compressed()
        self.wc_all = self.w_all.compressed()
        self.fc_all = self.f_all.compressed()
        if not np.isclose(Phi(self.ac_all, self.wc_all, params), self.fc_all).all():
            raise ValueError('Inconsistent fitness values')

        # Pick all births: Start with age 1 (initial entries invalid for animals born before yr_min)
        self._in_b = (~self.a_all.mask[0, :] & (self.a_all[0, :] == 1)).ravel()
        self.ix_b = np.argwhere(self._in_b).ravel()
        self.wb = self.w_all[0, self.ix_b].compressed() / (1 - params['eta'])
        self.n_birth = len(self.wb)

        # Pick all deaths: Location given by largest age
        self.ix_d = np.argwhere(self.a_all.max(axis=0) == self.a_death_all).ravel()  # death is before yr_max
        self._ax_d = self.a_all.argmax(axis=0).ravel()  # row location of death event
        self.n_death = len(self.ix_d)
        self.ad = np.fromiter((self.a_all[self._ax_d[ix], ix] for ix in self.ix_d),
                              float, self.n_death)
        self.wd = np.fromiter((self.w_all[self._ax_d[ix], ix] for ix in self.ix_d),
                              float, self.n_death)
        self.fd = np.fromiter((self.f_all[self._ax_d[ix], ix] for ix in self.ix_d),
                              float, self.n_death)

        # Count number of animals alive in any given year right after birth
        self.cnt_y = np.arange(yr_min, yr_max)
        self.cnt_all = np.zeros_like(self.cnt_y)
        for yr, cnt in Counter(self.yc_all).items():
            self.cnt_all[int(yr)-yr_min] = cnt

        # Now reduce to data from animals which are alive after death has occurred
        # Need to invalidate all animals that have died in a given year
        yu = self.y_all.copy()
        au = self.a_all.copy()
        wu = self.w_all.copy()
        fu = self.f_all.copy()
        for yix in self.ix_d:
            yu[self._ax_d[yix], yix] = ma.masked  # mask entries of animals dying in a given year
            au[self._ax_d[yix], yix] = ma.masked
            wu[self._ax_d[yix], yix] = ma.masked
            fu[self._ax_d[yix], yix] = ma.masked

        # Strip entirely masked columns
        ix_survive = np.argwhere(~np.all(yu.mask, axis=0)).ravel()
        self.y_srv = yu[:, ix_survive]
        self.a_srv = au[:, ix_survive]
        self.w_srv = wu[:, ix_survive]
        self.f_srv = fu[:, ix_survive]
        self.n_srv = len(ix_survive)
        self.a_death_srv = a_death[ix_survive].ravel()

        # Compressed versions
        self.yc_srv = self.y_srv.compressed()
        self.ac_srv = self.a_srv.compressed()
        self.wc_srv = self.w_srv.compressed()
        self.fc_srv = self.f_srv.compressed()

        # Count number of animals alive at end of any given year, after deaths
        self.cnt_srv = np.zeros_like(self.cnt_y)
        for yr, cnt in Counter(self.yc_srv).items():
            self.cnt_srv[int(yr)-yr_min] = cnt

        # Create cohort data: select animals born in yr_min, yr_max for whom we have
        # full life history 
        age_max = self.a_all.max()
        with np.errstate(invalid='ignore'):
            full_life = (self.a_all[0, :] == 1) & (self.y_all[0, :] < yr_max-age_max)
        self.y_coh = self.y_all[:, full_life]
        self.a_coh = self.a_all[:, full_life]
        self.w_coh = self.w_all[:, full_life]
        self.f_coh = self.f_all[:, full_life]

        # Compressed versions
        self.yc_coh = self.y_coh.compressed()
        self.ac_coh = self.a_coh.compressed()
        self.wc_coh = self.w_coh.compressed()
        self.fc_coh = self.f_coh.compressed()

        # Compute total animal mass for each year
        self.tot_w_all = np.zeros_like(self.cnt_y)
        self.tot_w_srv = np.zeros_like(self.cnt_y)
        for k, yr in enumerate(self.cnt_y):
            self.tot_w_all[k] = self.wc_all[self.yc_all == yr].sum()
            self.tot_w_srv[k] = self.wc_srv[self.yc_srv == yr].sum()

        # Load raw data from CSV file, just herbivore counts
        self._c = np.loadtxt(fname + '.csv', delimiter=',')
        ixy = (yr_min <= self._c[:, 0]) & (self._c[:, 0] < yr_max)
        self.csv_y = self._c[ixy, 0]
        self.csv_n = self._c[ixy, 1]

        # Consistency check
        assert (self.csv_y == self.cnt_y).all()
        assert (self.csv_n == self.cnt_srv).all()




if __name__ == '__main__':
    hp = {'w_birth': 8.,
          'sigma_birth': 1.5,
          'beta': 0.9,
          'eta': 0.05,
          'a_half': 40.,
          'phi_age': 0.6,
          'w_half': 10.,
          'phi_weight': 0.1,
          'mu': 0.25,
          'gamma': 0.2,
          'zeta': 3.5,
          'xi': 1.2,
          'omega': 0.4,
          'F': 10.,
          'f_max': 800.}

    h = HerbData('../data_j06/mono_hol_7442342', params=hp)