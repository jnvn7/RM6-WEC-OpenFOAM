#!/usr/bin/env python3
import numpy as np
import coreFuncs as cF
import matplotlib.pyplot as plt
#-------------------------------Adjust some plot settings----------------------------#
plt.rcParams['figure.dpi'] = 400
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

#---------------------------------Read In Flow Settings----------------------------#
# Set constants and directories
g = 9.81

waveDataPrePackDir = '../prePackaged-postProcessing/interfaceHeight1/*/height.dat'
waveDataDir = '../postProcessing/interfaceHeight1/*/height.dat'

# Read flowParams file and set constant
rf = cF.readFlowParams('../flowParams')

#---------------------------------Plot wave data-----------------------------------#
# Get wave data from '<postProcessing> dir'
[nProbes, time, elevSims] = cF.importElevData(waveDataDir)

# Get prepackaged wave data from '<postProcessing-prePackaged> dir'
[nProbesPrePack, timePrePack, elevSimsPrePack] = cF.importElevData(waveDataPrePackDir)

# Make sure we are using the same number of probes in both data sets: 
if (nProbes != nProbesPrePack):
    print(f'Error -- the pre-packaged data has {nProbesPrePack:d} wave probes, but the data to compare has {nProbes:d} wave probes. These should be the same for proper comparison. ')
    exit()


# Create a figure of subplots to house all the probe comparison plots: 
figheight = 5.0
figwidth = 7.0
fig_, axs_ = plt.subplots(nProbes, 1, 
                          figsize = (figwidth, figheight*nProbes*1.1), tight_layout = True)

# Plot the pre-packaged data vs user-generated for each probe
for probe in range(nProbes):
    curr_ax = axs_[probe]
    curr_ax.plot(timePrePack, elevSimsPrePack[probe], '-', linewidth = 2, label = 'Pre-packaged')
    curr_ax.plot(time, elevSims[probe], '--', linewidth = 2, label = 'User-generated')

    curr_ax.set_title(f'Probe {probe:d}')

    curr_ax.grid(visible=True)
    curr_ax.legend(loc='lower right')

    curr_ax.set_xlabel('Simulated Time (s)')
    curr_ax.set_ylabel('Surface Elevation (m)')
plt.show()
