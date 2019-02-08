from simtk import unit
import simtk.openmm as mm
from simtk.openmm import app


class OPENMM:
    """This class contains simulation types for the OPENMM package."""

    def __init__(self, molecule, temp, nonbonded_cutoff_dist=None, integrator='lang', pressure=1, friction=5,
                 opls=False, minimise=100, platform='CPU', constraints=None, solvation_model='TIP3P',
                 nonbonded_cutoff_type=app.Periodic, switching_dist=None, long_range_correct=True):

        """The required parameters are:
        Integrator : the type of integrator
        Temperature: the temperature of the simulation
        Pressure: the pressure of the simulation
        Friction coefficient: how often are the collisions in the simualation
        Nonbonded: cutoff, switching distance (none means do not use), method (PME), long-range corrections
        Use: OPLS
        Minimizer : how many iterations of minimization should we try
        Platform : what should we use if CPU how many threads can we have?
        Reporters: What do we need? and how often do we need it?
        Solvation: what water model do we want? how many particles
        Constraints: constrain the h bonds?
        Pure liquid: how many copies of the molecule should we have?
        """

        self.molecule = molecule
        self.temp = temp
        self.nonbonded_cutoff_dist = nonbonded_cutoff_dist
        self.integrator = integrator
        self.pressure = pressure
        self.friction = friction
        self.opls = opls
        self.minimise = minimise
        self.platform = platform
        self.constraints = constraints
        self.solvation_model = solvation_model
        self.nonbonded_cutoff_type = nonbonded_cutoff_type
        self.switching_dist = switching_dist
        self.long_range_correct = long_range_correct

    def create_system(self, system_type='liquid'):
        """Make the initial Openmm system from the input files."""

        if system_type == 'liquid':
            self.initialise_box_liquid()
            pass
        elif system_type == 'gas':
            self.initialise_gas()
            pass
        elif system_type == 'both':
            self.initialise_box_liquid()
            self.initialise_gas()
            pass
        else:
            raise KeyError

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

    def initialise_box_liquid(self):
        pass

    def initialise_gas(self):
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


class PSI4:
    pass


class G09:
    pass
