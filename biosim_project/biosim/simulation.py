# -*- Utf-8 -*-

from biosim.island import Island
from biosim.animals import Herbivore, Carnivore
import matplotlib.pyplot as plt
import numpy as np
import random

"""
Simulation module
"""

__author__ = 'Marius Kristiansen, Kristian Frafjord'
__email__ = 'mariukri@nmbu.no, krfr@nmbu.no'


class BioSim(object):
    """
    Class BioSim
    Main simulation class for biosim project
    """

    def __init__(self, island_map=None, ini_pop=None, seed=None):
        """
        Constructor creates island from given map, and adds
            initial population to island.
        All parameters needed to create animals are contained within
            ini_pop.

        :param island_map: String containing letters representing each
        type of landscape
        :param ini_pop: List of initial_populations. [pop1, pop2]
        :param seed: Seed for rng
        """
        if seed is not None:
            np.random.seed(seed)
            random.seed(seed)
        else:
            random.seed(1234)
            np.random.seed(987654)

        if island_map is None:
            island_map = """OOOOOOO
                            OJJSJJO
                            OJSSSJO
                            OJSMSJO
                            OJSMSJO
                            OJJJJJO
                            OOOOOOO"""
        self.island_map = island_map
        self.island = Island(self.island_map)
        self.island.build_map()
        self.vis_steps = None
        self.img_steps = None
        self.years_sim = 0
        self.heat = None
        if ini_pop is None:
            ini_herbs = [{'loc': (3, 3),
                          'pop': [{'species': 'Herbivore',
                                   'age': 5,
                                   'weight': 20}
                                  for _ in xrange(150)]}]
            ini_carns = [{'loc': (3, 3),
                          'pop': [{'species': 'Carnivore',
                                   'age': 5,
                                   'weight': 20}
                                  for _ in xrange(40)]}]
            ini_pop = ini_herbs + ini_carns
        self.add_population(ini_pop)
        self.fig = None

    def add_population(self, population):
        """
        Adds given population to cells. Location stored in given population
        :param population: list of populations
        """
        for species in population:
            y, x = [n - 1 for n in species['loc']]
            for ani in species['pop']:
                if ani['species'] == 'Herbivore':
                    self.island.island[y][x].herbivores.append(Herbivore(
                        weight=ani['weight'], age=ani['age'],
                        coordinates=(y, x)))
                elif ani['species'] == 'Carnivore':
                    self.island.island[y][x].carnivores.append(Carnivore(
                        weight=ani['weight'], age=ani['age'],
                        coordinates=(y, x)))

    @staticmethod
    def heatmap(island_results):
        """
        Returns two nested lists; [row[cell]], one for herbivore population
        and one for carnivore population.
        :param island_results: Array containing population data for one year
        :return kart_herb, kart_carn: Map over populations
        """
        kart_herb = []
        kart_carn = []
        for row in island_results:
            h_row = []
            c_row = []
            for cell in row:
                h_row.append(cell["herbivores"])
                c_row.append(cell["carnivores"])
            kart_herb.append(h_row)
            kart_carn.append(c_row)
        return kart_herb, kart_carn

    def years_simulated(self):
        """
        Prints the total number of years simulated
        """
        if self.years_sim != 0:
            print 'Number of years simulated: {:5}'.format(self.years_sim)
        else:
            raise ValueError('No years have been simulated, run .simulate()!')

    def per_cell_animal_count(self):
        """
        Prints the total amount of animals in island
        """
        print self.island.individuals()

    def animal(self):
        """
        Returns total number of animals per type
        :return anim: Dict of animals per type
        """
        animals = self.island.individuals()
        herb = 0
        carn = 0
        for row in animals:
            for cell in row:
                herb += cell["herbivores"]
                carn += cell["carnivores"]
        anim = {"Herbivores": herb, "Carnivores": carn}
        return anim

    def animals_by_species(self):
        """
        Prints number of Animals per type on island
        """
        print self.animal()

    def total_number_of_animals(self):
        """
        Prints the total number of animals on island
        """
        animals = self.animal()
        print 'Total number of animals on island: {:4}'.format(
            animals["Herbivores"] + animals["Carnivores"])

    def plot_update(self, years, abscissa, ordinate, colour_herb, colour_carn):
        """
        Updates the plot n_steps years
        :param years: Number of years to plot
        :param abscissa: Xrange
        :param ordinate: Yrange
        :param colour_herb: Colour of heatmap (default None)
        :param colour_carn: Colour of heatmap (default None)
        """
        if self.years_sim == 0:
            self.fig = plt.figure()
        plt.axis('off')

        if abscissa is None:
            abscissa = years  # + self.years_sim

        ax1 = self.fig.add_subplot(2, 2, 1)
        plt.title('Rossum Island')
        rgb_value = {'O': (0.0, 0.0, 1.0),
                     'M': (0.5, 0.5, 0.5),
                     'J': (0.0, 0.6, 0.0),
                     'S': (0.5, 1.0, 0.5),
                     'D': (1.0, 1.0, 0.5)}
        kart_rgb = [[rgb_value[column] for column in row] for row in
                    self.island_map.replace(" ", "").split()]
        axlg = self.fig.add_axes([0.0, 0.5, 0.025, 0.5])
        axlg.axis('off')
        for ix, name in enumerate(('Ocean', 'Mountain', 'Jungle',
                                   'Savannah', 'Desert')):
            axlg.add_patch(plt.Rectangle((0., ix * 0.2), 0.3, 0.1,
                                         edgecolor='none',
                                         facecolor=rgb_value[name[0]]))
            axlg.text(0.35, ix * 0.2, name, transform=axlg.transAxes)

        ax1.imshow(kart_rgb, interpolation='nearest')
        ax1.set_xticks(range(0, len(kart_rgb[0]), 4))
        ax1.set_xticklabels(range(1, 1 + len(kart_rgb[0]), 4))
        ax1.set_yticks(range(0, len(kart_rgb), 4))
        ax1.set_yticklabels(range(1, 1 + len(kart_rgb), 4))

        ax2 = self.fig.add_subplot(2, 2, 2)
        plt.axis([self.years_sim, self.years_sim + abscissa, self.years_sim,
                  ordinate])

        title = plt.title('')
        line_herbs = ax2.plot(np.arange(years + self.years_sim), np.nan *
                              np.ones(self.years_sim + years), 'g-',
                              label="Herbivores")[0]
        line_carns = ax2.plot(np.arange(years + self.years_sim), np.nan * 
                              np.ones(self.years_sim + years), 'r-',
                              label="Carnivores")[0]
        if self.years_sim == 0:
            plt.grid()
            plt.legend(loc=1, prop={'size': 7})

        ax3 = self.fig.add_subplot(2, 2, 3)
        plt.title("Herbivores")
        ax3.set_xticks(range(0, len(self.island_map), 2))
        ax3.set_xticklabels(range(1, 1 + len(self.island_map), 2))
        ax3.set_yticks(range(0, len(self.island_map), 2))
        ax3.set_yticklabels(range(1, 1 + len(self.island_map), 2))
        ax3_bar = plt.imshow([[0 for _ in range(21)] for _ in range(13)])
        if self.years_sim == 0:
            plt.colorbar(ax3_bar,  orientation='horizontal', ticks=[])

        ax4 = self.fig.add_subplot(2, 2, 4)
        plt.title("Carnivores")
        ax4.set_xticks(range(0, len(self.island_map), 2))
        ax4.set_xticklabels(range(1, (1 + len(self.island_map)), 2))
        ax4.set_yticks(range(0, len(self.island_map), 2))
        ax4.set_yticklabels(range(1, (1 + len(self.island_map)), 2))
        ax4_bar = plt.imshow([[0 for _ in range(21)] for _ in range(13)])
        if self.years_sim == 0:
            plt.colorbar(ax4_bar, orientation='horizontal', ticks=[])

        for n in xrange(self.years_sim, self.years_sim + years):
            self.heat = self.heatmap(self.island.one_year())
            if n % self.vis_steps == 0:
                ax3.imshow(self.heat[0], interpolation='nearest',
                           cmap=colour_herb)

                ax4.imshow(self.heat[1], interpolation='nearest',
                           cmap=colour_carn)
                herbs = np.sum(self.heat[0])
                carns = np.sum(self.heat[1])
                ydata_herbs = line_herbs.get_ydata()
                ydata_carns = line_carns.get_ydata()
                ydata_herbs[n] = herbs
                ydata_carns[n] = carns
                line_herbs.set_ydata(ydata_herbs)
                line_carns.set_ydata(ydata_carns)
                title.set_text('Year: {:5}'.format(n + 1))  # Year counter

                self.fig.savefig(
                    'img{}{}.png'.format('0' * (5 - len(str(n + self.years_sim
                                                            ))),
                                         n)) if \
                    (n + 1) % self.img_steps == 0 else None

                plt.pause(1e-7)
                if np.sum(self.heat) == 0:
                    break
        self.years_sim += years

    def simulate(self, num_steps=100, vis_steps=1, img_steps=2000,
                 abscissa=None, ordinate=20000, colour_herb=None,
                 colour_carn=None):
        """

        Runs simulation num_steps number of years

        :param num_steps: Number of years to simulate
        :param vis_steps: Number of years between each time results are drawn
        :param img_steps: Number of years between each .png file created
        :param abscissa: Length of x-axis
        :param ordinate: Length of y-axis
        :param colour_herb: Colour for chart of herbivore population
        :param colour_carn: Colour for chart of herbivore population
        """
        self.vis_steps = vis_steps
        self.img_steps = img_steps
        self.plot_update(num_steps, abscissa, ordinate,
                         colour_herb, colour_carn)
        plt.show()
