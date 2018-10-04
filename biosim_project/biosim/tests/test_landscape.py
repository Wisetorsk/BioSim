# -*- Utf-8 -*-

from biosim.landscape import *
import nose.tools as nt

__author__ = 'Marius Kristiansen'
__email__ = 'mariukri@nmbu.no'


class TestClassHerb(object):
    """
    Tests for cell with only herbivores
    """

    def __init__(self):
        self.original_params_savannah = Savannah.params
        self.original_params_jungle = Jungle.params
        self.jungle = None
        self.savannah = None
        self.herb = None
        self.carn = None

    def setup(self):
        self.herb = [Herbivore() for _ in range(5)]
        self.savannah = Savannah(self.carn, self.herb)
        self.jungle = Jungle(self.carn, self.herb)

    def teardown(self):
        Savannah.params = self.original_params_savannah
        Jungle.params = self.original_params_jungle

    def test_food_savannah(self):
        """
        Test that savannah starts with 300 available food
        """
        initial_food = 300
        nt.assert_equal(self.savannah.available_food_herb, initial_food)

    def test_eat_food_savannah(self):
        """
        Test that available food in savannah is eaten and new amount is updated
        """
        self.savannah.feeding_cycle()
        food_left = 250
        nt.assert_equal(self.savannah.available_food_herb, food_left)

    def test_replenish_food_savannah(self):
        """
        test that eaten food gets replenished correctly
        """
        self.savannah.feeding_cycle()
        food_after_replenish = 265
        self.savannah.grow_food()
        nt.assert_equal(self.savannah.available_food_herb, food_after_replenish)

    def test_jungle_initial_food(self):
        """
        Test of initial available food for jungle
        """
        initial_food = 800
        nt.assert_equal(self.jungle.available_food_herb, initial_food)

    def test_jungle_food_replenishes(self):
        """
        Test that available food in jungle gets replenished
        """
        initial_food = 800
        food_after_feeding = 750
        self.jungle.feeding_cycle()
        nt.assert_equal(self.jungle.available_food_herb, food_after_feeding)
        self.jungle.grow_food()
        nt.assert_equal(self.jungle.available_food_herb, initial_food)


class TestClass(object):
    """
    Tests for cell with both carnivores and herbivores
    """

    def __init__(self):
        self.original_params_savannah = Savannah.params
        self.original_params_jungle = Jungle.params
        self.jungle = None
        self.savannah = None
        self.carn = None
        self.herb = None
        self.desert = None
        self.single_carn = None
        self.original_params_herb = None
        self.list = None
        self.single_herb = None
        self.original_params_herb = Herbivore.params
        self.original_params_carn = Carnivore.params
        self.ocean = None
        self.mountain = None

    def setup(self):
        self.herb = [Herbivore(weight=1) for _ in range(50)]
        self.carn = [Carnivore(weight=80) for _ in range(20)]
        self.savannah = Savannah(self.carn, self.herb)
        self.jungle = Jungle(self.carn, self.herb)
        self.desert = Desert(self.carn, self.herb)
        self.list = [((0, 1), 0.25), ((1, 2), 0.25), ((2, 1), 0.25),
                     ((1, 0), 0.25)]
        self.single_herb = Herbivore()
        self.single_carn = Carnivore()
        self.mountain = Mountain()
        self.ocean = Ocean()

    def teardown(self):
        Savannah.params = self.original_params_savannah
        Jungle.params = self.original_params_jungle
        Herbivore.params = self.original_params_herb
        Carnivore.params = self.original_params_carn

    def test_carnivore_weight_increase(self):
        """
        test that carnivores weight increase of feeding
        """
        initial_weight = 80
        num_carnivores = 20
        self.jungle.feeding_cycle()
        total_weight = 0
        for carn in self.carn:
            total_weight += carn.weight
        average_weight = total_weight / num_carnivores
        nt.assert_greater(average_weight, initial_weight)

    def test_carnivores_feed_jungle(self):
        """
        Test that the number of herbivores decrease after carnivores have fed
        """
        initial_amount_herbivores = 50
        self.jungle.feeding_cycle()
        nt.assert_less(len(self.herb), initial_amount_herbivores)

    def test_carnivores_feed_savannah(self):
        """
        tests that amount of herbivores is reduced after carnivores feed
        """
        initial_amount_herbivores = 50
        self.savannah.feeding_cycle()
        nt.assert_less(len(self.herb), initial_amount_herbivores)

    def test_relative_food(self):
        """
        Tests calculated relative food for both carnivores and herbivores
        """
        relative_food_carn = 0.04761904
        relative_food_herb = 1.56862745
        nt.assert_almost_equal(self.jungle.relative_food_herb(),
                               relative_food_herb)
        nt.assert_almost_equal(self.jungle.relative_food_carn(),
                               relative_food_carn)

    def test_breeding_cycle(self):
        """
        Tests breeding for herbivores and carnivores
        """
        initial_herbivores = 50
        initial_carnivores = 20
        for herb in self.herb:
            herb.weight = 80
            herb.fitness = 1
        self.jungle.breeding_cycle()
        nt.assert_greater(len(self.herb), initial_herbivores)
        nt.assert_greater(len(self.carn), initial_carnivores)

    def test_no_breeding(self):

        Herbivore.set_parameters({"gamma": 0})
        Carnivore.set_parameters({"gamma": 0})
        initial_herbivores = 50
        initial_carnivores = 20
        for herb in self.herb:
            herb.weight = 80
            herb.fitness = 1
        for carn in self.carn:
            carn.weight = 80
            carn.fitness = 1
        self.jungle.breeding_cycle()
        nt.assert_equal(len(self.herb), initial_herbivores)
        nt.assert_equal(len(self.carn), initial_carnivores)

    def test_age_cycle(self):
        """
        tests ageing in landscape
        """
        new_age = 1
        self.jungle.age_cycle()
        for herb in self.herb:
            nt.assert_equal(herb.age, new_age)
        for carn in self.carn:
            nt.assert_equal(carn.age, new_age)

    def test_weightloss(self):
        """
        Tests the weightloss function
        """
        new_weight_herb = 0.95
        new_weight_carn = 70
        self.jungle.weightloss_cycle()
        for herb in self.herb:
            nt.assert_equal(herb.weight, new_weight_herb)
        for carn in self.carn:
            nt.assert_equal(carn.weight, new_weight_carn)

    def test_death_cycle(self):
        """
        tests that both herbivores and carnivores dies
        """

        initial_num_herbivores = 50
        initial_num_carnivores = 20
        for herb in self.herb:
            herb.fitness = 0
        for carn in self.carn:
            carn.fitness = 0
        self.jungle.death_cycle()
        nt.assert_less(len(self.herb), initial_num_herbivores)
        nt.assert_less(len(self.carn), initial_num_carnivores)

    def test_num_of_individuals(self):
        """
        Test of function number_of_individuals
        """

        number_of_carnivores = 20
        number_of_herbivores = 50
        nt.assert_equal(self.jungle.number_of_individuals(),
                        {"carnivores": number_of_carnivores,
                         "herbivores": number_of_herbivores})

    def test_avg_age(self):
        """
        Test of function avg_age
        """
        for carn in self.carn:
            carn.age = 10
        self.jungle.age_cycle()
        average_herb = 1
        average_carn = 11
        avg_age = (average_carn, average_herb)
        nt.assert_equal(self.jungle.avg_age(), avg_age)

    def test_avg_fitness(self):
        """
        Tests the function for calculating average fitness
        """
        for herb in self.herb:
            herb.fitness = 0.8
        for carn in self.carn:
            carn.fitness = 0.65
        avg_herb = 0.8
        avg_carn = 0.65
        nt.assert_almost_equal(self.jungle.avg_fitness()[0], avg_herb)
        nt.assert_almost_equal(self.jungle.avg_fitness()[1], avg_carn)

    def test_food_desert(self):
        """
        tests calculation of food in desert
        """
        available_food = 0
        nt.assert_equal(self.desert.available_food_herb, available_food)

    def test_moves(self):
        """
        Tests that animals position updates
        """
        jungle = Jungle([self.single_carn], [self.single_herb])
        Herbivore.set_parameters({"mu": 1})
        Carnivore.set_parameters({"mu": 1})
        self.single_carn.fitness = 1
        self.single_herb.fitness = 1
        carn_position = self.single_carn.coordinates
        herb_position = self.single_herb.coordinates
        jungle.migration_cycle_herb(self.list)
        jungle.migration_cycle_carn(self.list)
        nt.assert_not_equal(self.single_herb.coordinates, herb_position)
        nt.assert_not_equal(self.single_carn.coordinates, carn_position)

    def test_has_moved(self):
        """
        Tests first that animals has_moved returns true after migration and
        after that it does not move a second time
        """
        jungle = Jungle([self.single_carn], [self.single_herb])
        Herbivore.set_parameters({"mu": 1})
        Carnivore.set_parameters({"mu": 1})
        self.single_carn.fitness = 1
        self.single_herb.fitness = 1
        jungle.migration_cycle_herb(self.list)
        jungle.migration_cycle_carn(self.list)
        nt.assert_true(self.single_herb.has_moved)
        nt.assert_true(self.single_carn.has_moved)

        carn_position = self.single_carn.coordinates
        herb_position = self.single_herb.coordinates
        jungle.migration_cycle_herb(self.list)
        jungle.migration_cycle_carn(self.list)
        nt.assert_equal(self.single_herb.coordinates, herb_position)
        nt.assert_equal(self.single_carn.coordinates, carn_position)

    def test_passable(self):
        """
        Test of attribute passable for all landscapes
        """
        nt.assert_true(self.savannah.passable)
        nt.assert_true(self.jungle.passable)
        nt.assert_true(self.desert.passable)
        nt.assert_false(self.ocean.passable)
        nt.assert_false(self.mountain.passable)
