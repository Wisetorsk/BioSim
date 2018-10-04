BioSim
======

This python package simulates a simple ecosystem on a NxM size island.
----------------------------------------------------------------------
 * User can specify number, location, type, age and weight for individual
  animals as well as parameters describing the amount of available food and
  regrowth of food in the different cell types.

 * Parameters on animal level controls the behaviour of the animals.
    Parameters are class(species) specific
    Parameters:
    - "w_birth": Average weight of newborn animals
    - "sigma_birth": Standard deviation from w_birth
    - "beta": Relative Amount of weight the animal gains from food (eaten*beta)
    - "eta": Relative amount of weight the animal loses from weightloss
    - "a_half": Point at which age negatively impacts the animals fitness
    - "phi_age": "Fitness per year"
    - "w_half": Point at which low age impacts the animals fitness
    - "phi_weight": "Fitness per weight"
    - "mu": Probability of animals migrating (0 = no migration)
    - "lambda": Food preference impact on migration: If lambda > 0, the animal
        will prefer cell with more relative food, if lambda < 0, the animal
        will turn away from food, if lambda = 0, the animal will show no
        preference for any cell
    - "gamma": Probability to give birth (Also dependant on weight and animals
        in cell)
    - "zeta": Lower ratio between mother animal and offspring weight
    - "xi": Amount of weight the mother loses during birth not due to offspring
        weight
    - "omega": Probability of death
    - "F": Animal "Hunger". Amount of food the animal will eat
    - "DeltaPhiMax": Delta between herbivore and carnivore fitness
        used in feeding

 *  Parameters on Island level control the amount of available food and
    the rate at which food grows back.

Contents
--------

 - biosim: The BioSim python package
 - examples: Compatability check simulation