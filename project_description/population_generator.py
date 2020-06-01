# -*- coding: utf-8 -*-

'''
:mod:`biosim.population_generator` generates several populations of animals
with age and weight randomly distributed and returns a list of dictionaries
with the animals and the coordinates they are to be put.

The user can define:
#. The number of each species that are put on every defined coordinate
#. The coordinates that the animals in that species should occupy

If different sizes of the population within an species is preferable,
the user can simply make another population and add it to the island

Example of list returned:
-------------------------
::

    [{'loc': (3,4),
      'pop': [{'species': 'Herbivore', 'age': 10, 'weight': 15},
              {'species': 'Herbivore', 'age': 5, 'weight': 40},
              {'species': 'Herbivore', 'age': 15, 'weight': 25}]},
     {'loc': (4,4),
      'pop': [{'species': 'Herbivore', 'age': 2, 'weight': 60},
              {'species': 'Herbivore', 'age': 9, 'weight': 30},
              {'species': 'Herbivore', 'age': 16, 'weight': 14}]},
     {'loc': (4,4),
      'pop': [{'species': 'Carnivore', 'age': 3, 'weight': 35},
              {'species': 'Carnivore', 'age': 5, 'weight': 20},
              {'species': 'Carnivore', 'age': 8, 'weight': 5}]}]

'''

__author__ = "Ragnhild Smistad, UMB and Toril Fjeldaas Rygg, UMB"

import numpy.random as nprand

class Population(object):
    '''
    The population on the island
    '''
    def __init__(self, n_herbivores=None, coord_herb=None,
                 n_carnivores=None, coord_carn=None):
        '''
        ==============    ==============================================
        *n_herbivores*    The number of herbivores in each coordinate
        *coord_herb*      A list of the different coordinates(tuple)
        *n_carnivores*    The number of carnivores in each coordinate
        *coord_carn*      A list of the different coordinates as tuple
        ==============    ==============================================
        '''
        self.animals = []
        self.n_herb = n_herbivores
        self.n_carn = n_carnivores
        self.coord_herb = coord_herb
        self.coord_carn = coord_carn

    def get_animals(self):
        '''
        Returns a complete list of dictionaries with a population for
        every coordinate defined.
        '''
        if self.n_herb:
            for coord in self.coord_herb:
                self.animals.append({'loc': coord,
                                     'pop': []})

                for _ in range(self.n_herb):
                    self.animals[-1]['pop'].append({'species': 'Herbivore',
                                        'age': nprand.randint(0, 20),
                                        'weight': nprand.randint(5, 80)})

        if self.n_carn:
            for coord in self.coord_carn:
                self.animals.append({'loc': coord,
                                     'pop': []})
                for _ in range(self.n_carn):
                    self.animals[-1]['pop'].append({'species': 'Carnivore',
                                        'age': nprand.randint(0, 10),
                                        'weight': nprand.randint(3, 50)})
        return self.animals
