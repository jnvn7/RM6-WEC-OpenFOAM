# 2D Wave Flume
<div align="justify">
TODO: start writing
</div>
&nbsp;

<!-- <p align="middle">
  <img src="https://github.com/jnvn7/RM6-WEC-OpenFoam/blob/main/images/rm6.png" height="200"/>
  <img src="https://github.com/jnvn7/RM6-WEC-OpenFoam/blob/main/images/rm6-dimensions.png" height="200"/>
</p>

<p align='middle'> Figure 1 - RM6 BBDB Device Design and Dimensions</p> -->

## Case Description 
<div align="justify">
Write about the wave settings, how they are selected, etc. Jessica provided this info in an email.
</div>
&nbsp;

## Case Structure
<div align="justify">
TODO: I might actually make a file structure for this in beamer, then export as a figure. Then we can reuse the same graphic for all these cases but just adjust them based on what's going on 
</div>
&nbsp;

The case directory is organized with the following key subdirectories and files: 



**system**
* caseSetup:
* controlDict:
* blockMeshDict: 
* setFieldsDict:
* decomposeParDict:
* fvSolution:
* fvSchemes:

**constant**
* waveInput.txt:
* waveProperties:
* transportProperties: 
* turbulenceProperties:
* g:

**0.orig**
* alpha.water: 
* p_rgh: 
* U: 
* k, epsilon, omega, nut: 

**processing_scripts**
* plotWaves.py: 
* setIrregWave.py:  
* coreFuncs.py: 

**<tt>flowParams</tt>:** this file provides wave tank and wave model setup. (!) (TODO: add more)

The case additionally contains the following scripts which are related to running the case: 
* <tt>Allrun.ser</tt>: A script that performs all the necessary steps to run the case in serial (on one processor). Even if the eventual goal is to run the case in parallel, running the case in serial is a good step for checking if the case works properly before attempting to run in parallel. 

* <tt>Allrun</tt>: A script that performs all the necessary steps to run the case in parallel (on multiple processors). Note that the number of processors to use for the case is specified in system/decomposeParDict. 

* <tt>Allclean</tt>: A script that can be run to "clean" the case directory. This will remove output files from a previous run, whilst preserving all the core files needed to run the case. 

* <tt>restart.sh</tt>: This script is called by <tt>Allrun</tt> (or <tt>Allrun.ser</tt>) in the event a current simulation run already exists, and we want to restart from the latest output of the previous run. The script will move the existing logfile and postProcessing data files into a backup storage directory. 

## Running the Case
<div align="justify">
TODO: Write a bit about Allrun, just to explain what it is doing. Can point users to the Allrun file for more info 
TODO: add comments to the Allrun file 
</div>
&nbsp;

## Post-processing

<div align="justify">
TODO: write about the post-processing scripts, and how to run them. Include a plot of what the results should look like. Include a "true solution" file and a script that will compare whatever is run with "true soln" results to make sure people can do a 1:1 comparision -- if they use the same settings, they should get the same thing 

TODO: add some comments to the post-processing scripts 

TODO: add some screenshots of how it should look in paraview . Do we need to add how to visualize it in paraview? maybe not 
</div>
&nbsp;
