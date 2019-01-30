# FFBench or BenchFF

This software package offeres wrappers around GMX and OpenMM to run simulations in order to benchmark Force Fields.
This will be a GUI based software allowing users to pick which experimental properties they would like to calculate using the software.
Users can use a standard FF like GAFF or OPLS or can use totally new FF that they have made. The files should be provided as either GMX or OpenMM inputs.
We can also offer some extra charge assignment tools through the use of QM based charges from either G09 or Psi4 or Horton.
Molecule sets are also provided based on those found in standard FF development sets. Users can add to them or create their own sets.
We also have a list of experimental data which should be hosted on either github or a web site with an api where we can request the latest versions of the experimental data.
The proram should offer post analysis and statisitcs and real time quering of the results where possible a report style PDF can be produced.
The program should be ran locally or should generate a script that can be submitted to a cluster and will run the task. 
Check points should be created to resume the runs. 
The program should be modeler (every simulation type is a class) so any extra experimental data point simulations can easily be added.
Allow a flexible functional form in openMM to test future development of the form quickly this will be useful in future versions of QUBEKit.
Virtual sites should be allowed. 
We should optimize the resources used not just draining the GPU but also ensuring that spear CPUs are used. 

Alist of standard settings can be used for all of the simulation types provided these are in config files, but we can also allow the user to change any settings and load these from now config files.
A web service with different groups config files could be created and test sets or they could be hosted on the git hub? 



## Software to learn
YANK
 

To test the sucess and ease of use of the platform we shall recalculate some reference data sets using standard GAFF and opls FFs.

## ISSUES 

How do we get the OPLS parameters if someone does not have an OPLS typing engine? The best solution would be to try and contact the ligpargen webservice and parameterize the molecules through the API?


