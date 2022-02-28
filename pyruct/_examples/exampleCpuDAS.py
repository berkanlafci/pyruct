#-----
# Description   : Example script to use cpu delay and sum beamforming code
# Date          : October 2021
# Author        : Berkan Lafci
# E-mail        : lafciberkan@gmail.com
#-----

#%% Start logging
import logging
logging.basicConfig(filename='exampleCpuDAS.log', filemode='w', level=logging.INFO)
logging.info('  Script      "exampleCpuDAS"     : exampleCpuDAS.py')

#%% Import libraries
import numpy as np
import matplotlib.pyplot as plt

# stop writing __pycache__ files
import sys
sys.dont_write_bytecode = True

from pyruct import *

#%% Data paths (defined by users)
folderPath          = 'data/rawData'
scanName            = 'allenKey_1_pos_1'

#%% read signal file
usData              = usReader(folderPath=folderPath, scanName=scanName, averaging=False)
sigMat              = usData.sigMat

#%% Initialize cpuBP object
das                  = cpuDAS()

#%% Reconstruction parameters (defined by user)
das.speedOfSound        = 1490              # change SoS based on water temperature (default: 1480)
das.fieldOfView         = 0.024             # FOV to reconstruct (default: 0.03)
das.pixelNumber         = 256               # increase this number for higher resolution (default: 128)
das.cupType             = 'ring'            # ring (default: ring)
das.lowCutOff           = 2.5e6             # low cutoff for bandpass (default: 0.1e6)
das.highCutOff          = 6e6               # high cutoff for bandpass (default: 6e6)
das.fSampling           = 24e6              # sampling frequency
das.numRxChannels       = 128               # number of reception channels
das.numTxEvents         = 512               # number of transmission events

#%% Define tranmission/reception channels and delays
traActiveChannels       = np.zeros((das.numTxEvents, das.numElements))
traDelays               = np.zeros((das.numTxEvents, das.numElements))
activeChannels          = np.zeros((das.numTxEvents, das.numRxChannels+1))

traChannelIds           = np.linspace(0, das.numElements, num=das.numTxEvents, dtype=int, endpoint=False)

for eventTxId in range(das.numTxEvents):
    traActiveChannels[eventTxId, traChannelIds[eventTxId]]  = 1
    traDelays[eventTxId, traChannelIds[eventTxId]]          = 3255*(5.5e-9)
    activeChannels[eventTxId,:]                             = np.linspace(eventTxId-int(das.numRxChannels/2),eventTxId+int(das.numRxChannels/2), das.numRxChannels+1, dtype=int)%das.numElements

das.traActiveChannels   = traActiveChannels
das.traDelays           = traDelays
das.activeChannels      = activeChannels

#%% Reconstruction
imageRecon          = das.reconDAS(sigMat)

# %% Visualize reconstructed images (optional)
# plt.figure()
# plt.imshow(imageRecon, cmap='gray')
# plt.show()

#%% Save reconstructed images (optional)

# save as png
imageReconRotated = np.rot90(imageRecon,1)
pngPath = 'data/pngImages'
saveUsImagePng(reconObject=das, pngPath=pngPath, saveName=scanName, imageRecon=imageReconRotated)

# save as mat
imageReconRotated = np.rot90(imageRecon,1)
matPath = 'data/matImages'
saveUsImageMat(reconObject=das, matPath=matPath, saveName=scanName, imageRecon=imageReconRotated)
