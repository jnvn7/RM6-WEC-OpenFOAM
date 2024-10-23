# 2D Wave Flume

<div align="justify">

## Overview 
This directory houses a templated example for 2D wave flume simulations, along with four specific example cases based upon the template. 

It is recommended that the interested user start with the <tt>README</tt> file in the template case directory <tt>template_waveFlume</tt>, which contains instructions on how to run a case, as well as documentation on the simulation setup, <tt>OpenFOAM</tt> dictionary files and file structure, and post-processing.  

The four example cases are each built by making modifications to the template case, and are ready to be run "as-is". They are described in more detail below in [Example cases](#example-cases). 


## Example cases 
### Descriptions
Three conditions from the PacWave South test sites are selected (see TABLE 1). 
These represent: 1) the most commonly occurring seas, 2) the highest annualized wave energy sea state, and 3) one of the extreme sea states on the 50-year contour (Dunkle et al., 2020). 
While these correspond to the irregular sea states at the site, for the current project, we will simulate them as regular wave conditions. 
The significant wave height ($H_s$) and energy period ($T_e$) are treated as regular wave height and period, respectively. 

For completeness, case 4 serves to simulate case 2 (TABLE 1) as irregular sea state. 
It is noted that all simulation demonstration cases developed in this project are scaled at a 1:15 ratio, which provides an appropriate size for typical wave flume experimental tests. 
&nbsp;

<p align='middle'>

| Test Name | Case 1 | Case 2 | Case 3 | Case 4 | 
------------|--------|--------|--------|----------
| Wave type | Regular | Regular | Regular | Irregular | 
| $H_s (m)$ | 1.75 (0.12) | 2.75 (0.18) | 7.45 (0.50) | 1.75 (0.12)| 
| $T_e (s)$ | 8.50 (2.20) | 10.5 (2.71) | 10.0 (2.58) | 8.50 (2.20)| 
| $\lambda (m)$ | 112.80 (7.52) | 172.13 (11.48) | 156.13 (10.41) | 112.80 (7.52)|

</p>
<p align='middle'> TABLE 1 - Wave Characteristics </p>

</div>
&nbsp;

[1]	Dunkle, G., Robertson, B., García-Medina, G., & Yang, Z. (2020). Pacwave wave resource assessment.

### Pre-packaged wave probe data for example cases
For each example case, pre-packaged wave probe data is provided as a "sanity check" for the user to compare with their own simulated data. This data is housed in the <tt>prePackaged-postProcessing</tt> directory of each example case. If the case has run correctly, the user-generated wave probe data in <tt>postProcessing</tt> should match the data in <tt>prePackaged-postProcessing</tt>. 

To check if this is the case, the user can use the provided python script <tt>plotWavesCompare.py</tt> in the <tt>processing_scripts</tt> directory. Running this script will plot the pre-packaged data against the user-generated data for each wave probe in the simulation. Example output of this script should look like Figure 1 below. 

<p align="middle">
  <img src="https://github.com/jnvn7/RM6-WEC-OpenFoam/blob/main/images/case1-prepack-vs-usergen-example-figure.png" width="400"/>
</p>
<p align='middle'> Figure 1 - Example output of the <tt>plotWavesCompare.py</tt> python script, plotting the user-generated wave probe data vs. the pre-packaged wave probe data for each probe. </p>