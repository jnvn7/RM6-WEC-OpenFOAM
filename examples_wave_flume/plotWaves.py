#!/usr/bin/env python3
#---------------------------------------------------------------------------#
import numpy as np
import coreFuncs as cF
import matplotlib.pyplot as plt
import sys
import os
#-------------------------------Adjust some plot settings----------------------------#
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

#---------------------------------Plot wave data----------------------------#
# Read inputs
nCases = len(sys.argv)-1
if (nCases < 1):
    print('Missing case input(s) for plotting!')
    sys.exit()

# Extract wave data
# Default for wavePath is in OpenFOAM <postProcessing>. 
# Here it is set to pre-packeged data
wavePath = 'prePackaged_postProcessing/waveProbes/*/height.dat'
time = []
elevSims = []
H = []
T = []
for iCase,case in enumerate(sys.argv[1:]):
    rf = cF.readFlowParams(os.path.join(case,'flowParams'))

    if (rf['waveType'] == 0):
        iTime, iElevSims, iH, iT = cF.evalWaveData(sys.argv[iCase+1], iProbe=3, nStart=5, nFFT=5, wavePath=wavePath)    
    else:
        iTime, iElevSims, iH, iT = cF.evalWaveData(sys.argv[iCase+1], iProbe=3, nStart=5, nFFT=160, wavePath=wavePath)    
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

