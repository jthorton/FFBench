

class OPENMM:
    """This class contains simulation types for the OPENMM package."""

    def __init__(self, molecule, temp, Nonbonded_cutof_dist=None, integrator='lang', pressure=1, friction=5, OPLS=False, minimize=100, platform='CPU', constraints=None, solvation_model='TIP3P', Nonbonded_cutof_type=app.Periodic, switching_dist=None, longrange_correct=True):
        """The required parameters are:
        Integrator : the type of integrator
        Temperature: the tempuratre of the simulation
        Preasure: the peasure of the simulation
        Friction coefficent: how often are the collisons in the simualtion
        Nonbonded: cutof, switching distance (none means do not use), method (PME), longrange corrections
        Use: OPLS
        Minimizer : how many iterations of minimization should we try
        Platform : what should we use if CPU how many theads can we have?
        Reporters: What do we need? and how often do we need it?
        Solvation: what water model do we want? how many particles
        Constraints: constrain the h bonds?
        Pure liquid: how many copies of the molecule should we have?
        """

        self.molecule = molecule
        self.temp = temp
        self.Nonbonded_cutof_dist = Nonbonded_cutof_dist
        self.integrator = integrator
        self.pressure = pressure
        self.friction = friction
        self.OPLS = OPLS
        self.minimize = minimize
        self.platform = platform
        self.constraints = constraints
        self.solvation_model = solvation_model
        self.Nonbonded_cutof_type = Nonbonded_cutof_type
        self.switching_dist = switching_dist
        self.longrange_correct = longrange_correct

    def create_system(self):
        """Make the initial Openmm system from the input files."""
        pass

    def run_gas(self):
        """Run the gas simulation."""

        pass

    def run_liquid(self):
        """Run a liquid simulation."""
        pass

    def free_energy(self):
        """Run a free energy simulation using YANK."""
        pass

    def use_OPLS(self):
        """Apply the OPLS fix to the system."""
        pass


class GMX:
    """This class contains simulation types for the GMX package."""


    def __init__(self):
        """The required parameters are:
        Integrator : the type of integrator
        Temperature: the tempuratre of the simulation
        Preasure: the peasure of the simulation
        Friction coefficent: how often are the collisons in the simualtion
        Nonbonded: cutof, switching distance (none means do not use), method (PME), longrange corrections
        Use: OPLS
        Minimizer : how many iterations of minimization should we try
        Platform : what should we use if CPU how many theads can we have?
        Reporters: What do we need? and how often do we need it?
        Solvation: what water model do we want? how many particles
        Constraints: constrain the h bonds?
        Pure liquid: how many copies of the molecule should we have?
        """

        pass



class PSI$:
    pass


class g09:
    pass
