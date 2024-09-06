import numpy as np
import acoustics as ac
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import *
import acoustics.room as ac
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import numpy as np
import sys
import soundfile as sf

def rt_descriptors(signal, signal_raw, fs):
    # Calculates the time bound descriptors
    # signal ==> filtrada, suavizada
    # rts -> param : init, end, factor
    rts = {'t30' : [-5.0, -35.0, 2.0],
           't20' : [-5.0, -25.0, 3.0],
           't10' : [-5.0, -15.0, 6.0],
           'edt' : [0.0, -10.0, 6.0]}
    params = {}
    
    # np.save('asd.npy', signal_raw)
    
    for rt in rts:
        init, end, factor = rts[rt]
        sch_db = signal
        # Linear regression
        sch_init = sch_db[np.abs(sch_db - init).argmin()]
        sch_end = sch_db[np.abs(sch_db - end).argmin()]
        init_sample = np.where(sch_db == sch_init)[0][0]
        end_sample = np.where(sch_db == sch_end)[0][0]
        x = np.arange(init_sample, end_sample + 1) / fs
        y = sch_db[init_sample:end_sample + 1]
        slope, intercept = ac.stats.linregress(x, y)[0:2]
        # Reverberation time (T30, T20, T10 or EDT)
        db_regress_init = (init - intercept) / slope
        db_regress_end = (end - intercept) / slope
        param = factor * (db_regress_end - db_regress_init)
        params[rt] = param
        
    # clarity -> param : c50/c80
    clarities = {'C50' : 50, 'C80' : 80}
    for clarity in clarities:
        h2 = signal_raw**2.0
        time = clarities[clarity]
        t = int((time / 1000.0) * fs + 1) #Así venía el original
        #t = int(time / 1000.0) * fs 
        c = 10.0 * np.log10((np.sum(h2[:t]) / np.sum(h2[t:])) + sys.float_info.epsilon)
        params[clarity] = c
        
    #tt y edtt
    index = np.where(np.cumsum(signal_raw ** 2) <= 0.99 * np.sum(signal_raw ** 2))[0][-1]
    params['tt'] = index / fs
    signal_mt = signal[:index]
    sch_db = signal_mt
    x = np.arange(0, signal_mt.size) / fs
    y = sch_db[0:signal_mt.size]
    slope, intercept = ac.stats.linregress(x, y)[0:2]
    # Reverberation time (T30, T20, T10 or EDT)
    params['edt_t'] = -60 / slope
    return params


def IACC_e(L, R, fs):
    '''
    Calculate IACCe according to the ISO 3382:2001 standard.
    
    Parameters
    ----------
    L : array
        Left channel input RIR.
    R : array
        Right channel input RIR.
    fs : int
        Sampling frequency.
    
    Returns
    -------
    IACCe : float
        Early interaural cross-correlation coefficient parameter.
    '''
    iacc_er_total = []
    for ir_L, ir_R in zip(L, R):
        t80 = np.int64(0.08*fs) 
        # integral limit of 80 ms is calculated
        I = np.correlate(ir_L[0:t80],ir_R[0:t80],'full')/(np.sqrt(np.sum(ir_L[0:t80]**2)*np.sum(ir_R[0:t80]**2))) 
        # mathematical definition of the IACC is implemented
        iacce = np.max(np.abs(I))

        # values are appended in a vector
        IACCe = np.round(iacce, 2)
        # the obtained values are rounded

        iacc_er_total.append(IACCe)
        
    return iacc_er_total

# data , fs= sf.read('stereo.wav')
# L = data[0]
# R = data[1]
# _IntACC = IACC_e(L, R,fs)
# print(_IntACC)