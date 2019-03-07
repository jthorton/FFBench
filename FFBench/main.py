from os import chdir, walk, path
import sys
import qdarkstyle
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QTimer, Qt, QSettings, QByteArray, QPoint, QSize, pyqtSlot
from subprocess import PIPE, Popen
from multiprocessing import cpu_count

from FFBench.utils import QSSHelper, preperation




class StartUp(QtWidgets.QMainWindow):
    """The start up window which checks if we want to open a new benchmark or an existing run to analyse."""

    def __init__(self, parent=None):
        super(StartUp, self).__init__(parent)
        self.label = QtWidgets.QLabel('Welcome to FFBench!')
        self.label.setFont(QtGui.QFont("Aerial", 20, QtGui.QFont.Bold))
        self.label.setAlignment(Qt.AlignHCenter)
        self.open = QtWidgets.QPushButton('Open existing')
        self.start = QtWidgets.QPushButton('New Benchmark')
        self.setCentralWidget(self.start)
        self.start.clicked.connect(self.start_new_click)
        self.dialog = None

        # now add the styling
        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(self.label)
        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(self.open)
        hbox.addWidget(self.start)
        vbox.addLayout(hbox)


        # central widget
        central = QtWidgets.QWidget()
        central.setLayout(vbox)
        self.setCentralWidget(central)
        self.center()

    def center(self):
        frameGm = self.frameGeometry()
        centerPoint = QtWidgets.QDesktopWidget().availableGeometry().center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

    def start_new_click(self):
        """Start the main window
        1 open up the file explorer to chose a location to work in
        2 open the main window
        """

        options = QtWidgets.QFileDialog.Options()
        file = str(QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.main = Window(file)
        self.hide()
        self.main.show()

    def open_old_click(self):
        """Open an old run
        1 open file explorer to find the old run
        2 open the main window and load in the results
        """

        pass

# main window set up to run one simulation through the gui then look at extending to multipule
class Window(QtWidgets.QMainWindow):
    def __init__(self, location, parent=None ):
        super(Window, self).__init__(parent)

        # get the location of the project and move into the folder
        self.location = location
        chdir(self.location)

        # set the layout
        self.layout = QtWidgets.QVBoxLayout()

        # set up the tabs for the display
        self.tabs = QtWidgets.QTabWidget()
        self.General_tab = General_Tab(self.location)
        self.Integrator_tab = QtWidgets.QWidget()

        # add the tabs to the screen
        self.tabs.addTab(self.General_tab, "General")
        self.tabs.addTab(self.Integrator_tab, "Integrator")

        self.layout.addWidget(self.tabs)

        # central widget
        central = QtWidgets.QWidget()
        central.setLayout(self.layout)
        self.setCentralWidget(central)


class QM_Tab(QtWidgets.QWidget):
    """General options page tab"""

    def __init__(self, parent=None):
        super(QM_Tab, self).__init__(parent)



class General_Tab(QtWidgets.QWidget):
    """General options page tab"""

    def __init__(self, location, parent=None):
        super(General_Tab, self).__init__(parent)

        self.location = location

        # main page layout
        self.layout = QtWidgets.QHBoxLayout(self)

        # left side labels and buttons
        # main header
        self.Simulation_label = QtWidgets.QLabel('Simulation main setup')
        self.Simulation_label.setFont(QtGui.QFont("Aerial", 16, QtGui.QFont.Bold))

        # md engine selector
        self.Engine_label = QtWidgets.QLabel('Molecular dynamics engine')
        self.MM_engine = QtWidgets.QComboBox()
        engines = self.find_engines()
        self.MM_engine.addItems(engines)

        # checkable groupbox / property selector
        self.density = QtWidgets.QCheckBox('Density')
        self.heat_of_vap = QtWidgets.QCheckBox('Heat of vaporization')
        self.hydration_free_energy = QtWidgets.QCheckBox('Hydration free energy')
        self.all = QtWidgets.QCheckBox('All')

        # add logic to buttons
        self.density.stateChanged.connect(self.all_props_state)
        self.heat_of_vap.stateChanged.connect(self.all_props_state)
        self.hydration_free_energy.stateChanged.connect(self.all_props_state)
        self.all.stateChanged.connect(self.all_props_state)

        # style the buttons
        groupbox_checkable_layout = QtWidgets.QHBoxLayout()
        groupbox_left_layout = QtWidgets.QVBoxLayout()
        groupbox_right_layout = QtWidgets.QVBoxLayout()
        groupbox_left_layout.addWidget(self.density)
        groupbox_left_layout.addWidget(self.heat_of_vap)
        groupbox_right_layout.addWidget(self.hydration_free_energy)
        groupbox_right_layout.addWidget(self.all)
        groupbox_checkable_layout.addLayout(groupbox_left_layout)
        groupbox_checkable_layout.addLayout(groupbox_right_layout)
        self.groupbox_checkable = QtWidgets.QGroupBox('Select the required properties')
        self.groupbox_checkable.setLayout(groupbox_checkable_layout)
        # self.groupbox_checkable.setCheckable(True)

        # hardware infomation
        self.hard_label = QtWidgets.QLabel('Hardware')
        self.hard_label.setFont(QtGui.QFont("Aerial", 16, QtGui.QFont.Bold))
        self.cores_label = QtWidgets.QLabel('Cores')
        self.CPU = QtWidgets.QCheckBox('CPU')
        self.CPU.setToolTip('At least 1 CPU is always needed! Select the amount of cores to distribute jobs')
        self.CPU.setChecked(True)
        self.CPU.setEnabled(False)
        self.GPU = QtWidgets.QCheckBox('GPU')
        self.hardware = QtWidgets.QGroupBox('Select the required hardware platforms')
        self.cores = QtWidgets.QComboBox()
        cpus = cpu_count()
        cpu = [str(x) for x in range(1, cpus+1)]
        self.cores.addItems(cpu)
        self.cores.setEditable(True)

        # hardware styling
        hard_box_options = QtWidgets.QHBoxLayout()
        hard_box_options.addWidget(self.CPU)
        hard_box_options.addWidget(self.GPU)
        hard_box_all = QtWidgets.QVBoxLayout()
        hard_box_all.addLayout(hard_box_options)
        hard_box_all.addWidget(self.cores_label)
        hard_box_all.addWidget(self.cores)
        self.hardware.setLayout(hard_box_all)

        # General FF parametrisation options
        self.parm_label = QtWidgets.QLabel('Molecule Parameters')
        self.parm_input_Amber_gaff1 = QtWidgets.QRadioButton('GAFF1')
        self.parm_input_Amber_gaff2 = QtWidgets.QRadioButton('GAFF2')
        self.parm_input_OPLS_BOSS = QtWidgets.QRadioButton('OPLSAA')
        self.parm_input_BCC = QtWidgets.QCheckBox('BCC')
        self.FFBench_param = QtWidgets.QGroupBox('Would you like FFBench to parameterise the molecules?')
        self.FFBench_param.setCheckable(True)

        # QM parma options
        self.QM_pop_Mulliken = QtWidgets.QCheckBox('Mulliken')
        self.QM_pop_Becke = QtWidgets.QCheckBox('Becke')
        self.QM_pop_Hirshfeld = QtWidgets.QCheckBox('Hirshfeld')
        self.QM_pop_Iterative_Hirshfeld = QtWidgets.QCheckBox('Iterative Hirshfeld')
        self.QM_pop_Iterative_Stockholder = QtWidgets.QCheckBox('Iterative Stockholder')
        self.QM_pop_Extended_Hirshfeld = QtWidgets.QCheckBox('Extended Hirshfeld')
        self.QM_pop_DDEC3 = QtWidgets.QCheckBox('DDEC3')
        self.QM_pop_DDEC6 = QtWidgets.QCheckBox('DDEC6')
        #TODO add more mertz ?
        self.QM_pop_options = QtWidgets.QGroupBox('Use QM population charges?')
        self.QM_pop_options.setCheckable(True)
        self.QM_pop_options.setChecked(False)
        self.QM_pop_advanced = QtWidgets.QPushButton('Advanced QM Settings')
        self.QM_pop_advanced.clicked.connect(self.show_QM_options)



        # parametrisation logic
        self.parm_input_OPLS_BOSS.toggled.connect(lambda :self.params_logic(self.parm_input_OPLS_BOSS))


        # parametrisation styling
        gaff_box = QtWidgets.QHBoxLayout()
        gaff_box.addWidget(self.parm_input_Amber_gaff1)
        gaff_box.addWidget(self.parm_input_Amber_gaff2)
        gaff_box.addWidget(self.parm_input_BCC)

        QM_box = QtWidgets.QGridLayout()
        QM_box.addWidget(self.QM_pop_Mulliken, 0, 0)
        QM_box.addWidget(self.QM_pop_Becke, 0, 1)
        QM_box.addWidget(self.QM_pop_Hirshfeld, 1, 0)
        QM_box.addWidget(self.QM_pop_Iterative_Hirshfeld, 1, 1)
        QM_box.addWidget(self.QM_pop_Iterative_Stockholder, 3, 1)
        QM_box.addWidget(self.QM_pop_Extended_Hirshfeld, 2, 1)
        QM_box.addWidget(self.QM_pop_DDEC3, 2, 0)
        QM_box.addWidget(self.QM_pop_DDEC6, 3, 0)
        self.QM_pop_options.setLayout(QM_box)

        parm_box = QtWidgets.QVBoxLayout()
        parm_box.addLayout(gaff_box)
        parm_box.addWidget(self.parm_input_OPLS_BOSS)
        self.FFBench_param.setLayout(parm_box)

        # molecules
        self.Mol_main = QtWidgets.QLabel('Molecules')
        self.Mol_main.setFont(QtGui.QFont("Aerial", 16, QtGui.QFont.Bold))

        # molecule set and data
        self.MOL_set_main = QtWidgets.QLabel('Molecule sets')
        self.MOL_set_main.setFont(QtGui.QFont("Aerial", 16, QtGui.QFont.Bold))
        self.MOL_label = QtWidgets.QLabel('Looking for molecules...')
        self.MOL_set_label_more = QtWidgets.QLabel('Select a molecule set')
        self.MOL_sets = QtWidgets.QComboBox()
        self.MOL_sets.addItems(['QUBEKit 109', 'Freesolv'])
        self.MOL_edit_set = QtWidgets.QPushButton('Edit set')
        self.MOL_edit_set.clicked.connect(self.show_molecule_set)



        # pack the layouts in
        vlayout_left = QtWidgets.QVBoxLayout()
        vlayout_left.addWidget(self.Simulation_label)
        vlayout_left.addWidget(self.Engine_label)
        vlayout_left.addWidget(self.MM_engine)
        vlayout_left.addWidget(self.groupbox_checkable)
        vlayout_left.addWidget(self.hard_label)
        vlayout_left.addWidget(self.hardware)

        vlayout_right = QtWidgets.QVBoxLayout()
        vlayout_right.addWidget(self.Mol_main)
        vlayout_right.addWidget(self.FFBench_param)
        vlayout_right.addWidget(self.QM_pop_options)
        vlayout_right.addWidget(self.QM_pop_advanced)
        vlayout_right.addWidget(self.MOL_set_main)
        vlayout_right.addWidget(self.MOL_label)
        vlayout_right.addWidget(self.MOL_set_label_more)
        vlayout_right.addWidget(self.MOL_sets)
        vlayout_right.addWidget(self.MOL_edit_set)

        self.layout.addLayout(vlayout_left)
        self.layout.addLayout(vlayout_right)

        # do the molecule search logic
        self.molecules = self.molecule_search()
        self.MOL_label.setText(f'{len(self.molecules)} molecule(s) found')
        self.MOL_sets.addItems([f'User set of {len(self.molecules)}'])


    def show_QM_options(self):
        """Show the QM options window."""

        self.QM_tab = QM_Tab()
        self.QM_tab.show()

    def show_molecule_set(self):
        """Show the molecule set editor"""

        self.Mol_tab =  Molecule_set_tab()
        self.Mol_tab.show()


    # all options logic
    @pyqtSlot(int)
    def all_props_state(self, state):
        if state == Qt.Checked:
            if self.sender() == self.all:
                self.density.setChecked(True)
                self.heat_of_vap.setChecked(True)
                self.hydration_free_energy.setChecked(True)
                self.all.setChecked(True)
        elif state == Qt.Unchecked:
            if self.sender() != self.all:
                self.all.setChecked(False)

    @pyqtSlot(int)
    def params_logic(self, button):
        if button.isChecked():
            self.parm_input_BCC.setCheckable(False)
            self.parm_input_BCC.setChecked(False)
        else:
            self.parm_input_BCC.setCheckable(True)

    def find_engines(self):
        """Find the MM engines present on the system that we can use."""

        mm_engines = []

        # test OpenMM
        try:
            from simtk import openmm
            mm_engines.append('OpenMM')
        except ImportError:
            pass

        # test GMX
        gmx = Popen("gmx", stdout=PIPE, shell=True)
        (output, err) = gmx.communicate()
        gmx_status = gmx.wait()
        if gmx_status == 0:
            mm_engines.append('Gromacs')

        # test Amber
        # TODO add amber support

        return mm_engines


    def molecule_search(self):
        """Search for any pdb structures of molecules in the folder"""

        molecules = {}
        for root, dirs, files in walk(self.location):
            for name in files:
                if name.endswith(".pdb"):
                    path.join(root, name)
                    molecules[name] = root

        return molecules


class Molecule_set_tab(QtWidgets.QWidget):
        """Open up the molecule data selector
        Inputs
        --------
        pdb file name:
        smiles string if from a default data set:
        property infomation: boling temp, density, heat of vap etc, any QM jobs, cut off
        clompleted/ progress:
        """

        def __init__(self, parent=None):
            super(Molecule_set_tab, self).__init__(parent)

            pass

def main():
    # creates the application and takes arguments from the command line
    application = QtWidgets.QApplication(sys.argv)

    # creates the window and sets its properties
    window = StartUp()
    window.setWindowTitle('FFBench (Force Field Benchmark toolkit)')  # title
    window.resize(500, 100)  # size

    # setup stylesheet
    application.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    window.show()  # shows the window

    # runs the application and waits for its return value at the end
    sys.exit(application.exec_())


if __name__ == '__main__':
    main()
