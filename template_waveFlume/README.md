# 2D Wave Flume

## Case Description 
<div align="justify">

<div align="justify">
TODO: Brief intro blurb/image? similar to how Jessica has for main page
</div>
&nbsp;

<!-- <p align="middle">
  <img src="https://github.com/jnvn7/RM6-WEC-OpenFoam/blob/main/images/rm6.png" height="200"/>
  <img src="https://github.com/jnvn7/RM6-WEC-OpenFoam/blob/main/images/rm6-dimensions.png" height="200"/>
</p>

<p align='middle'> Figure 1 - RM6 BBDB Device Design and Dimensions</p> -->

Write about the wave settings, how they are selected, etc. Jessica provided this info in an email.

Something like: "this example case uses the <tt>interFoam</tt> solver of <tt>OpenFOAM</tt> to simulate a 2D wave flume, for either regular or irregular waves. Outputs are XXX. 
</div>
&nbsp;

## Case Structure
<div align="justify">

<!-- </div>
&nbsp; -->

The case directory of <tt> OpenFOAM </tt> dictionary files is organized with the following key subdirectories and files described below. However, for more minor adjustments to the case, such as changing domain/mesh size, or modifying wave properties or models, the key files the user should note are: 
*  <tt>flowParams</tt>
*  <tt>system/caseSetup</tt>
*  (TODO: add more?)


**<tt>flowParams</tt>:** This file provides information related to the wave tank and wave model setup to the solver. For example, in this file, the user can specify things such as: the wave type (regular or irregular), the wave model utilized, wave height/period, positioning of wave probes to measure the surface height, or quantities related to mesh control (i.e. cells per wave height, cells per wave length). The <tt>flowParams</tt> file is included in other <tt>OpenFOAM</tt> dictionary files with the expression <tt>#include "..flowParams";</tt>, so that settings specified in <tt>flowParams</tt> can be utilized in those dictionary files. 

**system**
* <tt>caseSetup</tt>: Defines many of the quantities needed by <tt>blockMeshDict</tt> to create the simulation domain and mesh. Many of the parameters used in <tt>caseSetup</tt> are specified by the user in <tt>flowParams</tt>. 

* <tt>controlDict</tt>: Specifies main case control settings such as timing, timestep, and file write settings. This dictionary can also house user-defined function objects. In this particular case, the <tt>controlDict</tt> dictionary houses a function called <tt>interfaceHeight1</tt> which samples the free-surface height of the wave at specified probe locations along the wave tank. 


* <tt>blockMeshDict</tt>: Defines the mesh geometry and boundary conditions. (TODO: note here where else a user would need to edit to change boundary conditions)

* <tt>setFieldsDict</tt>: Used to set specified field values on a specified set of cells/faces/etc. In this case, it is used to set the initial conditon of the $\alpha_{\text{water}}$ variable, which denotes the phase (air or water), to 1 (water) below the still water level (of $z=0.0$), and to 0 (air) above the still water level.

* <tt>decomposeParDict</tt>: Specifies the parallel decomposition of the simulation domain for running the case in parallel. 

* <tt>fvSolution</tt>: Provides numerical solver settings to be used for the case. 

* <tt>fvSchemes</tt>: Specifies the numerical methods to be used for the case. 

**constant**
* <tt>waveInput.txt</tt>: This file is written by the processing script <tt>processing_scripts/setIrregWave.py</tt>, to be used for irregular wave cases. See description of <tt>setIrregWave.py</tt> below and the section on running cases with [irregular waves](#irregular-waves). 

* <tt>waveProperties</tt>: Provides wave property settings to the <tt>interFoam</tt> solver, including wave generation and absorption settings for the domain inlet and outlet. Many of the settings used in <tt>waveProperties</tt> are specified by the user in the <tt>flowParams</tt> file. 

* <tt>transportProperties</tt>: Specifies physical properties of the fluid phases (air and water) for the case.

* <tt>turbulenceProperties</tt>: Specifies properties related to the turbulence model used. In this example case, a laminar flow is selected. 

* <tt>g</tt>: Provides definition for acceleration due to gravity. 

**0.orig**: This directory contains dictionary files that provide boundary condition information for each of the relevant simulated fields in the case. Note: for actual simulations, the directory used by <tt>OpenFOAM</tt> is called <tt>0</tt>, which is then overwritten by the simulation solver. To prevent loss of original contents of the directory, the dictionaries are stored in <tt>0.orig</tt> instead, and then are copied into <tt>0</tt> by calling <tt>restore0Dir</tt> (called in the run script <tt>Allrun</tt>) described later on. The fields that <tt>0.orig</tt> contains this specified information for are:

* <tt>alpha.water</tt>: the phase-fraction variable used by <tt>interFoam's</tt> volume of fluid method, which represents how much of a grid cell contains each phase (air and water). 

* <tt>p_rgh</tt>: the hydrostatic pressure

* <tt>U</tt>: the fluid velocity

* <tt>k, epsilon, omega, nut</tt>: fields related to turbulence modeling, which are not utilized in this example

**processing_scripts**

* <tt>plotWaves.py</tt>: This script can be used to plot the height of the waves simulated in the case at various probe locations along the wave tank. The actual probe locations are specified in the <tt>flowParams</tt> dictionary, and the function which generates the probe data is defined in <tt>system/controlDict</tt>. The wave probe data is then stored in postProcessing/interfaceHeight1. For more information on the wave probes, see [Defining the wave probes](#defining-the-wave-probes). 

* <tt>setIrregWave.py</tt>:  TODO

* <tt>coreFuncs.py</tt>: TODO

* <tt>compareSolutions.py</tt>: TODO -- need to write this script as well 

The case additionally contains the following scripts which are related to running the case: 
* <tt>Allrun.ser</tt>: A script that performs all the necessary steps to run the case in serial (on one processor). Even if the eventual goal is to run the case in parallel, running the case in serial is a good step for checking if the case works properly before attempting to run in parallel. 

* <tt>Allrun</tt>: A script that performs all the necessary steps to run the case in parallel (on multiple processors). Note that the number of processors to use for the case is specified in system/decomposeParDict. 

* <tt>Allclean</tt>: A script that can be run to "clean" the case directory. This will remove output files from a previous run, whilst preserving all the core files needed to run the case. 

* <tt>restart.sh</tt>: This script is called by <tt>Allrun</tt> (or <tt>Allrun.ser</tt>) in the event a current simulation run already exists, and we want to restart from the latest output of the previous run. The script will move the existing logfile and postProcessing data files into a backup storage directory. 


Lastly, as the case runs, a new directory will be created called <tt>postProcessing</tt>. This will contain data files related to the wave probes defined using <tt>flowParams</tt> and <tt>system/controlDict</tt>, and further described in [Defining the wave probes](#defining-the-wave-probes). 


## Defining the wave probes
<div align="justify"> TODO: write blurb on what the wave probes are, how they are defined, etc. just so it's all in one place 

## Running the Case
<div align="justify">
Once all the dictionary files are appropriately set up, running the wave tank simulation case is done by running the appropriate <tt>Allrun</tt> scripts from the terminal. A walk-through of the steps involved for both regular and irregular wave cases are discussed below. 
</div>
&nbsp;

### Regular waves
Preliminary setup (optional -- these can be left at default settings if doing a simple walk-through): 
1. Check <tt>flowParams</tt> and ensure that the <tt>waveType</tt> is set to <tt>0</tt> for simulating regular waves. 
2. Select the desired wave model for the <tt>waveModel</tt> entry in <tt>flowParams</tt>. The available wave models are outlined in the header commented section of <tt>flowParams</tt>. 
3. Choose the desired wave properties in <tt>flowParams</tt>, i.e. <tt>waveHeight</tt> and <tt>wavePeriod</tt>

Running the case: 
1. Source the appropriate <tt>OpenFOAM</tt> environment. i.e.:
    ```
    . $OPENFOAM-INSTALL-DIR/etc/bashrc; # source the bashrc for the installation of OpenFOAM
    . ${WM_PROJECT_DIR:?}/bin/tools/RunFunctions; # source the run functions
    . ${WM_PROJECT_DIR:?}/bin/tools/CleanFunctions # source the clean functions
    ```

1. Test the case in serial (single processor) by running the <tt>Allrun.ser</tt> script: 
    ```
    ./Allrun.ser
    ```

    Terminal output should look like: 

    ```
    Cleaning case /PATH-TO-CASE/template_waveFlume_ser
    Restore 0/ from 0.orig/
    Running blockMesh on /PATH-TO-CASE/template_waveFlume
    Running setFields on /PATH-TO-CASE/template_waveFlume
    Running interFoam on /PATH-TO-CASE/template_waveFlume
    ```

    You can track the progress of the <tt>interFoam</tt> solver by doing a <tt>tail -f</tt> on the logfile, i.e.: 
    ```
    tail -f log.interFoam
    ```
    This should give something that looks like like: 
    ```
    Courant Number mean: 2.85758e-05 max: 0.0168531
    Interface Courant Number mean: 1.08762e-07 max: 0.0168278
    deltaT = 0.0166667
    Time = 0.833333

    PIMPLE: iteration 1
    Updating StokesII wave model for patch inlet
    MULES: Solving for alpha.water
    Phase-1 volume fraction = 0.499998  Min(alpha.water) = 0  Max(alpha.water) = 1
    Updating StokesII wave model for patch inlet
    MULES: Solving for alpha.water
    Phase-1 volume fraction = 0.499998  Min(alpha.water) = 0  Max(alpha.water) = 1
    Updating StokesII wave model for patch inlet
    MULES: Solving for alpha.water
    Phase-1 volume fraction = 0.499998  Min(alpha.water) = 0  Max(alpha.water) = 1
    Updating shallowWaterAbsorption wave model for patch outlet
    Updating StokesII wave model for patch inlet
    DICPCG:  Solving for p_rgh, Initial residual = 0.0097082, Final residual = 0.000607658, No Iterations 3
    time step continuity errors : sum local = 1.00546e-09, global = 2.48466e-11, cumulative = 2.46875e-09
    GAMG:  Solving for p_rgh, Initial residual = 0.000602819, Final residual = 7.1751e-08, No Iterations 18
    time step continuity errors : sum local = 1.20634e-13, global = 5.02768e-14, cumulative = 2.4688e-09
    ExecutionTime = 140.45 s  ClockTime = 143 s
    ```

    As the case runs, the user will note the directory will populate with new output files. This includes the aforementioned <tt>postProcessing</tt> directory, and also includes numbered directories corresponding to time values at which the solver will write the solution, i.e.: 
    ```
    [user@machine template_waveFlume]$ ls
    0         Allrun         postProcessing
    0.orig    Allrun.ser     processing_scripts
    1         constant       README.md
    2         flowParams     restart.sh
    3         log.blockMesh  system
    4         log.interFoam  viz.foam
    Allclean  log.setFields
    ```

    The frequency at which these are written is specified in the "Time Control" section of <tt>flowParams</tt>. 


1. To run the case in parallel, call the <tt>Allrun</tt> script. Note: before running in parallel, the user may want to adjust the number of parallel processors utilized. This can be done by editing the <tt>system/decomposeParDict</tt> dictionary file. Calling <tt>Allrun</tt> should look like:  
    ```

    [user@machine template_waveFlume] ./Allrun
    Cleaning case /PATH-TO-CASE/template_waveFlume
    Restore 0/ from 0.orig/
    Running blockMesh on /PATH-TO-CASE/template_waveFlume
    Running decomposePar on /PATH-TO-CASE/template_waveFlume
    Running setFields (36 processes) on /PATH-TO-CASE/template_waveFlume
    Running interFoam (36 processes) on /PATH-TO-CASE/template_waveFlume
    ```

    Calling a ```tail -f log.interFoam``` on the logfile should produce similar results to that shown in the serial case above. 

    Similarly to the serial case, the directory will populate with output file directories -- the main difference is that in a parallel run, the time output directories are housed within file folders per parallel process, i.e.: 

    ```
    [user@machine template_waveFlume]$ ls
    0                   processor13  processor3
    0.orig              processor14  processor30
    Allclean            processor15  processor31
    Allrun              processor16  processor32
    Allrun.ser          processor17  processor33
    constant            processor18  processor34
    flowParams          processor19  processor35
    log.blockMesh       processor2   processor4
    log.decomposePar    processor20  processor5
    log.interFoam       processor21  processor6
    log.setFields       processor22  processor7
    postProcessing      processor23  processor8
    processing_scripts  processor24  processor9
    processor0          processor25  README.md
    processor1          processor26  restart.sh
    processor10         processor27  system
    processor11         processor28  viz.foam
    processor12         processor29

    [user@machine template_waveFlume]$ ls processor0
    0  1  2  3  4  5  6  7  8  9  constant
    ```

1. Once the case has finished running (reached the end time specified in <tt>flowParams</tt>), it is ready to view and analyze!


### Irregular waves
Preliminary setup: 
1. Check <tt>flowParams</tt> and ensure that the <tt>waveType</tt> is set to <tt>1</tt> for simulating irregular waves. 
1. Select the desired wave model for the <tt>waveModel</tt> entry in <tt>flowParams</tt>. The available wave models and their usage are outlined in the header commented section of <tt>flowParams</tt>.
1. Choose the desired wave properties in <tt>flowParams</tt>, i.e. <tt>waveHeight</tt> and <tt>wavePeriod</tt> (TODO: is this still relevant?)
1. (TODO: double check this works, clean up writing) run the python script <tt>processing_scripts/setIrregWave.py</tt> to generate the appropriate <tt>constant/waveInput.txt</tt> file. 
    Output of this script should look like: 
    ```
    TODO-- add example
    ```

Running the case: 
1. Replicate steps for running the case outlined in [Regular waves](#regular-waves)

(TODO: add example outputs ?)
## Post-processing

<div align="justify">
TODO's:    

* write about the post-processing scripts, and how to run them. 
* Include a plot of what the results should look like. 
* Include a "true solution" file 
* Write script that will compare whatever is run with "true soln" results to make sure people can do a 1:1 comparision -- if they use the same settings, they should get the same thing 
* add some comments to the post-processing scripts  (if needed)

* add some screenshots of how it should look in paraview . 

* maybe add brief description of how to viz in paraview?
</div>
&nbsp;
