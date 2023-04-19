#-----
# Description   : Data reader for RUCT
# Date          : October 2021
# Author        : Berkan Lafci
# E-mail        : lafciberkan@gmail.com
#-----

# import Python libraries
import os
import h5py
import time
import logging
import numpy as np

class usReader():
    """
    Ultrasound data reader for RUCT system

    :param folderPath:      Path to data folder
    :param scanName:        Name of data file inside the folder

    :return:                usReader object
    """
    
    # initialize the class
    def __init__(self, folderPath=None, scanName=None, averaging=False, averagingAxis=2):
        logging.info('  Class       "usReader"          : %s', __name__)
        
        self._folderPath    = folderPath
        self._scanName      = scanName
        self._averaging     = averaging
        self._averagingAxis = averagingAxis
 
        # print info about process
        print('***** reading data *****')
        startTime        = time.time()
            
        if self.folderPath==None or scanName==None:
            print('WARNING: Data path is not valid creating random data for test')
            self.sigMat             = np.random.uniform(low=-1, high=1, size=(2032,512,1))
        else:           
            # read data using h5py
            signalFile       = h5py.File(os.path.join(self.folderPath, (self.scanName+'.mat')), 'r')
            
            # check availability of sigMat
            if not any(keyCheck== 'sigMat' for keyCheck in signalFile.keys()):
                raise AssertionError('No sigMat variable key found in data!')

            # read acquisitionInfo and sigMat
            for keyValue in signalFile.keys():
                if keyValue == 'sigMat':
                    self.sigMat             = np.transpose(signalFile['sigMat'])

            # WARNING: If mat file is not saved with -v7.3 use this method
            # signalFile              = sio.loadmat(filePath)
            # self.acquisitionInfo    = signalFile['acquisitionInfo']
            # self.sigMat             = signalFile['sigMat']

        # expand dimensions
        if np.ndim(self.sigMat) == 2:
            self.sigMat = np.expand_dims(self.sigMat, axis=2)
        else:
            self.sigMat = self.sigMat
        
        endTime = time.time()
        print('time elapsed: %.2f' %(endTime-startTime))

    #--------------------------------#
    #---------- properties ----------#
    #--------------------------------#

    #--------------------------------#
    # Path to folder

    @property
    def folderPath(self):
        return self._folderPath

    @folderPath.setter
    def folderPath(self, value):
        self._folderPath = value

    @folderPath.deleter
    def folderPath(self):
        del self._folderPath
    
    #--------------------------------#
    # Scan name inside the folder

    @property
    def scanName(self):
        return self._scanName

    @scanName.setter
    def scanName(self, value):
        self._scanName = value

    @scanName.deleter
    def scanName(self):
        del self._scanName
