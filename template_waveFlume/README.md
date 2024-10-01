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


The case additionally contains the following scripts which are related to running the case: 
* Allrun.ser: 
* Allrun: 
* Allclean: 
* flowParams: 
* restart.sh: 

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
