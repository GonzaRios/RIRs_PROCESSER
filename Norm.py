import numpy as np

def Normal(IIrsFilt,N=100):

    Norm = np.zeros_like(IIrsFilt)
    for i in range(IIrsFilt.shape[0]):
        
        Norm[i, :] =np.log10(IIrsFilt[i, :]/IIrsFilt.max())  

    return Norm

