# -*- Utf-8 -*-

import nose.tools as nt
import numpy as np
from biosim.simulation import BioSim
from biosim.animals import Herbivore, Carnivore
from biosim.landscape import Savannah, Jungle

__author__ = 'Marius Kristiansen'
__email__ = 'mariukri@nmbu.no'


class TestSimulation(object):
    geo = """OOOOOOO
             OJJJJJO
             OJSMSJO
             OSDJDSO
             OJSMSJO
             OJJJJJO
             OOOOOOO"""

    def __init__(self):
        self.original_herb = Herbivore.params
        self.original_carn = Carnivore.params
        self.original_Jungle = Jungle.params
        self.original_Savannah = Savannah.params
        self.sim = None

    def setup(self):
        ini_carns = [{'loc': (5, 3),
                      'pop': [{'species': 'Carnivore',
                               'age': 5,
                               'weight': 20}
                     for _ in xrange(20)]}]

        ini_herbs = [{'loc': (3, 3),
                      'pop': [{'species': 'Herbivore',
                               'age': 5,
                               'weight': 20}
                     for _ in xrange(80)]}]

        ini_pop = ini_carns + ini_herbs
        self.sim = BioSim(self.geo, ini_pop, 123456)

    def teardown(self):
        Herbivore.params = self.original_herb
        Carnivore.params = self.original_carn
        Jungle.params = self.original_Jungle
        Savannah.params = self.original_Savannah

    def test_add_population(self):
        """
        Test that add_population function adds population in right cell with
        given weight and age.
        """
        num_carnivores = 5
        num_herbivores = 10
        herbs = [{'loc': (2, 2),
                  'pop': [{'species': 'Herbivore',
                           'age': 8,
                           'weight': 40}
                          for _ in xrange(num_herbivores)]}]
        carns = [{'loc': (2, 2),
                  'pop': [{'species': 'Carnivore',
                           'age': 7,
                           'weight': 30}
                          for _ in xrange(num_carnivores)]}]
        self.sim.add_population(herbs + carns)
        nt.assert_equal(num_carnivores,
                        len(self.sim.island.island[1][1].carnivores))
        nt.assert_equal(num_herbivores,
                        len(self.sim.island.island[1][1].herbivores))

        for carn in self.sim.island.island[1][1].carnivores:
            nt.assert_equal(carn.age, 7)
            nt.assert_equal(carn.weight, 30)
        for herb in self.sim.island.island[1][1].herbivores:
            nt.assert_equal(herb.age, 8)
            nt.assert_equal(herb.weight, 40)

        herbs_ = [{'loc': (2, 2),
                  'pop': [{'species': 'Herbivore',
                           'age': 8,
                           'weight': 40}]}]
        self.sim.add_population(herbs_)

    def test_heatmap(self):
        """
        Tests that heatmap makes array with correct number of herbivores.
        :return:
        """
        Carnivore.set_parameters({"gamma": 0, "omega": 0, "mu": 0})
        Herbivore.set_parameters({"gamma": 0, "omega": 0, "mu": 0})
        initial_herbivores = 80
        initial_carnivores = 20
        herbivores, carnivores = self.sim.heatmap(self.sim.island.one_year())
        nt.assert_equal(initial_carnivores, np.sum(carnivores))
        nt.assert_equal(initial_herbivores, np.sum(herbivores))

        nt.assert_equal(initial_herbivores, herbivores[2][2])
        nt.assert_equal(initial_carnivores, carnivores[4][2])

    @staticmethod
    def test_standard_arguments():
        """
        Tests that simulation works without any given arguments.
        """
        initial_herbivores = 150
        initial_carnivores = 40
        sim_ = BioSim()
        Carnivore.set_parameters({"gamma": 0, "omega": 0, "mu": 0})
        Herbivore.set_parameters({"gamma": 0, "omega": 0, "mu": 1})

        for row in sim_.island.island:
            for cell in row:
                for herb in cell.herbivores:
                    herb.fitness = 1
        sim_.island.migration()
        herbivores, carnivores = sim_.heatmap(sim_.island.one_year())
        nt.assert_equal(initial_carnivores, np.sum(carnivores))
        nt.assert_equal(initial_herbivores, np.sum(herbivores))

        nt.assert_equal(initial_carnivores, carnivores[2][2])

    def test_number_animals(self):
        """
        Tests that the animal function works
        """
        total = 100
        herbs = 80
        carns = 20
        animals = self.sim.animal()
        nt.assert_equal(herbs, animals["Herbivores"])
        nt.assert_equal(carns, animals["Carnivores"])
        nt.assert_equal(total, animals["Herbivores"] + animals["Carnivores"])
