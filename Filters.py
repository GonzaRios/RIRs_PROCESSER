
import numpy as np
from scipy import signal
import soundfile as sf
from matplotlib import pyplot as plt


def filtroter(IR_L, IR_R, fs, ter):
    '''
    Filter a stereo impulse response according to the UNE-EN 61260 standard,
    using passband Butterworth filters.
    
    Parameters
    ----------
    IR_L : array
        Left channel input signal.
    IR_R : array
        Right channel input signal.
    fs : int
        Sampling frequency.
    ter : bool
        Filter by third octave (True) or octave band (False).
    Returns
    -------
    IR_L_filt : array
        Filtered left channel impulse response.
    IR_R_filt : array
        Filtered right channel impulse response.
    centrosHZ : array
        Filter's center frequencies.
    '''
    
    filtradaL = filtroter_mono(IR_L, fs, ter)
    filtradaR = filtroter_mono(IR_R, fs, ter)
    
    IR_L_filt = filtradaL[0]
    IR_R_filt = filtradaR[0]
    centrosHZ = filtradaL[1]
                    
    return  IR_L_filt, IR_R_filt, centrosHZ

def filtroter_mono(IR, fs, ter):
    '''
    Filter an impulse response according to the UNE-EN 61260 standard, using
    passband Butterworth filters.   
    
    Parameters
    ----------
    IR : array
        Input signal.
    fs : int
        Sampling frequency.
    ter : bool
        Filter by third octave (True) or octave band (False).

    Returns
    -------
    IR_filt : array
        Filtered impulse response.
    centrosHZ : array
        Filter's center frequencies.

    '''
    
    # Invert the impulse response and initialize variables
    
    W = np.flip(IR) 
    G = 10**(3/10)
    fil = []

    if ter:
        centrosHZ = np.array([25, 31.5, 40, 50, 63, 80, 100, 125, 160, 200, 
                              250, 315, 400, 500, 630, 800, 1000, 1250, 1600,
                              2000, 2500, 3150, 4000, 5000, 6300, 8000, 10000,
                              12500, 16000, 20000])
        fmin = G ** (-1/6)
        fmax = G ** (1/6)
    else:
        centrosHZ = np.array([31.5, 63, 125, 250, 500, 1000, 2000, 4000,
                              8000, 16000])
        fmin = G ** (-1/2)
        fmax = G ** (1/2)
            
    for j, fc in enumerate(centrosHZ):
        
        # Define the upper and lower limits of the frequency band

        sup = fmax*fc/(0.5*fs) 
        
        if sup >= 1:
            sup = 0.999999
            
        inf = fmin * fc / (0.5*fs) # Límite inferior

    # Apply the Nth order IIR Butterworth filter.
        
        sos = signal.butter(N=2, Wn=np.array([inf, sup]), 
                            btype='bandpass',output='sos')
        
        filt = signal.sosfilt(sos, W)
        fil.append(filt) 
        fil[j] = np.flip(fil[j])
    
    IR_filtrada = np.array(fil)
    
    # Cut the last 5% of the signal to minimize the border effect
    
    IR_filt = IR_filtrada[:int(len(fil[1])*0.95)]
    
    return IR_filt, centrosHZ

def Normal(self, IIrsFilt,N=100):

    Norm = np.zeros_like(IIrsFilt)
    for i in range(IIrsFilt.shape[0]):
        
        Norm[i, :] =np.log10(IIrsFilt[i, :]/IIrsFilt.max())  

    return Norm


# dataWav, dataFs = sf.read('rir_mono.wav')
# IR_filt, centrosHZ = filtroter_mono(dataWav, dataFs, False)
# IR_Norm = Normal(IR_filt, N=100)

# _matrixNorm =  20*IR_Norm

# plt.plot( _matrixNorm[2])
# plt.show()
# plt.grid()