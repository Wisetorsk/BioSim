# -*- Utf-8 -*-

from biosim.animals import Herbivore, Carnivore
import numpy as np

"""
Landscape module
"""

__author__ = 'Marius Kristiansen, Kristian Frafjord'
__email__ = 'mariukri@nmbu.no, krfr@nmbu.no'


class Landscape(object):
    """
    Superclass Landscape
    """

    params = None

    def __init__(self, carnivores=None, herbivores=None):
        """
        Constructor for Landscape.

        :param carnivores: Instances of carnivores as list of
        "Carnivore()" instances
        :param herbivores: Instances of herbivores as list of
        "Herbivore()" instances
        """
        self.available_food_herb = 0
        self.available_food_carn = 0
        if carnivores is None:
            self.carnivores = []
        else:
            self.carnivores = carnivores
        if herbivores is None:
            self.herbivores = []
        else:
            self.herbivores = herbivores

        self.relative_food_herbivore = None
        self.relative_food_carnivore = None
        self.total_weight = None

    def herbivore_weight(self):
        """
        Updates available food in cell for carnivore based on
        the total weight of herbivores in cell
        """
        self.available_food_carn = np.sum([herb.weight for
                                           herb in self.herbivores])

    @staticmethod
    def calc_fitness(animals):
        """
        Makes a sorted list for animal fitness of the input list of animal
        instances. Highest fitness first.

        :param animals: List of animal instances
        :return: Sorted list of animal instances with fitness values in a
        tuple consisting of (<class instance>, "fitness value")
        """
        return sorted([(individual, individual.fitness
                        ) for individual in animals], key=lambda x: x[1])[::-1]

    def feeding_cycle(self):
        """
        Starts the feeding cycle for herbivores in a single cell.
        Highest fitness first.
        """
        sorted_ = self.calc_fitness(self.herbivores)
        for animal in sorted_:
            self.available_food_herb = animal[0].feeding(
                self.available_food_herb)

        sort = self.calc_fitness(self.carnivores)
        for carnivore in sort:
            self.herbivores = carnivore[0].feeding(self.herbivores)

    def relative_food_carn(self):
        """
        Calculates the amount of relative food in cell for carnivores.

        :return: Amount of relative food for carnivores
        """
        self.herbivore_weight()
        self.relative_food_carnivore = (self.available_food_carn/((
            len(self.carnivores) + 1) * Carnivore.params["F"]))
        return self.relative_food_carnivore

    def relative_food_herb(self):
        """
        Calculates the amount of relative food in cell for herbivores.

        :return: Amount of relative food for herbivore
        """
        self.relative_food_herbivore = (self.available_food_herb/((
            len(self.herbivores) + 1) * Herbivore.params["F"]))
        return self.relative_food_herbivore

    def breeding_cycle(self):
        """
        Starts the breeding cycle for both species in a single cell
        If breeding is successful, the method appends a new animal
        of the same species to the list of animals
        """
        not_newborn_herbivores = len(self.herbivores)
        not_newborn_carnivores = len(self.carnivores)
        sorted_herbivores = self.calc_fitness(self.herbivores)
        sorted_carnivores = self.calc_fitness(self.carnivores)
        for herb in sorted_herbivores:
            result = herb[0].breeding(not_newborn_herbivores)
            if result is not None:
                self.herbivores.append(Herbivore(result, coordinates=herb[0].
                                                 coordinates))

        for carn in sorted_carnivores:
            result = carn[0].breeding(not_newborn_carnivores)
            if result is not None:
                self.carnivores.append(Carnivore(result, coordinates=carn[0].
                                                 coordinates))

    def migration_cycle_herb(self, _list):
        """
        Starts the migration cycle for the herbivores in the cell.

        :param _list: Nested list with possible coordinates the herbivores may
        move to and the relative food for each cell.
        :return: List of animals that are migrating and their new position
        """

        migrating_herbivores = []
        for herbivore in self.herbivores:
            if not herbivore.has_moved:
                if herbivore.check_migrate():
                    herbivore.has_moved = True
                    migrating_herbivores.append((herbivore.migrate(_list),
                                                 herbivore))
        return migrating_herbivores

    def migration_cycle_carn(self, _list):
        """
        Starts the migration cycle for the carnivores in the cell.

        :param _list: Nested list with possible coordinates the carnivores may
        move to and the relative food for each cell.

        :return: List of animals that are migrating and their new position
        """
        migrating_carnivores = []
        for carnivore in self.carnivores:
            if not carnivore.has_moved:
                if carnivore.check_migrate():
                    carnivore.has_moved = True
                    migrating_carnivores.append((carnivore.migrate(_list),
                                                 carnivore))
        return migrating_carnivores

    def age_cycle(self):
        """
        Each animals age is incremented by one year
        """
        for animal in self.herbivores + self.carnivores:
            animal.ageing()

    def weightloss_cycle(self):
        """
        Each animal loses weight according to formula; "eta" * "weight"
        """
        for animal in self.herbivores + self.carnivores:
            animal.weightloss()

    def death_cycle(self):
        """
        Starts the death-function for each animal.
        Removes animals who are "dead" (Animal death method returns "True")
        """
        for herb in self.herbivores:
            if herb.death():
                self.herbivores.remove(herb)

        for carn in self.carnivores:
            if carn.death():
                self.carnivores.remove(carn)

    @classmethod
    def set_parameters(cls, new_params):
        """
        Updates parameters. Raises ValueError if values are invalid

        :param new_params: New set of parameters as dictionary
        """
        for param in new_params:
            if new_params[param] < 0:
                raise ValueError('Parameter "{}" is negative!'.format(param))
        cls.params.update(new_params)

    def number_of_individuals(self):
        """
        Returns number of individuals in cell.

        :return: dictionary containing number
        of carnivores and number of herbivores
        """
        return {"carnivores": len(self.carnivores),
                "herbivores": len(self.herbivores)}

    def avg_age(self):
        """
        Returns the average age of population

        :return: ("herbivores age", "carnivores age")
        """
        age_herb = []
        age_carn = []
        if len(self.herbivores) == 0:
            average_herb = None
        elif self.herbivores is None:
            average_herb = None
        else:
            for animal in self.herbivores:
                age_herb.append(animal.age)
            average_herb = np.sum(age_herb)/len(age_herb)

        if len(self.carnivores) == 0:
            average_carn = None
        elif self.carnivores is None:
            average_carn = None
        else:
            for animal in self.carnivores:
                age_carn.append(animal.age)
            average_carn = np.sum(age_carn)/len(age_carn)

        age_tup = (average_carn, average_herb)
        return age_tup

    def avg_fitness(self):
        """
        Method used for testing
        Returns the average fitness of the population

        :return: ("herbivores fitness", "carnivores fitness")
        """
        fitness_herb = []
        fitness_carn = []
        for animal in self.herbivores:
            fitness_herb.append(animal.fitness)

        for animal in self.carnivores:
            fitness_carn.append(animal.fitness)
        fitness_tup = (np.sum(fitness_herb) / len(fitness_herb),
                       np.sum(fitness_carn) / len(fitness_carn))
        return fitness_tup


class Jungle(Landscape):
    """
    Landscape subclass Jungle.
    Habitable and food is replenished to maximum level each year
    """
    params = {"fmax": 800, "alpha": None}

    def __init__(self, carnivores=None, herbivores=None):
        super(Jungle, self).__init__(carnivores, herbivores)
        self.available_food_herb = self.params["fmax"]
        self.passable = True
        self.herbivore_weight()

    def grow_food(self):
        """
        Replenishes the amount of food in the jungle cell to f_max
        """
        self.available_food_herb = self.params["fmax"]


class Savannah(Landscape):
    """
    Landscape subclass Savannah.
    Habitable, but food grows at a reduced rate.
    """
    params = {"fmax": 300, "alpha": 0.3}

    def __init__(self, carnivores=None, herbivores=None):
        super(Savannah, self).__init__(carnivores, herbivores)
        self.available_food_herb = self.params["fmax"]
        self.passable = True
        self.herbivore_weight()

    def grow_food(self):
        """
        Replenishes the amount of food in Savannah cell according to formula
        """
        self.available_food_herb = self.available_food_herb + (
            self.params["alpha"] * (self.params["fmax"] -
                                    self.available_food_herb))


class Desert(Landscape):
    """
    Landscape subclass Desert
    Inhabitable for herbivores, but carnivores can feed on herbivores in desert
    """
    def __init__(self, carnivores=None, herbivores=None):
        super(Desert, self).__init__(carnivores, herbivores)
        self.available_food_herb = 0
        self.passable = True
        self.herbivore_weight()


class Mountain(Landscape):
    """
    Landscape subclass Mountain
    Impassable terrain for both species
    """
    def __init__(self, carnivores=None, herbivores=None):
        super(Mountain, self).__init__(carnivores, herbivores)
        self.passable = False


class Ocean(Landscape):
    """
    Landscape subclass Ocean
    Impassable terrain for both species
    """
    def __init__(self, carnivores=None, herbivores=None):
        super(Ocean, self).__init__(carnivores, herbivores)
        self.passable = False
