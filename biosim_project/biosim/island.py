# -*- Utf-8 -*-

import numpy as np
from biosim.landscape import Jungle, Savannah, Desert, Mountain, Ocean
import random

"""
Module Island
"""

__author__ = 'Marius Kristiansen, Kristian Frafjord'
__email__ = 'mariukri@nmbu.no, krfr@nmbu.no'


class Island(object):
    """
    Class object: Island.
        - <var> = Island(String of landscape types)
        - <var>.build_map() must run before simulation starts
    """

    def __init__(self, island_map):
        """
        :param island_map: Map of island as string of "biomes"
        """
        self.island_map = island_map
        self.island_temp = []
        self.island = None

    def build_map(self):
        """
        Builds island based on input string.
        Island biomes are placed in a two dimensional array
        """

        geography = [list(row) for row in self.island_map.replace(" ", ""
                                                                  ).split("\n")]
        for row in geography:
            temp = []
            for cell in row:
                if cell == "J":
                    temp.append(Jungle())
                elif cell == "S":
                    temp.append(Savannah())
                elif cell == "D":
                    temp.append(Desert())
                elif cell == "M":
                    temp.append(Mountain())
                elif cell == "O":
                    temp.append(Ocean())
                else:
                    raise ValueError('"{}" is not properly defined! '
                                     'Use capital letters.')
            self.island_temp.append(temp)
        self.island = np.array(self.island_temp)

    def grow(self):
        """
        Runs through growth cycle for each cell in <var>.island.
        Runs only if the cell i capable of growing food
        """
        for row in self.island:
            for cell in row:
                if cell.__class__.__name__ == "Jungle":
                    cell.grow_food()
                elif cell.__class__.__name__ == "Savannah":
                    cell.grow_food()

    def feeding(self):
        """
        Runs animal level feeding method on each animal in each cell
        """
        for row in self.island:
            for cell in row:
                cell.feeding_cycle()

    def procreation(self):
        """
        Runs animal level breeding method on each animal in each cell
        """
        for row in self.island:
            for cell in row:
                cell.breeding_cycle()

    def surrounding_cells(self, coordinate):
        """
        Calculates surrounding cells that animals can migrate to.
        If the neighboring cell is either mountain or ocean it does not
        append the selected coordinates

        :param coordinate: A given coordinate
        :return: List of surrounding cells which animals can migrate to.
        """
        coordinates = []
        if not coordinate[0] <= 0:
            cell_north = ((coordinate[0] - 1), coordinate[1])
            if self.island[cell_north[0]][cell_north[1]].passable:
                if self.island[cell_north[0]][cell_north[1]].passable:
                    coordinates.append(cell_north)

        if not coordinate[0] >= (self.island.shape[0] - 1):
            cell_south = ((coordinate[0] + 1), coordinate[1])
            if self.island[cell_south[0]][cell_south[1]].passable:
                if self.island[cell_south[0]][cell_south[1]].passable:
                    coordinates.append(cell_south)

        if not coordinate[1] <= 0:
            cell_west = ((coordinate[0]), coordinate[1] - 1)
            if self.island[cell_west[0]][cell_west[1]].passable:
                if self.island[cell_west[0]][cell_west[1]].passable:
                    coordinates.append(cell_west)

        if not coordinate[1] >= (self.island.shape[1] - 1):
            cell_east = ((coordinate[0]), coordinate[1] + 1)
            if self.island[cell_east[0]][cell_east[1]].passable:
                if self.island[cell_east[0]][cell_east[1]].passable:
                    coordinates.append(cell_east)

        return coordinates

    def shuffle_coordinates(self):
        """
        Makes a shuffled list of the coordinates for all the cells on map.

        :return: Shuffled list of coordinates
        """
        coordinates = []
        for row in range(len(self.island)):
            for cell in range(len(self.island[row])):
                coordinates.append((row, cell))
        random.shuffle(coordinates)
        return coordinates

    def surrounding_cells_relative_food(self, y, x, species):
        """
        Makes nested lists for the coordinates of the surrounding cells and
        their amount of relative food.

        :param y: y coordinate for the center cell
        :param x: x coordinate for the center cell
        :param species: String with the name of the specie to calculate relative
        food for.
        :return: nested list with surrounding cell and their calculated relative
        food
        """
        nested_list = []
        surrounding_cells = self.surrounding_cells((y, x))

        for surrounding_cell in surrounding_cells:
            if species == "herbivore":
                nested_list.append(
                    (surrounding_cell, self.island[y][x].relative_food_herb()))
            else:
                nested_list.append(
                    (surrounding_cell, self.island[y][x].relative_food_carn()))
        return nested_list

    def migration(self):
        """
        Runs the migration process for all cells. Starts at first cell in
        shuffled list. Resets the has_moved attribute of the animals when
        all animals have moved.
        """
        for coordinates in self.shuffle_coordinates():
            y, x = coordinates
            migrating_herbivores = self.island[y][x].migration_cycle_herb(
                self.surrounding_cells_relative_food(y, x, "herbivore"))
            for herbivore in migrating_herbivores:
                if herbivore[0] is not None:
                    new_y, new_x = herbivore[0]
                    self.island[new_y][new_x].herbivores.append(herbivore[1])
                    self.island[y][x].herbivores.remove(herbivore[1])

            migrating_carnivores = self.island[y][x].migration_cycle_carn(
                self.surrounding_cells_relative_food(y, x, "carnivore"))
            for carnivore in migrating_carnivores:
                if carnivore[0] is not None:
                    new_y, new_x = carnivore[0]
                    self.island[new_y][new_x].carnivores.append(carnivore[1])
                    self.island[y][x].carnivores.remove(carnivore[1])

        for row in self.island:
            for cell in row:
                for animal in cell.carnivores + cell.herbivores:
                    animal.has_moved = False

    def aging(self):
        """
        Runs ageing method in each cell
        """
        for row in self.island:
            for cell in row:
                cell.age_cycle()

    def loss_of_weight(self):
        """
        Runs weightloss method in each cell
        """
        for row in self.island:
            for cell in row:
                cell.weightloss_cycle()

    def death(self):
        """
        Runs death function in each cell
        """
        for row in self.island:
            for cell in row:
                cell.death_cycle()

    def individuals(self):
        """
        Returns the number of carnivores and herbivores in each cell
        as array with each cell containing a dict over herbivores and carnivores
        """
        population = []
        for row in self.island:
            row_population = []
            for cell in row:
                row_population.append(cell.number_of_individuals())
            population.append(row_population)
        return np.array(population)

    def one_year(self):
        """
        Simulates one year progression and returns array containing the
        numbers of each species in each cell.
        """
        self.grow()
        self.feeding()
        self.procreation()
        self.migration()
        self.aging()
        self.loss_of_weight()
        self.death()
        return self.individuals()
