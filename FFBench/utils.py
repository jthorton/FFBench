def pure_replicate(molecule, replicate=267, length=4):
    """This function uses gromacs to replicate a molecule in a solution box x amount of times to be used in pure
    liquid simulations, the molecule should be the pdb file."""

    #TODO do we need the conectivity to run in openMM? or gromacs?
    #TODO if we do can we get it from pymol or vmd or do we need chimera?

    from os import  mkdir, chdir
    from shutil import copy
    from subprocess import call

    # make a folder to store the liquid box move into it and run the insert molecule command.
    mkdir('pure_liquid')
    copy(molecule, 'pure_liquid')
    chdir('pure_liquid')
    # run the command into a log file as we need to chack the right amount of molecule were put in the box.
    with open('log.txt', 'w+')as log:
        call(f'gmx insert-molecules -ci  {molecule} -box {length} {length} {length}  -nmol {replicate} -o box.pdb', shell=True, stdout=log)

    # now make sure we have the right amount of molecules in the box
    with open('log.txt', 'w+')as log:
        lines = log.readlines()

    for line in lines:
        if 'Added' in line and 'molecules' in line:
            added = int(line.split()[1])
            if added == replicate:
                solvated = True
                break
            else:
                solvated = False
                break

    # return the success of the function
    # if it fails remove the folder increase the length and call it again till it returns true.
    return solvated



