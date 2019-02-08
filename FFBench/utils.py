def pure_replicate(pdb_file, replicate=267, length=4):
    """This function uses gromacs to replicate a molecule in a solution box x times to be used in pure
    liquid simulations; the molecule should be the pdb file."""

    # TODO do we need the connectivity to run in openMM? or gromacs?
    # TODO if we do can we get it from pymol or vmd or do we need chimera?

    from os import mkdir, chdir
    from shutil import copy
    from subprocess import call

    # make a folder to store the liquid box move into it and run the insert molecule command.
    mkdir('pure_liquid')
    copy(pdb_file, 'pure_liquid')
    chdir('pure_liquid')
    # run the command into a log file as we need to check the right number of molecule were put in the box.
    with open('log.txt', 'w+')as log:
        call(f'gmx insert-molecules -ci  {pdb_file} -box {length} {length} {length}  -nmol {replicate} -o box.pdb', shell=True, stdout=log)

        for line in log:
            if 'Added' in line and 'molecules' in line:
                added = int(line.split()[1])
                if added == replicate:
                    solvated = True
                    break
        else:
            solvated = False

    # return the success of the function
    # if it fails remove the folder increase the length and call it again till it returns true.
    return solvated


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
