#!/usr/bin/env python3
import numpy as np
import coreFuncs as cF

#---------------------------------Read In Flow Settings----------------------------#
# Set constants and directories
g = 9.81
tCoeff = 500       # Multiplier of wave period for maximum simulated time (irregular wave)
waveInput = '../constant/waveInput.txt'

# Read flowParams file and set constant
rf = cF.readFlowParams("../flowParams")

# Wave Parameters
if (rf["waveType"] == 1 and rf["waveModel"] != 'userInput'):

    waterDepth = rf["waterDepth"]
    waveHeight = rf["waveHeight"]
    wavePeriod = rf["wavePeriod"]
    tmax = rf["endTime"]
    samplingT = rf["writeElev"]

    if (tmax == 0):
        tmax = tCoeff*wavePeriod

    if (len(rf["waveModel"].split('(')) == 1):
        cF.errCodes(12)

    waveModel =  rf["waveModel"].split('(')[0]
    fOut = rf["waveModel"].split('(')[1].split(',')
    fmin = float(fOut[0])
    fmax = float(fOut[1])
    nf = int(fOut[2][:-1])
    f = np.linspace(fmin, fmax, nf)

    if (waveModel != 'PM' and waveModel != 'Bretschneider' and waveModel != 'Jonswap'):
        print(rf["waveModel"])
        cF.errCodes(5)

    # Write wave components to the '<constant>/waveInput.txt' file
    if (rf["waveType"] == 1 and rf["waveModel"] != 'userInput'):
        with open(waveInput,'w') as fout:
            # Create time and frequency series
            time = np.arange(0, tmax, samplingT)

            if (waveModel == "PM"):
                Sf = cF.pierson_moskowitz_spectrum(f, wavePeriod)
            elif (waveModel == "Bretschneider"):
                Sf = cF.bretschneider_spectrum(f, wavePeriod, waveHeight)
            elif (waveModel == "Jonswap"):
                Sf = cF.jonswap_spectrum(f, wavePeriod, waveHeight, gamma=3.3)
            else:
                cF.errCodes(5)

            # Create time serie parameters from spectrum
            [Amps, Phases] = cF.wave_components(f, Sf, time, seed=123)

            # Calculate wave numbers
            waveK = []
            for i in range(len(f)):
                waveK.append(cF.waveNumber(g, 2*np.pi*f[i], waterDepth))

            cF.writeSpec(fout, waveEngine, f, Amps, Phases, waveK)

else:
    print('The case is set for regular wave. No calculation is performed!')
