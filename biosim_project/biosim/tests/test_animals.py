# -*- coding: utf-8 -*-

from biosim.animals import *
import nose.tools as nt

__author__ = 'Kristian Frafjord'
__email__ = 'krfr@nmbu.no'


class TestAnimals(object):
    def __init__(self):
        self.herb = None
        self.carn = None
        self.herb_params = Herbivore.params
        self.carn_params = Carnivore.params

    def setup(self):
        self.herb = Herbivore()
        self.carn = Carnivore()

    def teardown(self):
        Herbivore.params = self.herb_params
        Carnivore.params = self.carn_params

    def test_age_is_positive(self):
        """
        Test that the age value is positive
        """
        nt.assert_greater_equal(self.herb.age, 0)

    def test_age_increase(self):
        """
        test for the ageing function
        """
        self.herb.ageing()
        nt.assert_equal(self.herb.age, 1)

    def test_weight_is_positive(self):
        """
        Test that the weight value is positive
        """
        nt.assert_greater(self.herb.weight, 0)

    def test_weight_decrease(self):
        """
        Test for the weightloss function
        """
        new_weight = (1 - 0.05) * self.herb.weight
        self.herb.weightloss()
        nt.assert_equal(round(self.herb.weight, 7), round(new_weight, 7))

    def test_does_die(self):
        """
        Test that animal with fitness 0 dies with parameter "omega" = 1
        :return:
        """
        self.herb.fitness = 0
        self.herb.params["omega"] = 1
        nt.assert_true(self.herb.death())

    def test_does_not_die(self):
        """
        test that herbivore with fitness value 1 will not die
        """
        self.herb.fitness = 1
        nt.assert_false(self.herb.death())

    @staticmethod
    def test_fitness():
        """
        Test that fitness differs according to weight and age
        """
        herb1 = Herbivore(0)
        herb2 = Herbivore(80)
        nt.assert_not_equal(herb1.fitness, herb2.fitness)
        herb3 = Herbivore(20, 0)
        herb4 = Herbivore(20, 80)
        nt.assert_not_equal(herb3.fitness, herb4.fitness)

    @staticmethod
    def test_update_fitness():
        """
        Test if fitness updates after feeding
        """
        herb1 = Herbivore(10)
        original_fitness = herb1.fitness
        herb1.feeding(10)
        nt.assert_not_equal(herb1.fitness, original_fitness)

    def test_feeding_weight(self):
        """
        Test that the animals weight increases after feeding
        """
        original = 20
        self.herb.weight = 20
        self.herb.feeding(10)
        nt.assert_greater(self.herb.weight, original)

    def test_feeding_decrease(self):
        """
        Test that the function returns the decreased amount of available food
        """
        available_food = 100
        expected = 90
        nt.assert_equal(expected, self.herb.feeding(available_food))

    def test_feeding_less(self):
        """
        Test that the function returns "0" when there is less than 10 food and
        that new weight for herbivore is correct.
        """
        available_food = 5
        new_weight = \
            self.herb.weight + available_food * self.herb.params['beta']
        expected = 0
        nt.assert_equal(self.herb.feeding(available_food), expected)
        nt.assert_equals(self.herb.weight, new_weight)

    def test_breeding(self):
        """
        Test breeding function returns newborn weight successful
        """
        Herbivore.set_parameters({"gamma": 1})
        self.herb.weight = 50
        newborn_weight = self.herb.breeding(10)
        nt.assert_not_equal(None, newborn_weight)

    def test_breeding_parent_weight(self):
        """
        Test if the weight of the parent decreases after birth
        """
        Herbivore.set_parameters({"gamma": 1})
        start_weight = 50
        self.herb.weight = start_weight
        self.herb.breeding(10)
        nt.assert_less(self.herb.weight, start_weight)

    def test_breeding_failed(self):
        """
        Test if the function returns None when breeding fails
        """
        Herbivore.set_parameters({"gamma": 0})
        returned = self.herb.breeding(10)
        nt.assert_equal(returned, None)

    def test_age_is_positive_carn(self):
        """
        Test that the age value is positive
        """
        nt.assert_greater_equal(self.carn.age, 0)

    def test_age_increase_carn(self):
        """
        test for the ageing function
        """
        self.carn.ageing()
        nt.assert_equal(self.carn.age, 1)

    def test_weight_is_positive_carn(self):
        """
        Test that the weight value is positive
        """
        nt.assert_greater(self.carn.weight, 0)

    def test_weight_decrease_carn(self):
        """
        Test for the weightloss function
        """
        new_weight = (1 - 0.125) * self.carn.weight
        self.carn.weightloss()
        nt.assert_equal(self.carn.weight, new_weight)

    def test_does_die_carn(self):
        """
        Test that animal with fitness 0 dies with parameter "omega" = 1
        """
        self.carn.fitness = 0
        self.carn.params["omega"] = 1
        nt.assert_true(self.carn.death())

    def test_does_not_die_carn(self):
        """
        test that herbivore with fitness value 1 will not die
        """
        self.carn.fitness = 1
        nt.assert_false(self.carn.death())

    @staticmethod
    def test_fitness_carn():
        """
        Test that fitness differs according to weight and age
        """
        carn1 = Carnivore(0)
        carn2 = Carnivore(80)
        nt.assert_not_equal(carn1.fitness, carn2.fitness)
        carn3 = Carnivore(20, 0)
        carn4 = Carnivore(20, 80)
        nt.assert_not_equal(carn3.fitness, carn4.fitness)

    @staticmethod
    def test_update_fitness_carn():
        """
        Test if fitness updates after feeding
        """
        carn1 = Carnivore(30)
        carn2 = Carnivore(30)
        carn1.feeding([Herbivore(age=90) for _ in range(50)])
        nt.assert_not_equal(carn1.fitness, carn2.fitness)

    def test_feeding_weight_carn(self):
        """
        Test that the animals weight increases after feeding
        """
        original = self.carn.weight
        self.carn.fitness = 1
        herb = [Herbivore(age=90) for _ in range(50)]
        self.carn.feeding(herb)
        nt.assert_greater(self.carn.weight, original)

    def test_herbivore_removed_when_eaten(self):
        herbivores = [Herbivore(age=90) for _ in range(50)]
        self.carn.fitness = 1
        self.carn.feeding(herbivores)
        nt.assert_less(len(herbivores), 50)

    def test_breeding_carn(self):
        """
        Test breeding function returns newborn weight successful
        """
        Carnivore.set_parameters({"gamma": 1})
        self.carn.weight = 50
        newborn_weight = self.carn.breeding(10)
        nt.assert_not_equal(None, newborn_weight)

    def test_breeding_parent_weight_carn(self):
        """
        Test if the weight of the parent decreases after birth
        """
        start_weight = 50
        self.carn.weight = 50
        self.carn.breeding(10)
        nt.assert_less(self.carn.weight, start_weight)

    def test_breeding_failed_carn(self):
        """
        Test if the function returns None when breeding fails
        """
        nt.assert_equal(self.carn.breeding(1), None)


class TestMigrate(object):

    def __init__(self):
        self.original_params_herb = Herbivore.params
        self.original_params_carn = Carnivore.params
        self.herb = None
        self.carn = None
        self.list = None

    def setup(self):
        """

        """
        self.herb = Herbivore()
        self.carn = Carnivore()
        self.list = [((0, 1), 0.25), ((1, 2), 0.25), ((2, 1), 0.25),
                     ((1, 0), 0.25)]
        self.herb.coordinates = (1, 1)

    def teardown(self):
        """

        """
        Herbivore.params = self.original_params_herb
        Carnivore.params = self.original_params_carn

    def test_does_not_move(self):
        """
        Test that the check_migrate function returns false
        """
        Herbivore.set_parameters({"mu": 0})
        nt.assert_false(self.herb.check_migrate())

    def test_moves(self):
        """
        Test that the animal returns a new set of coordinates under ideal
        conditions
        """
        self.herb.fitness = 1
        Herbivore.set_parameters({"mu": 1})
        original_position = (1, 1)
        self.herb.coordinates = self.herb.migrate(self.list)
        nt.assert_not_equal(self.herb.coordinates, original_position)
