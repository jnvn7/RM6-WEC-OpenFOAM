#!/usr/bin/env python3
import sys
import os
import numpy as np
import pandas as pd
import glob
from scipy import signal
from scipy.integrate import simps
#--------------------------------Read in Parameters---------------------------#
# Constants and directory setup
g = 9.81
waveDataPath = '/postProcessing/interfaceHeight1/*/height.dat'

#--------------------------------Read in Parameters---------------------------#
# Read flowParams parameters
def readFlowParams(flowParamsFile):
    ufData = pd.read_csv(flowParamsFile, sep="\s+|\t", header=None, skiprows = 11,
                            names = range(1000), engine="python")

    rOut = {'sim3D':[],'waveEngine':[],'waveType':[],'Uin':0.0,'waterDepth':[],
		    'waveHeight':[],'wavePeriod':[],'waveAngle':0.0,'wavePhase':0.0,
            'endTime':[],'writeElev':0.01,'writeVTK':1.0,'Probe1':0.0,
            'Probe2':0.0,'Probe3':0.0,'Probe4':0.0,'Probe5':0.0,'dtContr':1.0,
		    'startTime':0.0,'waveModel':[]}

    varNames = list(rOut.keys())
    varList = ufData[:][0]
    varValues = ufData[:][1]

    for i in range(len(varNames)):
        for j in range(len(varValues)):
            if (str(varList[j]) == varNames[i]):
                value = varValues[j].split(';')[0]
                if (i < 3):
                    rOut[varNames[i]] = int(value)
                elif (i >= 3 and i < 19):
                    rOut[varNames[i]] = float(value)
                else:
                    rOut[varNames[i]] = value
                break

    # Check input parameters
    for i in range(len(varNames)):
        if (rOut[varNames[i]] == []):
            print('Missing input for parameter(s): ' + varNames[i])
            errCodes(13)

    if (rOut['waveType'] != 0 and rOut['waveType'] != 1):
        errCodes(9)

    return rOut

#--------------------------Get wave prob data---------------------------#
def importWaveData(case, wavePath=waveDataPath):
    eleFile = sorted(glob.glob(case+wavePath))

    if (len(eleFile)==0):
        print('No elevation data found. Check wavePath input!')
        sys.exit()

    data = pd.read_csv(eleFile[0], sep="\s+|\t", header=None, engine="python")
    nProbes = int((len(data.columns)-1)/2)

    for i in range(1,len(eleFile)):
        dataTemp = pd.read_csv(eleFile[i], sep="\s+|\t", header=None, engine="python")
        data = pd.concat([data, dataTemp],ignore_index=True, sort=False)

    # Import Data
    time = data[0]
    eleSims = []

    for i in range(nProbes):
        eleSims.append(data[:][2*(i+1)])
        eleSims[i] -= eleSims[i][0]

    return (nProbes, time, eleSims)

def evalWaveData(case, wavePath=waveDataPath, iProbe=3, nStart=8, nFFT=5):
    # Read In Flow Settings
    g = 9.81
    iProbe -= 1

    # Read flowParams file and set constant
    rf = readFlowParams(case+'/flowParams')

    # Get wave data from '<postProcessing> dir'
    [nProbes, time, elevSims] = importWaveData(case, wavePath)
    Fs = 1/(time[1] - time[0])

    # Set the time inverval used for FFT of the simulated waves.
    # Used to remove the transient data at the start and the data
    # impacted by wave reflection at the end
    tStart = int(nStart*rf["wavePeriod"]*Fs)             # Remove the initial nStart cycles
    tEnd = int(tStart + nFFT*rf["wavePeriod"]*Fs)        # Take the next nFFT cycles to do FFT

    # Plot the results and estimate the simulated wave height and period
    if (rf["waveType"] == 0):
        elev = elevSims[iProbe][tStart:tEnd]
        [Freqs, elevFFT] = fftSignal(Fs, elev)

        H = 2*np.max(abs(elevFFT))
        T = 1/(Freqs[abs(elevFFT).argmax()])
    else:
        elev = elevSims[iProbe][tStart:tEnd]
        fOut = calcPSD_Hs(Fs, elev, len(elev))
        T = 1/fOut[2]
        H = fOut[3]

    return time, elevSims[iProbe], H, T

#--------------------------Wave Functions---------------------------#
# FFT signal function
def fftSignal(Fs, signal):
    n = len(signal)
    signalFFT = np.fft.fft(signal)/n
    signalFFT = 2*signalFFT[range(n//2)]
    Freqs = np.arange(n//2)*Fs/n

    return (Freqs, signalFFT)

# Wave Dispersion Calculation using Newton Raphson
def waveNumber(g, omega, d):
    k0 = 1;
    err = 1;
    count = 0;
    while (err >= 10e-8 and count <= 100):
        f0 = omega*omega - g*k0*np.tanh(k0*d)
        fp0 = -g*np.tanh(k0*d)-g*k0*d*(1-np.tanh(k0*d)*np.tanh(k0*d))
        k1 = k0 - f0/fp0
        err = abs(k1-k0)
        k0 = k1
        count += 1

    if (count >= 100):
        print('Can\'t find solution for dispersion equation!')
        exit()
    else:
        return(k0)

# Wave Spectrums
def wave_components(f,S, time, seed=123, frequency_bins=None,phases=None):
    """
    Calculates wave elevation time-series from spectrum

    Parameters
    ------------
    S: pandas DataFrame
        Spectral density [m^2/Hz] indexed by frequency [Hz]
    time_index: numpy array
        Time used to create the wave elevation time-series [s],
        for example, time = np.arange(0,100,0.01)
    seed: int (optional)
        Random seed
    frequency_bins: numpy array or pandas Series (optional)
        Bin widths for frequency of S. Required for unevenly sized bins
    phases: numpy array or pandas DataFrame (optional)
        Explicit phases for frequency components (overrides seed)
        for example, phases = np.random.rand(len(S)) * 2 * np.pi

    Returns
    ---------
    eta: pandas DataFrame
        Wave surface elevation [m] indexed by time [s]

    """

    start_time = time[0]
    end_time = time[len(time)-1]      

    nf=len(f)
    if frequency_bins is None:
        delta_f = np.empty(nf)
        delta_f[0] = 0
        delta_f[1:] = f[1:] - f[:-1]

    if phases is None:
        np.random.seed(seed)
        phase = 2*np.pi*np.random.rand(nf)

    # Wave amplitude times delta f, truncated
    A = 2*S
    A = A*delta_f
    A = np.sqrt(A)
    return [A,phase]

def pierson_moskowitz_spectrum(f, Tp):
    """
    Calculates Pierson-Moskowitz Spectrum from Tucker and Pitt (2001)

    Parameters
    ------------
    f: numpy array
        Frequency [Hz]
    Tp: float/int
        Peak period [s]

    Returns
    ---------
    S: pandas DataFrame
        Spectral density [m^2/Hz] indexed frequency [Hz]

    """
    try:
        f = np.array(f)
    except:
        pass
    assert isinstance(f, np.ndarray), 'f must be of type np.ndarray'
    assert isinstance(Tp, (int,float)), 'Tp must be of type int or float'

    f.sort()
    g = 9.81
    B_PM = (5/4)*(1/Tp)**(4)
    A_PM = 0.0081*g**2*(2*np.pi)**(-4)
    Sf  = A_PM*f**(-5)*np.exp(-B_PM*f**(-4))

    return Sf

def bretschneider_spectrum(f, Tp, Hs):
    """
    Calculates Bretschneider Sprectrum from Tucker and Pitt (2001)

    Parameters
    ------------
    f: numpy array
        Frequency [Hz]
    Tp: float/int
        Peak period [s]
    Hs: float/int
        Significant wave height [m]

    Returns
    ---------
    S: pandas DataFrame
        Spectral density [m^2/Hz] indexed by frequency [Hz]

    """
    try:
        f = np.array(f)
    except:
        pass
    assert isinstance(f, np.ndarray), 'f must be of type np.ndarray'
    assert isinstance(Tp, (int,float)), 'Tp must be of type int or float'
    assert isinstance(Hs, (int,float)), 'Hs must be of type int or float'

    f.sort()
    B_BS = (1.057/Tp)**4
    A_BS = B_BS*(Hs/2)**2
    Sf = A_BS*f**(-5)*np.exp(-B_BS*f**(-4))

    return Sf

def jonswap_spectrum(f, Tp, Hs, gamma=3.3):
    """
    Calculates JONSWAP spectrum from Hasselmann et al (1973)
    
    Parameters
    ------------
    f: numpy array
        Frequency [Hz]
    Tp: float/int
        Peak period [s]
    Hs: float/int
        Significant wave height [m]    
    gamma: float (optional)
        Gamma
    
    Returns
    ---------    
    S: pandas DataFrame
        Spectral density [m^2/Hz] indexed frequency [Hz]
    """

    try:
        f = np.array(f)
    except:
        pass
    assert isinstance(f, np.ndarray), 'f must be of type np.ndarray'
    assert isinstance(Tp, (int,float)), 'Tp must be of type int or float'
    assert isinstance(Hs, (int,float)), 'Hs must be of type int or float'
    assert isinstance(gamma, (int,float)), 'gamma must be of type int or float'

    f.sort()
    g = 9.81

    # Cutoff frequencies for gamma function
    siga = 0.07
    sigb = 0.09

    fp = 1/Tp # peak frequency
    lind = np.where(f<=fp)
    hind = np.where(f>fp)
    Gf = np.zeros(f.shape)
    Gf[lind] = gamma**np.exp(-(f[lind]-fp)**2/(2*siga**2*fp**2))
    Gf[hind] = gamma**np.exp(-(f[hind]-fp)**2/(2*sigb**2*fp**2))
    S_temp = g**2*(2*np.pi)**(-4)*f**(-5)*np.exp(-(5/4)*(f/fp)**(-4))
    alpha_JS = Hs**(2)/16/np.trapz(S_temp*Gf,f)
    Sf = alpha_JS*S_temp*Gf # Wave Spectrum [m^2-s] 

    return Sf

def calcPSD_Hs(Fs, eta, nfft):
    [f, PSD] = signal.welch(eta, Fs, window='hann', nperseg=nfft, nfft=nfft, 
                                                        noverlap=None)
    Hs = 4*np.sqrt(simps(PSD, dx = f[2]-f[1]))
    fMax = f[PSD.argmax()]

    return [f, PSD, fMax, Hs]

#------------------------------Write Data to File-----------------------------#
def writeSpec(fout, waveEngine, f, amps, phases, waveK):

    nvals=len(f)
    H=amps*2.0
    T=1.0/f

    ## directions are all 0 for now
    DD=[0.0]*nvals

    numfmt='{:15.8e}'
    if (waveEngine == 0):
        outfmt='((' + (numfmt+' ')*(nvals-1) + numfmt + '));\n'
    elif (waveEngine == 1):
        outfmt='(' + (numfmt+' ')*(nvals-1) + numfmt + ');\n'
    else:
        outfmt='(\n' + (numfmt+'\n')*(nvals-1) + numfmt + '\n);\n'
        outfmt2='(\n' + ('(\t'+numfmt+'\t0\t0 )\n')*(nvals-1) + '(\t' + numfmt + '\t0\t0 )' + '\n);\n'

    # Wave Heights
    if (waveEngine != 2):
        lineout='waveHeights\n'
    else:
        lineout='waveAmps nonuniform List<scalar>\n'
    fout.write(lineout)
    if (waveEngine == 0):
        lineout='1\n'
    else:
        lineout=str(nvals)+'\n'

    fout.write(lineout)
    if (waveEngine != 2):
        lineout=outfmt.format(*H)
    else:
        lineout=outfmt.format(*H/2)
    fout.write(lineout)

    # Wave Periods
    if (waveEngine != 2):
        lineout='wavePeriods\n'
    else:
        lineout='wavePeriods nonuniform List<scalar>\n'
    fout.write(lineout)
    if (waveEngine == 0):
        lineout='1\n'
    else:
        lineout=str(nvals)+'\n'
    fout.write(lineout)
    if (waveEngine != 2):
        lineout=outfmt.format(*T)
    else:
        lineout=outfmt.format(*f)
    fout.write(lineout)

    # Wave Phases
    if (waveEngine != 2):
        lineout='wavePhases\n'
    else:
        lineout='wavePhases nonuniform List<scalar>\n'

    fout.write(lineout)
    if (waveEngine == 0):
        lineout='1\n'
    else:
        lineout=str(nvals)+'\n'
    fout.write(lineout)
    lineout=outfmt.format(*phases)
    fout.write(lineout)

    # Wave Angles/Dirs/Numbers
    if (waveEngine != 2):
        lineout='waveAngles\n'
        fout.write(lineout)
        if (waveEngine == 0):
            lineout='1\n'
        else:
            lineout=str(nvals)+'\n'
        fout.write(lineout)
        lineout=outfmt.format(*DD)
        fout.write(lineout)

        # Directions are assumed to be 0 for now
        lineout='waveDirs\n'
        fout.write(lineout)
        if (waveEngine == 0):
            lineout='1\n'
        else:
            lineout=str(nvals)+'\n'
        fout.write(lineout)
        lineout=outfmt.format(*DD)
        fout.write(lineout)
    else:
        lineout='waveNumbers nonuniform List<vector>\n'
        fout.write(lineout)
        lineout=str(nvals)+'\n'
        fout.write(lineout)
        lineout=outfmt2.format(*waveK)
        fout.write(lineout)

#---------------------------------Error Codes---------------------------------#
# Define Error Codes
def errCodes(error):
    print()

    if (error == 1):
        print('Cant use options -a and -p at the same time!')

    elif (error == 2):
        print('Missing Probe Number. See -help!')
        print()
        print(Usage)
    
    elif (error == 3):
        print('Numbers of Probes Specified are larger than available!')

    elif (error == 4):
        print('Specified probes are larger than available!')

    elif (error == 5):
        print('Unsupported Spectrum Model. Try: PM, Bretschneider, or Jonswap!')

    elif (error == 6):
        print('Unsupported waveType. 0: Regular Waves - 1: Irregular Waves.')

    elif (error == 7):
        print('Unsupported format for Irregular Wave Spectrum and Frequency. \n\n'+
                'Format: ModelName(fmix,fmax,#points). No spacing!')

    elif (error == 8):
        print('Background refinement process is stopped. \n'+
              'Refinement zone is larger than the tank dimensions.')

    elif (error == 9):
        print('Invalid waveType input. 0: Regular Waves. 1: Irregular Waves.')

    elif (error == 10):
        print('Invalid waveEngine input. 0: IHFOAM. 1: OLAFLOW. 2: waves2Foam')

    elif (error == 11):
        print('Invalid sim3D input. 0: 2D. 1: 3D')

    elif (error == 12):
        print('Invalid waveModel format for irregular waves. Format: ModelName(fmin,fmax,#points) with no sapcing!')

    elif (error == 13):
        print('Error parsing flowParams file.')

    print()
    sys.exit(1)

