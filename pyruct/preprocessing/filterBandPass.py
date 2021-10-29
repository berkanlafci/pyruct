#-----
# Description   : Bandpass filter for signals
# Compatibility : Razansky Lab Systems
# Date          : October 2021
# Author        : Berkan Lafci
# E-mail        : lafciberkan@gmail.com
#-----

import logging
import time
import numpy as np
from scipy.signal import butter, lfilter, filtfilt

def sigMatFilter(sigMat, lowCutOff=0.5e6, highCutOff=6e6, fSampling=40e6, fOrder=3, conRatio=0.5):
    """
    Band pass filtering for signals

    :param sigMat: 3D array (samples x channels x repetition) of signals
    :param lowCutOff: Low cut off frequency of bandpass filter
    :param highCutOff: High cut off frequency of bandpass filter
    :param fSampling: Sampling frequency of signals
    :param fOrder: Butterworth filter order
    :param conRatio: Nyquist ratio percentage

    :return: 3D filtered signal array
    """
    logging.info('  Function    "sigMatFilter"      : %s', __name__)

    #++++++++++++++++++++++++++++++++#
    # bandpass filter function
    
    print('***** filtering *****')
    startTime       = time.time()
   
    sigMatF         = np.zeros(np.shape(sigMat))
    
    nyquistRatio    = conRatio * fSampling
    lowCutOff       = lowCutOff / nyquistRatio
    highCutOff      = highCutOff / nyquistRatio
    lowF, highF     = butter(fOrder, [lowCutOff, highCutOff], btype='bandpass')
    
    sigMatF = filtfilt(lowF, highF, sigMat, padlen=0)

    endTime = time.time()
    print('time elapsed: %.2f' %(endTime-startTime))
    
    return sigMatF