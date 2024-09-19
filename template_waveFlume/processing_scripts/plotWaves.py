#!/usr/bin/env python3
import numpy as np
import coreFuncs as cF
import matplotlib.pyplot as plt

#---------------------------------Read In Flow Settings----------------------------#
# Set constants and directories
g = 9.81
waveDataDir = '../postProcessing/interfaceHeight1/*/height.dat'

# Read flowParams file and set constant
rf = cF.readFlowParams('../flowParams')

#---------------------------------Plot wave data-----------------------------------#
# Get wave data from '<postProcessing> dir'
[nProbes, time, elevSims] = cF.importElevData(waveDataDir)
Fs = 1/(time[1] - time[0])

# Set the time inverval used for FFT of the simulated waves.
# Used to remove the transient data at the start and the data
# impacted by wave reflection at the end
nS = 8                                          # Remove the initial 8 cycles
nT = 5                                          # Take the next 5 cycles to do FFT
tStart = int(nS*rf["wavePeriod"]*Fs)             
tEnd = int(tStart + nT*rf["wavePeriod"]*Fs)      

# Plot the results and estimate the simulated wave height and period
if (rf["waveType"] == 0):
    for probe in range(nProbes):
        elev = elevSims[probe][tStart:tEnd]
        [Freqs, elevFFT] = cF.fftSignal(Fs, elev)

        H = 2*np.max(abs(elevFFT))
        T = 1/(Freqs[abs(elevFFT).argmax()])

        plt.plot(time,elevSims[probe], label='Probe: ' + str(probe+1) 
                                        + '. H: ' + str(round(H,2))
                                        + '. T: ' + str(round(T,2)))
else:
    for probe in range(nProbes):
        plt.plot(time,elevSims[probe], label='Probe: ' + str(probe+1))

plt.xlabel('Simulated Time (s)')
plt.ylabel('Surface Elevation (m)')

plt.grid()
plt.legend(loc='lower right')
plt.show()
