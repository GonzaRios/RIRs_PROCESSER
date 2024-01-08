import numpy as np


def filtrado_FMM(signals,window):

    mono_suavizado = np.zeros_like(signals)
    for i in range(signals.shape[0]):
        
        mono_suavizado[i, :] =np.convolve(abs(signals[i, :]), np.ones(window)/window, mode='same')  #Convoluciono mono el valor absoluto con la ventande MM

    return mono_suavizado