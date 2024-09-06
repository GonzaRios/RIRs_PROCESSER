import soundfile as sf
import numpy as np
import sys
import scipy.io.wavfile as waves


class ImportarRI():
    def __init__(self):
 
        self.filename = str      # Nombre del archivo.
        self.fs = None           # Sample Rate.
        self.data = None         # Info de las RI. Tanto "mono" como "estereo". 
        self.mono = None         # Variable para RIRs mono.
        self.LCh = None          # Variable para canal izquierdo de RIRs estereo.
        self.RCh = None          # Variable para canal derecho de RIRs estereo.
        
#%%
    def read_IR(self,fileName ): 
        """Lector de Respuestas al impulso
        
        Parameters:
        -----------

        fileName : str
            Nombre del directorio donde se encuntra la RI a describir.
        
        Returns: 
        ------
        self.fs , self.mono, self.LCh , self.RCh: tuple
            Tupla comprendida entre la frecuencia de muestreo y los canales 
            mono y estéreo de la RI.
        """
        
        self.filename = fileName
        self.data, self.fs = sf.read(self.filename)   
        _shape = np.shape(self.data)
        _shapeLen = len(_shape)

        if _shapeLen == 2:  
            self.LCh = self.data[:, 0]   
            self.RCh = self.data[:, 1]  

        elif _shapeLen == 1:
            self.mono = self.data

        else:
            pass
 
        return self.fs , self.mono, self.LCh , self.RCh
