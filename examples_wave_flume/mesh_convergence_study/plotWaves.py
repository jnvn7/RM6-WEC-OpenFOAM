#!/usr/bin/env python3
##--------------------------------------------------------------------------------#
# Script to plot wave data from OF postProcessing folder
# Usage: python plotWaves.py OF_case_directories (single or multiple cases)
##--------------------------------------------------------------------------------#
import numpy as np
import coreFuncs as cF
import matplotlib.pyplot as plt
import sys
import os
#---------------------------------Plot settings-----------------------------#
#plt.rcParams['figure.dpi'] = 400
colors = np.array(
['#4477AA', # blue
  '#66CCEE', # cyan
  '#228833', # green
  '#CCBB44', # yellow
  '#EE6677', # red
  '#AA3377', # purple
  '#BBBBBB'] # grey]
)

# colormap from: https://personal.sron.nl/~pault/
plt.rcParams['axes.prop_cycle'] = plt.cycler(color=colors)

#---------------------------------User inputs----------------------------#
# Read inputs
nCases = len(sys.argv)-1
if (nCases < 1):
    print('\nMissing case input(s) for plotting!')
    print('\nUsage: \n \t python plotWaves.py OF_case_directories\n')
    sys.exit()

# Extract wave data. Default for wavePath is in OpenFOAM <postProcessing>. 
# Here it is set to pre-packeged data
wavePath = "prePackaged_postProcessing/waveProbes/*/height.dat"
iProbe = 3          # Set the probe number to plot. 
nStart = 5          # Number of wave cycles to remove initial transient effects.
nFFT_reg = 5        # Number of regular wave cycles for FFT analysis.
nFFT_irreg = 160    # Number of irregular wave cycles for FFT analysis.

#---------------------------------Plot wave data----------------------------#
time = []
elevSims = []
H = []
T = []
for iCase,case in enumerate(sys.argv[1:]):
    rf = cF.readFlowParams(os.path.join(case,"flowParams"))

    if (rf['waveType'] == 0):
        iTime, iElevSims, iH, iT = cF.evalWaveData(sys.argv[iCase+1], iProbe=iProbe, nStart=nStart, nFFT=nFFT_reg, wavePath=wavePath)    
    else:
        iTime, iElevSims, iH, iT = cF.evalWaveData(sys.argv[iCase+1], iProbe=iProbe, nStart=nStart, nFFT=nFFT_irreg, wavePath=wavePath)    
    time.append(iTime)
    elevSims.append(iElevSims)
    H.append(iH)
    T.append(iT)

# Plotting the wave outputs
xlabels = ['Simulated Time (s)', 'Refinement']
ylabels = ['Surface Elevation (m)', '% Change in wave height']

if (nCases == 1):
    plt.plot(time[0], elevSims[0], label='H: ' + str(round(H[0],3))+ ' - T: ' + str(round(T[0],3)))
    plt.xlabel(xlabels[0])
    plt.ylabel(ylabels[0])
    plt.legend(loc='lower left')
else:
    fig , axs = plt.subplots(1,2,figsize=(12,4),width_ratios=[3, 1],tight_layout=True)
    for i in range(nCases):
        axs[0].plot(time[i],elevSims[i], label='H: ' + str(round(H[i],3))+ ' - T: ' + str(round(T[i],3)))
        if (i != 0):
            axs[1].semilogy(i,abs(H[i]-H[i-1])/H[i]*100,'x')


    for i, (xlabel, ylabel) in enumerate(zip(xlabels,ylabels)):
        axs[i].set_xlabel(xlabel)
        axs[i].set_ylabel(ylabel)

    axs[0].legend(loc='lower left')
    axs[1].set_xlim([1e-3,nCases])
    axs[1].set_xticks(ticks=np.arange(nCases+1))
    axs[1].grid(color='lightgrey',which='both')

plt.show()

