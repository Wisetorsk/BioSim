# -*- coding: utf-8 -*-

"""
To create a package, run

python setup.py sdist

in the directory containing this file.

To create a zip archive in addition to a tar.gz archive, run

python setup.py sdist --formats=gztar,zip

The package will be placed in directory dist.

To install from the package, unpack it, move into the unpacked directory and
run

python setup.py install          # default location
python setup.py install --user   # per-user default location
python setup.py install --prefix=/Users/user/tmp/test  # to given dir

See also
    https://docs.python.org/2/distutils/
    https://docs.python.org/2/install/
    http://www.diveinto.org/python3/packaging.html
    https://python-packaging-user-guide.readthedocs.org
"""

from setuptools import setup
import codecs
import os

__author__ = 'Marius Kristiansen, Kristian Frafjord'
__email__ = 'mariukri@nmbu.no, krfr@nmbu.no'


def read_readme():
    """
    Read README.rst for use as long description.

    Based on PyPA Sample Project https://github.com/pypa/sampleproject

    :return: Multiline string containing contents of README.rst
    """

    # build absolute path to directory containing setup.py
    here = os.path.abspath(os.path.dirname(__file__))

    # read the README.rst file
    # using codes.open ensures that the file is read properly when using
    # UTF-8 encoding, e.g., for non-ASCII characters
    with codecs.open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
        long_description = f.read()

    return long_description


setup(
      # Basic information
      name='Biosim',
      version='1.1',

      # Packages to include
      packages=['biosim', 'biosim.tests'],

      # Required packages not included in Python standard library
      requires=['nose', 'numpy', 'matplotlib'],

      # Metadata
      description='BioSim Simulation of rossum island',
      long_description=read_readme(),
      author='Marius Skaug Kristiansen & Kristian Frafjord, NMBU',
      author_email='mariukri@nmbu.no & krfr@nmbu.no',
      url='https://bitbucket.org/kristian_marius/inf200_kristian_marius',
      keywords='simulation BioSim Island',
      license='MIT License',
      classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Science :: Ecological simulations',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2.7',
        ]
)
