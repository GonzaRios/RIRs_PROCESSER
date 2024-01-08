import numpy as np

def schroeder(F_IR):
    
    # This function calculates the schroeder cumulative sum of the filtered IR

    sch_int = np.cumsum(F_IR[::-1]**2)[::-1]
    sch_int_dB = 10.0 * np.log10(sch_int / np.max(sch_int)) 
    return sch_int_dB