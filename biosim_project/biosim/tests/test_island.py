# -*- Utf-8 -*-

import nose.tools as nt
import numpy as np
from biosim.island import Island
from biosim.animals import Herbivore, Carnivore
from biosim.landscape import Jungle, Savannah

__author__ = 'Marius Kristiansen'
__email__ = 'mariukri@nmbu.no'


class TestIsland:
    geogr_simple = """OMO
                      OJD
                      OSO"""

    def __init__(self):
        """
        Saves parameter values
        """
        self.true_params_jungle = Jungle.params
        self.true_params_savannah = Savannah.params
        self.true_params_herbivore = Herbivore.params
        self.true_params_carnivore = Carnivore.params
        self.island = None

    def setup(self):
        self.island = Island(self.geogr_simple)
        self.island.build_map()
        for row in self.island.island:
            for cell in row:
                if cell.passable:
                    cell.herbivores = [Herbivore(weight=50) for _ in range(10)]
                    cell.carnivores = [Carnivore(weight=50) for _ in range(10)]

    def teardown(self):
        """
        Resets parameters to correct values
        """
        Jungle.params = self.true_params_jungle
        Savannah.params = self.true_params_savannah
        Herbivore.params = self.true_params_herbivore
        Carnivore.params = self.true_params_carnivore

    def test_map_build(self):
        """
        Test that the island properly allocates cell types according to input
        """
        nt.assert_equal(self.island.island[1][1].__class__.__name__, "Jungle")
        nt.assert_equal(self.island.island[0][1].__class__.__name__, "Mountain")
        nt.assert_equal(self.island.island[2][1].__class__.__name__, "Savannah")
        nt.assert_equal(self.island.island[1][2].__class__.__name__, "Desert")

    def test_food_growth(self):
        """
        Test that food grows in each cell
        """
        new = []
        true_values = [0, 0, 0, 0, 800, 0, 0, 230, 0]
        self.island.build_map()
        self.island.feeding()
        self.island.grow()
        for row in self.island.island:
            for cell in row:
                new.append(cell.available_food_herb)
        for index in range(9):
            nt.assert_equal(new[index], true_values[index])

    def test_food_decrease(self):
        """
        Test that the total amount of food on island decreases
        """
        total_food = 0
        new_food = 0
        for row in self.island.island:
            for cell in row:
                total_food += cell.available_food_herb
        self.island.feeding()
        for row in self.island.island:
            for cell in row:
                new_food += cell.available_food_herb
        nt.assert_less(new_food, total_food)

    def test_weight_increase(self):
        """
        test that the weight of herbivores increase
        (sets number of carnivores to 0 to avoid them reducing herbivore numbers
        """
        new = 0
        original = 1500
        self.island.feeding()
        for row in self.island.island:
            for cell in row:
                cell.carnivores = []
                for herbivore in cell.herbivores:
                    new += herbivore.weight
        nt.assert_greater(new, original)

    def test_procreation(self):
        """
        Test that the number of animals increase
        :return:
        """
        Herbivore.set_parameters({"gamma": 1})
        Carnivore.set_parameters({"gamma": 1})
        original = 60
        new = 0
        self.island.procreation()
        for row in self.island.island:
            for cell in row:
                new += \
                    cell.number_of_individuals()["herbivores"] + \
                    cell.number_of_individuals()["carnivores"]
        nt.assert_greater(new, original)
        nt.assert_less_equal(new, original * 2)

    def test_age(self):
        """
        Test that average age per cell increases
        """
        original = 0
        new = []
        self.island.aging()
        for row in self.island.island:
            for cell in row:
                new.append(
                    cell.avg_age()[0] if cell.avg_age()[0] is not None else 0)
                new.append(
                    cell.avg_age()[1] if cell.avg_age()[1] is not None else 0)
        average = np.sum(new) / 6.
        nt.assert_greater(average, original)

    @staticmethod
    def test_surrounding_cells():
        """
        Test that the function surrounding cells returns the right cells
        """
        island = Island("JJJJJJ\nJJJJJJ\nJJJJJJ\nJJJJJJ\nJJJJJJ\nJJJJJJ")
        island.build_map()
        cor = island.surrounding_cells((5, 5))
        true = [(4, 5), (5, 4), (5, 6), (6, 5)]
        for index in range(len(cor)):
            nt.assert_equal(cor[index], true[index])

    @staticmethod
    def test_surrounding_cells_2():
        """
        Tests that no surrounding cells is returned if all are mountain and
        ocean
        """
        island = Island("OOO\nOJM\nMMM")
        island.build_map()
        cor = island.surrounding_cells((1, 1))
        nt.assert_list_equal(cor, [])

    def test_death(self):
        """
        Runs multiple times to minimise chance of failure due to all animals
         surviving.
        :return:
        """
        original = 40 * 5
        new = 0
        test = Island(self.geogr_simple)
        test.build_map()
        Herbivore.set_parameters({"omega": 1})
        Carnivore.set_parameters({"omega": 1})
        test.island[1][1].herbivores = [Herbivore() for _ in range(10)]
        test.island[1][2].herbivores = [Herbivore() for _ in range(10)]
        test.island[1][1].carnivores = [Carnivore() for _ in range(10)]
        test.island[1][2].carnivores = [Carnivore() for _ in range(10)]
        test.death()
        for _ in range(5):
            for row in test.island:
                for cell in row:
                    new += \
                        cell.number_of_individuals()["herbivores"] + \
                        cell.number_of_individuals()["carnivores"]
        nt.assert_less(new, original)

    def test_one_year(self):
        """
        tests that attributes changes after a year
        """
        island = Island(self.geogr_simple)
        island.build_map()
        Herbivore.set_parameters({"mu": 0})
        Carnivore.set_parameters({"mu": 0})
        island.island[1][1].herbivores = [Herbivore(40, 5)]
        island.island[1][1].carnivores = [Carnivore(20, 5)]
        for carnivore in island.island[1][1].carnivores:
            carnivore.fitness = 1
        for herbivore in island.island[1][1].herbivores:
            herbivore.fitness = 1
        island.one_year()
        nt.assert_equal(island.island[1][1].herbivores[0].age, 6)
        nt.assert_equal(island.island[1][1].carnivores[0].age, 6)
        nt.assert_not_equal(island.island[1][1].herbivores[0].weight, 40)
        nt.assert_not_equal(island.island[1][1].carnivores[0].weight, 20)


class TestMigration:
    geogr_simple = """OMO
                  OJD
                  OSO"""

    def __init__(self):
        """
        Saves parameter values
        """
        self.true_params_jungle = Jungle.params
        self.true_params_savannah = Savannah.params
        self.true_params_herbivore = Herbivore.params
        self.true_params_carnivore = Carnivore.params
        self.island = None

    def setup(self):
        self.island = Island(self.geogr_simple)
        self.island.build_map()
        for row in self.island.island:
            for cell in row:
                if cell.passable:
                    cell.herbivores = [Herbivore(weight=50) for _ in range(10)]
                    cell.carnivores = [Carnivore(weight=50) for _ in range(10)]

    def teardown(self):
        """
        Resets parameters to correct values
        """
        Jungle.params = self.true_params_jungle
        Savannah.params = self.true_params_savannah
        Herbivore.params = self.true_params_herbivore
        Carnivore.params = self.true_params_carnivore

    def test_animals_must_migrate(self):
        """
        Tests that no animals are left in cell after migration
        """
        Herbivore.set_parameters({"mu": 1})
        Carnivore.set_parameters({"mu": 1})
        island = Island(self.geogr_simple)
        island.build_map()
        island.island[1][1].herbivores = [Herbivore() for _ in range(20)]
        island.island[1][1].carnivores = [Carnivore() for _ in range(20)]
        for herb in island.island[1][1].herbivores:
            herb.fitness = 1
        for carn in island.island[1][1].carnivores:
            carn.fitness = 1
        island.migration()
        nt.assert_equal(island.island[1][1].herbivores, [])
        nt.assert_equal(island.island[1][1].carnivores, [])

    def test_num_animal_is_not_change(self):
        """
        Tests that the total number of animals are the same after migration
        """
        initial_num_animals = 20
        island = Island(self.geogr_simple)
        island.build_map()
        island.island[1][1].herbivores = [Herbivore() for _ in range(10)]
        island.island[1][1].carnivores = [Carnivore() for _ in range(10)]
        for herb in island.island[1][1].herbivores:
            herb.set_parameters({"mu": 1})
            herb.fitness = 1
        for carn in island.island[1][1].carnivores:
            carn.set_parameters({"mu": 1})
            carn.fitness = 1
        island.migration()
        total_num_animals = 0
        for row in island.individuals():
            for cell in row:
                total_num_animals += (cell["herbivores"] + cell["carnivores"])
        nt.assert_equal(total_num_animals, initial_num_animals)

    def test_no_animals_migrate(self):
        """
        Test that nothing change if no animal migrate
        """
        initial_num_animals = 20
        island = Island(self.geogr_simple)
        island.build_map()
        island.island[1][1].herbivores = [Herbivore() for _ in range(10)]
        island.island[1][1].carnivores = [Carnivore() for _ in range(10)]
        for herb in island.island[1][1].herbivores:
            herb.set_parameters({"mu": 0})
        for carn in island.island[1][1].carnivores:
            carn.set_parameters({"mu": 0})
        island.migration()
        total_animals = len(island.island[1][1].herbivores +
                            island.island[1][1].carnivores)
        nt.assert_equal(total_animals, initial_num_animals)
        total_num_animals = 0
        for row in island.individuals():
            for cell in row:
                total_num_animals += (cell["herbivores"] + cell["carnivores"])
        nt.assert_equal(total_num_animals, initial_num_animals)

    def test_relative_food_updates(self):
        """
        Tests that relative food in surrounding cells are updated after each
        year
        """
        island = Island(self.geogr_simple)
        island.build_map()
        island.island[1][1].herbivores = [Herbivore() for _ in range(10)]
        island.island[1][1].carnivores = [Carnivore() for _ in range(10)]
        for herb in island.island[1][1].herbivores:
            herb.set_parameters({"mu": 1})
            herb.fitness = 1
        for carn in island.island[1][1].carnivores:
            carn.set_parameters({"mu": 1})
            carn.fitness = 1
        initial_relative_food_carn = island.island[1][1].relative_food_herb()
        initial_relative_food_herb = island.island[1][1].relative_food_carn()
        island.migration()
        nt.assert_not_equal(initial_relative_food_carn,
                            island.island[1][1].relative_food_carn())
        nt.assert_not_equal(initial_relative_food_herb,
                            island.island[1][1].relative_food_herb())

    def test_list_of_coordinates(self):
        """
        Tests that shuffled_list function returns coordinates for all cells on
        map.
        """
        list_ = self.island.shuffle_coordinates()
        for row in range(len(self.island.island)):
            for cell in range(len(self.island.island[row])):
                nt.assert_in((cell, row), list_)

    def test_list_is_shuffled(self):
        """
        Tests that the list of coordinate from shuffled_list function is
        shuffled
        """
        sorted_list = []
        shuffled_list = self.island.shuffle_coordinates()
        for row in range(len(self.island.island)):
            for cell in range(len(self.island.island[row])):
                sorted_list.append((row, cell))
        nt.assert_not_equal(shuffled_list, sorted_list)

    def test_length_surrounding_cells(self):
        """
        Tests that surrounding cells does not give coordinates of ocean or
        mountain cells
        """
        cell = self.island.surrounding_cells((1, 2))
        nt.assert_equal(cell, [(1, 1)])
        cells = self.island.surrounding_cells((1, 1))
        correct_cells = [(2, 1), (1, 2)]
        nt.assert_equal(cells, correct_cells)
