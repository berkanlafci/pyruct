#-----
# Description   : Example script to use cpu delay and sum code
# Compatibility : Razansky Lab Systems
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

# stop wiriting __pycache__ files
import sys
sys.dont_write_bytecode = True

from pyruct import *

#%% Data paths (defined by users)
folderPath          = 'data/rawData'
scanName            = 'allenKey_1_pos_1_nct_1_ncr_1_nst_1_nsr_1'

#%% read signal file
usData              = usReader(folderPath=folderPath, scanName=scanName, averaging=False)
sigMat              = usData.sigMat

#%% Initialize cpuBP object
das                  = cpuDAS()

#%% Reconstruction parameters (defined by user)
das.speedOfSound        = 1490              # change SoS based on water temperature (default: 1480)
das.fieldOfView         = 0.024             # FOV to reconstruct (default: 0.03)
das.pixelNumber         = 256               # increase this number for higher resolution (default: 128)
das.cupType             = 'ring'            # ring, multisegment, virtualRing (default: ringCup)
das.lowCutOff           = 0.5e6             # low cutoff for bandpass (default: 0.1e6)
das.highCutOff          = 6e6               # high cutoff for bandpass (default: 6e6)
das.fSampling           = 24e6              # sampling frequency
das.numRxChannels       = 128               # number of reception channels
das.numTxEvents         = 512               # number of transmission events

#%% Define tranmission channels and delays
traActiveChannels       = np.zeros((das.numTxEvents,das.numElements))
traDelays               = np.zeros((das.numTxEvents,das.numElements))

for traInd in range(das.numTxEvents):
    traActiveChannels[traInd, traInd]   = 1
    traDelays[traInd, traInd]           = 3255*(5.5e-9)

das.traActiveChannels   = traActiveChannels
das.traDelays           = traDelays

#%% Define reception channels
activeChannels          = np.zeros((das.numRxChannels+1, das.numElements))
for colInd in range(512):
    activeChannels[:, colInd] = np.linspace(colInd-int(das.numRxChannels/2),colInd+int(das.numRxChannels/2), das.numRxChannels+1, dtype=int)%das.numElements

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
saveUsImagePng(reconObject=das, pngPath=pngPath, saveName='DAS_'+scanName, imageRecon=imageReconRotated)

# save as mat
imageReconRotated = np.rot90(imageRecon,1)
matPath = 'data/matImages'
saveUsImageMat(reconObject=das, matPath=matPath, saveName='DAS_'+scanName, imageRecon=imageReconRotated)
