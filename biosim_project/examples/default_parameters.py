# -*- Utf-8 -*-
# -*- coding: utf-8 -*-

import textwrap
import matplotlib.pyplot as plt

from biosim.simulation import BioSim

"""
Simulation run with default animal parameters over 200 years
"""

__author__ = 'Marius Kristiansen, Kristian Frafjord'
__email__ = 'mariukri@nmbu.no, krfr@nmbu.no'


if __name__ == '__main__':
    plt.ion()

    geogr = """OOOOOOOOOOOOOOOOOOOOO
               OOOOOOOOSMMMMJJJJJJJO
               OSSSSSJJJJMMJJJJJJJOO
               OSSSSSSSSSMMJJJJJJOOO
               OSSSSSJJJJJJJJJJJJOOO
               OSSSSSJJJDDJJJSJJJOOO
               OSSJJJJJDDDJJJSSSSOOO
               OOSSSSJJJDDJJJSOOOOOO
               OSSSJJJJJDDJJJJJJJOOO
               OSSSSJJJJDDJJJJOOOOOO
               OOSSSSJJJJJJJJOOOOOOO
               OOOSSSSJJJJJJJOOOOOOO
               OOOOOOOOOOOOOOOOOOOOO"""
    geogr = textwrap.dedent(geogr)

    ini_herbs = [{'loc': (10, 10),
                  'pop': [{'species': 'Herbivore',
                           'age': 5,
                           'weight': 20}
                          for _ in xrange(150)]}]
    ini_carns = [{'loc': (10, 10),
                  'pop': [{'species': 'Carnivore',
                           'age': 5,
                           'weight': 20}
                          for _ in xrange(40)]}]

    sim = BioSim(island_map=geogr, ini_pop=ini_herbs + ini_carns,
                 seed=656412)
    sim.simulate(num_steps=100, vis_steps=1, img_steps=2000)

    sim.add_population(population=ini_carns)
    sim.simulate(num_steps=100, vis_steps=1, img_steps=2000)

    raw_input('Press ENTER')
