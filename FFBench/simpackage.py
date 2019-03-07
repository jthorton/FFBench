from simtk import unit
import simtk.openmm as mm
from simtk.openmm import app
import sys
from numpy import array
from FFBench.utils import preperation
from os import system, mkdir, chdir, getcwd



class OPENMM:
    """This class contains simulation types for the OPENMM package."""

    def __init__(self, integrator='Langevin', pressure=1, friction=5,
                 opls=False, minimise=100, platform='CPU', constraints=None, solvation_model=None,
                 nonbonded_cutoff_type=app.Periodic, long_range_correct=True, replicas=267, box_length=4):

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

        self.integrator = integrator
        self.pressure = pressure
        self.friction = friction
        self.opls = opls
        self.minimise = minimise
        self.platform = platform
        self.constraints = constraints
        self.solvation_model = solvation_model
        self.nonbonded_cutoff_type = nonbonded_cutoff_type
        self.long_range_correct = long_range_correct
        self.replicas = replicas
        self.box_length = box_length

    def create_system(self, system_type, molecule, xml, temp, cutoff, switching_distance):
        """Make the initial Openmm system from the input files."""

        integrators = {'Langevin':  mm.LangevinIntegrator(),
                       'Verlet': mm.VerletIntegrator(),
                        'Brownian': mm.BrownianIntegrator(),
                        'VariableLangevin': mm.VariableLangevinIntegrator(),
                        'VariableVerlet': mm.VariableVerletIntegrator()}
        self.integrator = integrators[self.integrator]

        if system_type == 'liquid':
            self.initialise_box_liquid()
            # Load the initial coords into the system and initialise
            pdb = app.PDBFile(self.molecule.filename)
            forcefield = app.ForceField(f'{self.molecule.name}.xml')
            modeller = app.Modeller(pdb.topology, pdb.positions)  # set the initial positions from the pdb
            self.system = forcefield.createSystem(modeller.topology, nonbondedMethod=app.NoCutoff, constraints=None)

            if self.opls:
                self.opls()

            temperature = temp * unit.kelvin
            integrator = mm.LangevinIntegrator(temperature, 5 / unit.picoseconds, 0.001 * unit.picoseconds)

            self.simulation = app.Simulation(modeller.topology, self.system, integrator)
            self.simulation.context.setPositions(modeller.positions)
            pass
        elif system_type == 'gas':
            # set up a gas phase run system
            pdb = app.PDBFile(molecule)
            forcefield = app.ForceField(xml)
            modeller = app.Modeller(pdb.topology, pdb.positions)  # set the initial positions from the pdb
            self.system = forcefield.createSystem(modeller.topology, nonbondedMethod=app.NoCutoff, constraints=self.constraints)

            # if you want to use the opls combination rule
            if self.opls:
                self.opls_lj()

            # now set up the integrator
            temperature = temp * unit.kelvin
            integrator = mm.LangevinIntegrator(temperature, 5 / unit.picoseconds, 0.001 * unit.picoseconds)

        elif system_type == 'both':
            self.initialise_box_liquid()
            self.initialise_gas()
            pass
        else:
            raise KeyError

    def run_gas(self, molecule, xml):
        """Run the gas simulation."""
        gas_folder = 'gas_run_openmm'
        mkdir(gas_folder)
        chdir(gas_folder)
        self.create_system('gas', molecule, xml)
        pass

    def run_liquid(self, molecule, xml):
        """Run a liquid simulation."""

        self.create_system('liquid', molecule, xml)
        pass

    def free_energy(self):
        """Run a free energy simulation using YANK."""
        pass

    def use_OPLS(self):
        """Apply the OPLS fix to the system."""
        pass

    def initialise_pure_box_liquid(self, molecule):
        """Make the pure liquid box required."""

        # start the prep class with the OpenMM class settings
        prep = preperation(molecule, self.replicas, self.box_length, self.solvation_model)

        # now make the box using GMX and add the conect terms using pymol
        while not solvated:
            solvated = prep.pure_replicate()
            if not solvated:
                prep.box_length += 1
                system('rm box.pdb')
        prep.add_conections()


class Yank:
    """This is the Openmm free energy class using yank!"""
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
