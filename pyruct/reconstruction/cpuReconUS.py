#-----
# Description   : Beamformer functions on CPU
# Compatibility : Razansky Lab Systems
# Date          : October 2021
# Author        : Berkan Lafci
# E-mail        : lafciberkan@gmail.com
#-----

# import libraries
import time
import h5py
import logging
import numpy as np
import pkg_resources as pkgr
from scipy.signal import hilbert

#---------------------------------------------------------------------------------------------------------------------------#
#------------------------------------------------------ delay and sum ------------------------------------------------------#
#---------------------------------------------------------------------------------------------------------------------------#

# delay and sum beamformer
class cpuDAS():
    """
    Delay and sum reconstruction class on CPU for reflection ultrasound computed tomography (RUCT) imaging

    :param fieldOfView:         Field of view in x and y direction in meters (default: 0.03)
    :param pixelNumber:         Number of pixels in image (default: 128)
    :param xSensor:             X position of transducer elements (default: Ring array positions)
    :param ySensor:             Y position of transducer elements (default: Ring array positions)
    :param cupType:             Array type used in experiment (default: Ring array)
    :param speedOfSound:        Estimated speed of sound (m/s) based on temperature (default: 1540 m/s)
    :param nSamples:            Number of samples in sigMat (default: 2032)
    :param fSampling:           Sampling frequency of signals (default: 40e6)
    :param reconType:           Reconstruction type for backprojection (default: full)
    :param delayInSamples:      Active delay of signals
    :param lowCutOff:           Low cut off frequency of bandpass filter in MHz (default: 0.1e6 MHz)
    :param highCutOff:          High cut off frequency of bandpass filter in MHz (default: 6e6 MHz)
    :param fOrder:              Butterworth filter order
    :param traActiveChannels:   Active channels in transmission (numTxEvents x numChannels)
    :param traDelays:           Delays of active transmission channels (numTxEvents x numChannels)
    :param activeChannels:      Active channels in reception (numTxEvents x numRxChannels)

    :return:                    cpuDAS object
    """
   
    # initialization for class cpuDAS
    def __init__(self):
        logging.info('  Class       "cpuDAS"            : %s', __name__)
       
        self._fieldOfView       = 0.03
        self._pixelNumber       = 128
        self._xSensor           = {}
        self._ySensor           = {}
        self._numElements       = {}
        self._cupType           = 'ring'
        self._speedOfSound      = 1540
        self._nSamples          = 2032
        self._fSampling         = 24e6
        self._delayInSamples    = 1400
        self._lowCutOff         = 0.1e6
        self._highCutOff        = 6e6
        self._fOrder            = 3
        self._traActiveChannels = {}
        self._traDelays         = {}
        self._activeChannels    = {}
        self._numTxEvents      = {}
        self.__numTxChannels    = {}
        self._numRxChannels    = {}
        
    #--------------------------------#
    #---------- properties ----------#
    #--------------------------------#

    #--------------------------------#
    # cup type

    @property
    def cupType(self):
        return self._cupType

    @cupType.setter
    def cupType(self, value):
        logging.info('  Property    "cupType"           : %s', value)
        self._cupType       = value
        self.__arrayDir     = pkgr.resource_filename('pyruct', 'arrays/'+self._cupType+'Cup.mat')
        self.__arrayData    = h5py.File(self.__arrayDir, 'r')
        self.xSensor        = self.__arrayData['transducerPos'][0,:]
        self.ySensor        = self.__arrayData['transducerPos'][1,:]
        self.numElements    = np.shape(self.xSensor)[0]

    @cupType.deleter
    def cupType(self):
        del self._cupType
        del self.xSensor
        del self.ySensor
        del self.rSensor

    #--------------------------------#
    # x positions of sensor

    @property
    def xSensor(self):
        return self._xSensor

    @xSensor.setter
    def xSensor(self, value):
        self._xSensor = value

    @xSensor.deleter
    def xSensor(self):
        del self._xSensor
    
    #--------------------------------#
    # y positions of sensor

    @property
    def ySensor(self):
        return self._ySensor

    @ySensor.setter
    def ySensor(self, value):
        self._ySensor = value

    @ySensor.deleter
    def ySensor(self):
        del self._ySensor

    #--------------------------------#
    # number of elements in array

    @property
    def numElements(self):
        return self._numElements

    @numElements.setter
    def numElements(self, value):
        self._numElements = value
        assert value == np.shape(self.xSensor)[0], "Number of elements is not equal to array dimensions."
        
    @numElements.deleter
    def numElements(self):
        del self._numElements

    #--------------------------------#
    # field of view

    @property
    def fieldOfView(self):
        return self._fieldOfView

    @fieldOfView.setter
    def fieldOfView(self, value):
        logging.info('  Property    "fieldOfView"       : %.4f m', value)
        self._fieldOfView = value

    @fieldOfView.deleter
    def fieldOfView(self):
        del self._fieldOfView

    #--------------------------------#
    # pixel number

    @property
    def pixelNumber(self):
        return self._pixelNumber

    @pixelNumber.setter
    def pixelNumber(self, value):
        logging.info('  Property    "pixelNumber"       : %d ', value)
        self._pixelNumber = value

    @pixelNumber.deleter
    def pixelNumber(self):
        del self._pixelNumber

    #--------------------------------#
    # speed of sound

    @property
    def speedOfSound(self):
        return self._speedOfSound

    @speedOfSound.setter
    def speedOfSound(self, value):
        logging.info('  Property    "speedOfSound"      : %d m/s', value)
        self._speedOfSound = value

    @speedOfSound.deleter
    def speedOfSound(self):
        del self._speedOfSound

    #--------------------------------#
    # number of samples

    @property
    def nSamples(self):
        return self._nSamples

    @nSamples.setter
    def nSamples(self, value):
        logging.info('  Property    "nSamples"          : %d ', value)
        self._nSamples = value

    @nSamples.deleter
    def nSamples(self):
        del self._nSamples

    #--------------------------------#
    # sampling frequency

    @property
    def fSampling(self):
        return self._fSampling

    @fSampling.setter
    def fSampling(self, value):
        logging.info('  Property    "fSampling"         : %d Hz', value)
        self._fSampling = value

    @fSampling.deleter
    def fSampling(self):
        del self._fSampling

    #--------------------------------#
    # delay in samples

    @property
    def delayInSamples(self):
        return self._delayInSamples

    @delayInSamples.setter
    def delayInSamples(self, value):
        logging.info('  Property    "delayInSamples"    : %.4f ', value)
        self._delayInSamples = value

    @delayInSamples.deleter
    def delayInSamples(self):
        del self._delayInSamples

    #--------------------------------#
    # low cutoff frequency of filter

    @property
    def lowCutOff(self):
        return self._lowCutOff

    @lowCutOff.setter
    def lowCutOff(self, value):
        logging.info('  Property    "lowCutOff"         : %d Hz', value)
        self._lowCutOff = value

    @lowCutOff.deleter
    def lowCutOff(self):
        del self._lowCutOff

    #--------------------------------#
    # high cutoff frequency of filter

    @property
    def highCutOff(self):
        return self._highCutOff

    @highCutOff.setter
    def highCutOff(self, value):
        logging.info('  Property    "highCutOff"        : %d Hz', value)
        self._highCutOff = value

    @highCutOff.deleter
    def highCutOff(self):
        del self._highCutOff

    #--------------------------------#
    # order of filter

    @property
    def fOrder(self):
        return self._fOrder

    @fOrder.setter
    def fOrder(self, value):
        logging.info('  Property    "fOrder"            : %d ', value)
        self._fOrder = value

    @fOrder.deleter
    def fOrder(self):
        del self._fOrder
 
    #--------------------------------#
    # active transmission channels

    @property
    def traActiveChannels(self):
        return self._traActiveChannels

    @traActiveChannels.setter
    def traActiveChannels(self, value):
        logging.info('  Property    "traActiveChannels" : size {} '.format(np.shape(value)) )
        self._traActiveChannels = value

    @traActiveChannels.deleter
    def traActiveChannels(self):
        del self._traActiveChannels     

    #--------------------------------#
    # transmission delays

    @property
    def traDelays(self):
        return self._traDelays

    @traDelays.setter
    def traDelays(self, value):
        logging.info('  Property    "traDelays"         : size {} '.format(np.shape(value)) )
        self._traDelays = value

    @traDelays.deleter
    def traDelays(self):
        del self._traDelays
 
    #--------------------------------#
    # active reception channels

    @property
    def activeChannels(self):
        return self._activeChannels

    @activeChannels.setter
    def activeChannels(self, value):
        logging.info('  Property    "activeChannels"    : size {} '.format(np.shape(value)) )
        self._activeChannels = value

    @activeChannels.deleter
    def activeChannels(self):
        del self._activeChannels

    #--------------------------------#
    # number of transmission events

    @property
    def numTxEvents(self):
        return self._numTxEvents

    @numTxEvents.setter
    def numTxEvents(self, value):
        self._numTxEvents = value

    @numTxEvents.deleter
    def numTxEvents(self):
        del self._numTxEvents

    #--------------------------------#
    # number of transmission channels

    @property
    def numTxChannels(self):
        return self.__numTxChannels

    @numTxChannels.setter
    def numTxChannels(self, value):
        self.__numTxChannels = value

    @numTxChannels.deleter
    def numTxChannels(self):
        del self.__numTxChannels

    #--------------------------------#
    # number of reception channels

    @property
    def numRxChannels(self):
        return self._numRxChannels

    @numRxChannels.setter
    def numRxChannels(self, value):
        self._numRxChannels = value

    @numRxChannels.deleter
    def numRxChannels(self):
        del self._numRxChannels

    #-------------------------------#
    #---------- functions ----------#
    #-------------------------------#

    #-------------------------------#
    # reconstruction function

    def reconDAS(self, sigMat):
        """
        Delay and sum beamformer for reflection ultrasound computed tomography imaging.

        :param sigMat: 3D array (samples x Rx channels x Tx events) of signals

        :return: 2D image array of beamformed signals
        """
        logging.info('  Function    "reconDAS"          : %s', __name__)

        from pyruct import sigMatFilter, calculateDelay, sigMatNormalizeUS

        pixelNumber         = self.pixelNumber
        xSensor             = self.xSensor
        ySensor             = self.ySensor
        fSampling           = self.fSampling

        self.numTxEvents    = np.shape(sigMat)[2]
        self.numTxChannels  = 1
        self.numRxChannels  = np.shape(sigMat)[1]

        # filter sigMat
        sigMatF         = (-1)*sigMatFilter(sigMat, self.lowCutOff, self.highCutOff, fSampling, self.fOrder, 0.5)

        # normalize mean of sigMat around 0
        sigMatN         = sigMatNormalizeUS(sigMatF)

        #++++++++++++++++++++++++++++++++#
        # beginning of reconstruction

        print('***** reconstruction *****')
        startTime       = time.time()

        # hilbert transforms
        analyticalSigMat    = hilbert(sigMatN)
        realSigMat          = analyticalSigMat.real
        imagSigMat          = analyticalSigMat.imag

        # reconstructed image
        imageRecon = np.zeros((pixelNumber, pixelNumber))

        # length of one pixel
        Dxy = self.fieldOfView/(pixelNumber-1)
        
        # define imaging grid
        x = np.linspace(((-1)*(pixelNumber/2-0.5)*Dxy),((pixelNumber/2-0.5)*Dxy),pixelNumber)
        y = np.linspace(((-1)*(pixelNumber/2-0.5)*Dxy),((pixelNumber/2-0.5)*Dxy),pixelNumber)
        meshX, meshY = np.meshgrid(x,y)

        # calculate reception delay in samples
        receptionDelayInSamples = calculateDelay(fSampling, self.delayInSamples)

        # loop trhorugh Tx events
        for eventTxId in range(0, self.numTxEvents):
        # for eventTxId in range(0, 100):

            traChannels         = np.array(np.where(self.traActiveChannels[:,eventTxId] == 1)).ravel()
            receptionChannels   = self.activeChannels[:,eventTxId]

            # loop through all Tx elements in one Tx event
            distTx = 300000000000000000
            for channelTxId in traChannels:

                channelTxId     = int(channelTxId)

                # calculate distance
                distTxX         = meshX - xSensor[channelTxId]
                distTxY         = meshY - ySensor[channelTxId]
                distTx          = np.sqrt(distTxX**2 + distTxY**2)

                # calculate time of flight to Tx element
                tofTxInSamples  = (distTx * fSampling)/self.speedOfSound + self.traDelays[eventTxId, channelTxId]*self.fSampling

            realSignal  = np.zeros((pixelNumber, pixelNumber))
            imagSignal  = np.zeros((pixelNumber, pixelNumber))  

            # loop through all Rx elements in one Tx event
            for channelRxId in receptionChannels:

                channelRxId     = int(channelRxId)
                
                # # distance of detector to image grid
                distRxX         = meshX - xSensor[channelRxId]
                distRxY         = meshY - ySensor[channelRxId]
                distRx          = np.sqrt(distRxX**2 + distRxY**2)

                # calculate time of flight to Rx element
                tofRxInSamples  = (distRx * fSampling)/self.speedOfSound

                timeSample      = tofTxInSamples + tofRxInSamples - receptionDelayInSamples
                timeSampleLow   = np.floor(timeSample)
                timeSampleLow   = timeSampleLow.astype(int)

                # apply number of samples bounds
                timeSampleLow[timeSampleLow<=0]                 = 0
                timeSampleLow[timeSampleLow>=self.nSamples-4]   = self.nSamples-4

                # take real and imaginary signal & make interpolation
                realSignal  += realSigMat[timeSampleLow, channelRxId, eventTxId] + (timeSample-timeSampleLow)*(realSigMat[timeSampleLow+1, channelRxId, eventTxId] - realSigMat[timeSampleLow, channelRxId, eventTxId])
                imagSignal  += imagSigMat[timeSampleLow, channelRxId, eventTxId] + (timeSample-timeSampleLow)*(imagSigMat[timeSampleLow+1, channelRxId, eventTxId] - imagSigMat[timeSampleLow, channelRxId, eventTxId])

            imageRecon  += (realSignal**2 + imagSignal**2)

        endTime = time.time()
        print('time elapsed: %.2f' %(endTime-startTime))
        
        # end of reconstruction
        #++++++++++++++++++++++++++++++++#
        
        return imageRecon