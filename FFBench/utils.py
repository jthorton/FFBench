import os
import re


class preperation:
    """This class prepares the simulation files needed for each simulation type."""

    def __init__(self, pdb, replicas=267, box_length=4, water_model=None):
        self.pdb = pdb
        self.name = pdb[:-4]
        self.relicas = replicas
        self.box_length = box_length
        self.water_model = water_model

    def pure_replicate(self):
        """This function uses gromacs to replicate a molecule in a solution box x times to be used in pure
        liquid simulations; the molecule should be the pdb file."""

        from os import mkdir, chdir
        from shutil import copy
        from subprocess import call

        # make a folder to store the liquid box move into it and run the insert molecule command.
        mkdir('pure_liquid')
        copy(self.pdb, 'pure_liquid')
        chdir('pure_liquid')
        # run the command into a log file as we need to check the right number of molecule were put in the box.
        with open('log.txt', 'w+')as log:
            call(f'gmx insert-molecules -ci  {self.pdb} -box {self.box_length} {self.box_length} {self.box_length}  -nmol {self.relicas} -o box.pdb', shell=True, stdout=log)

            for line in log:
                if 'Added' in line and 'molecules' in line:
                    added = int(line.split()[1])
                    if added == self.relicas:
                        solvated = True
                        break
            else:
                solvated = False
                chdir('../')

        # return the success of the function
        # if it fails remove the folder increase the length and call it again till it returns true.
        return solvated


    def add_conections(self):
        """Take the pdb of the liquid box and add the connect terms to the bottom so we can use the system in OpenMM."""

        # weird fix to stop the pymol graphical window showing when the function is run

        import __main__
        __main__.pymol_argv = ['pymol', '-qc']  # Quiet and no GUI

        from pymol import cmd, finish_launching

        finish_launching()
        cmd.load('box.pdb', object='liquid')
        cmd.do('set pdb_conect_all, on')
        cmd.save(f'{self.name}_box.pdb', selection='(liquid)')
        cmd.quit()

        return True

    def solvate(self):
        """Solvate the molecule in the required water model."""

        pass


def get_cutoff(xml_file):
    """Opens an xml file, searches for all elements and identifies heavy (non-H) atoms.
    Returns a cut-off depending on this number.
    """

    heavy_atoms = 0
    with open(xml_file, 'r') as xml:
        for line in xml:
            if line.startswith('<Type'):
                # line.split('element')[1][2] is guaranteed* to be where the element names are in the xml. *hopefully
                if line.split('element')[1][2] != 'H':
                    heavy_atoms += 1

    if heavy_atoms < 3:
        cutoff = 1.1
    elif heavy_atoms < 5:
        cutoff = 1.3
    else:
        cutoff = 1.5

    print(f'{heavy_atoms} heavy atoms found in {xml_file[:-4]}; cut-off is {cutoff}')
    return cutoff


def view_system():
    """Open a pymol window in the gui that can view the system."""

    pass


def refresh_view():
    """Refresh the pymol viewing window to show more frames."""
    pass


class QSSHelper:
    def __init__(self):
        pass

    @staticmethod
    def open_qss(path):
        """
        opens a Qt stylesheet with a path relative to the project

        Note: it changes the urls in the Qt stylesheet (in memory), and makes these urls relative to the project
        Warning: the urls in the Qt stylesheet should have the forward slash ('/') as the pathname separator
        """
        with open(path) as f:
            qss = f.read()
            pattern = r'url\((.*?)\);'
            for url in sorted(set(re.findall(pattern, qss)), key=len, reverse=True):
                directory, basename = os.path.split(path)
                new_url = os.path.join(directory, *url.split('/'))
                new_url = os.path.normpath(new_url)
                new_url = new_url.replace(os.path.sep, '/')
                qss = qss.replace(url, new_url)
            return qss