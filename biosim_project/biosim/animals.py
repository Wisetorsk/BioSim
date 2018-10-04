# -*- coding: Utf-8 -*-

import numpy as np
import math

"""
Animals module
"""

__author__ = 'Marius Kristiansen, Kristian Frafjord'
__email__ = 'mariukri@nmbu.no, krfr@nmbu.no'


class Animal(object):
    """
    Superclass "Animal" for herbivores and carnivores
    """

    params = None

    def __init__(self, weight=None, age=0, coordinates=(1, 1)):
        """
        :param weight: Default None results in gaussian distribution of weight
        :param age: The starting age of animal
        :param coordinates: Starting coordinates of the animal
        """
        if weight is None:
            self.weight = np.random.normal(self.params["w_birth"],
                                           self.params["sigma_birth"])
        else:
            self.weight = weight
        self.age = age
        self.fitness = None
        self.update_fitness()
        self.coordinates = coordinates
        self.has_moved = False

    def ageing(self):
        """
        Increment age by one per year
        """
        self.age += 1

    def weightloss(self):
        """
        Recalculates the animals weight according to "eta" and original weight
        """
        self.weight -= self.params["eta"] * self.weight
        self.update_fitness()

    def update_fitness(self):
        """
        Re-calculates the animal's fitness based on age and weight
        """
        self.fitness = (1.0 / (1.0 + math.exp(self.params["phi_age"] * (self.age
                                                                        -
                                              self.params["a_half"])))) * \
                       (1.0 / (1.0 + math.exp(-self.params["phi_weight"] *
                                              (self.weight -
                                               self.params["w_half"]))))

    def death(self):
        """
        Calculates if the animal dies or not based on fitness and set parameters

        :return: True if the animal dies, False otherwise
        """
        probability = self.params["omega"] * (1 - self.fitness)
        return probability > np.random.random()

    def breeding(self, individuals):
        """
        Calculates if the animal will give birth based on animals present in
        cell, weight of animal and set parameters

        :param individuals: number of individuals in cell
        :return: Returns birth weight if it gives birth or None.
        """

        if self.weight < (self.params["zeta"] * (self.params["w_birth"] +
                                                 self.params["sigma_birth"])):
            probability = 0
        else:
            probability = self.params["gamma"] * self.fitness * (
                individuals - 1)
            if probability > 1:
                probability = 1

        if probability > np.random.random():
            birth_weight = np.random.normal(self.params["w_birth"],
                                            self.params["sigma_birth"])
            if birth_weight >= self.weight:
                return None
            elif birth_weight <= 0:
                return None
            self.weight -= self.params["xi"] * birth_weight
            self.update_fitness()
            return birth_weight
        else:
            return None

    def check_migrate(self):
        """
        Check if the animal wants to migrate based on set parameters

        :return: True if animal will migrate
        """
        return self.params["mu"] * self.fitness > np.random.random()

    def migrate(self, _list):
        """
        Calculates if the herbivore will migrate and returns either the new
        coordinates or the current coordinates.

        :param _list: Nested list of tuples with surrounding positions as first
        element and relative food as second element.
        :return: New coordinates for the animal if it migrates or the old
        if it does not.
        """
        p = 0
        random = np.random.random()
        _sum = 0
        for cell in _list:
            _sum += math.exp(self.params["lambda"] * cell[1])
        for cell in _list:
            dp = math.exp(self.params["lambda"] * cell[1])/_sum
            p += dp
            if p > random:
                self.coordinates = cell[0]
                return cell[0]

    @classmethod
    def set_parameters(cls, new_params):
        """
        Updates parameters. Raises ValueError if values are invalid

        :param new_params: New set of parameters as dictionary
        """
        testparams = ["omega", "mu", "phi_age", "phi_weight", "beta", "gamma"]

        for par in new_params:
            if new_params[par] < 0:
                raise ValueError('Given value "{}" for parameter "{}" is '
                                 'negative!'.format(new_params[par], par))

        for parameter in testparams:
            if parameter in new_params:
                if new_params[parameter] > 1:
                    raise ValueError('Given value for "{}" '
                                     'must be: [0 <= {} <= 1]'
                                     .format(parameter, parameter))
        cls.params.update(new_params)


class Herbivore(Animal):
    """
    Animal subclass Herbivore.
    """

    params = {"w_birth": 8, "sigma_birth": 1.5, "beta": 0.9, "eta": 0.05,
              "a_half": 40.0, "phi_age": 0.2, "w_half": 10.0, "phi_weight": 0.1,
              "mu": 0.25, "lambda": 1.0, "gamma": 0.2, "zeta": 3.5, "xi": 1.2,
              "omega": 0.4, "F": 10.0,
              "DeltaPhiMax": None}

    def __init__(self, weight=None, age=0, coordinates=(1, 1)):
        Animal.__init__(self, weight, age, coordinates)

    def feeding(self, available_food):
        """
        Herbivore feeding method. The animal will feed based on amount of
        available food in cell, and returns the result. If the amount left in
        cell is less than the animals "hunger", the animal will eat the
        remaining amount and returns 0

        :param available_food: available food before eating
        :return: new amount of food left after eating
        """
        if available_food >= self.params["F"]:
            self.weight += self.params["beta"] * self.params["F"]
            self.update_fitness()
            return available_food - self.params["F"]
        else:
            self.weight += available_food * self.params["beta"]
            self.update_fitness()
            return 0


class Carnivore(Animal):
    """
    Animal subclass Carnivore
    """

    params = {"w_birth": 6, "sigma_birth": 1, "beta": 0.75, "eta": 0.125,
              "a_half": 60.0, "phi_age": 0.4, "w_half": 4.0, "phi_weight": 0.4,
              "mu": 0.4, "lambda": 1.0, "gamma": 0.8, "zeta": 3.5, "xi": 1.1,
              "omega": 0.9, "F": 50.0,
              "DeltaPhiMax": 10}

    def __init__(self, weight=None, age=0, coordinates=(1, 1)):
        Animal.__init__(self, weight, age, coordinates)

    def feeding(self, herbivores):
        """
        Calculate if the carnivore will feed based on its own fitness and
        the fitness of the herbivore, and gain weight. Removes eaten
        herbivores.

        :param herbivores: List of herbivores in cell
        :return: Updated list of herbivores in cell after eating
        """
        eaten = 0
        d_phi_m = self.params["DeltaPhiMax"]
        beta = self.params["beta"]
        f = self.params["F"]
        for herbivore in herbivores:
            if (self.fitness - herbivore.fitness) < d_phi_m:
                if np.random.random() < (self.fitness - herbivore.fitness)\
                        / d_phi_m:
                    if herbivore.weight <= (f - eaten):
                        self.weight += beta * herbivore.weight
                        self.update_fitness()
                        eaten += herbivore.weight
                        herbivores.remove(herbivore)
                    else:
                        self.weight += beta * (f - eaten)
                        self.update_fitness()
                        herbivores.remove(herbivore)
                        break
        return herbivores
