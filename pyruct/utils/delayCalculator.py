#-----
# Description   : Delay calculator for DAQ
# Date          : October 2021
# Author        : Berkan Lafci
# E-mail        : lafciberkan@gmail.com
#-----

# Import libraries
import logging

def calculateDelay(fSampling, receptionDelay):
    """
    Calculates delay until signal acquisition starts.

    :param fSampling: Sampling frequency of DAQ
    :param receptionDelay: Delay until reception of signals

    :return: Active delay until acquisition
    """

    logging.info('  Function    "calculateDelay"    : %s', __name__)

    delayOffsetSamples      = 45.8e-6 * fSampling
    activeDelay             = receptionDelay - delayOffsetSamples
    
    return activeDelay
