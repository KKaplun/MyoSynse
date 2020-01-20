# -*- coding: utf-8 -*-
"""
Created on Fri Jun 22 00:08:05 2018

@author: Александр
"""
from scipy.signal import butter, lfilter
import numpy as np

class envelopeFilter():
    def __init__(self, **kwargs):
        self.bband,self.aband=self.butter_bandpass(lowcut=20, highcut=200, fs=500, order=5)
        self.blow, self.alow=self.butter_lowpass(cutoff=2, fs=500, order=5)
        self.filtorder=5
        self.Zband=0
        self.Zlow=0
        
    def changeParams(self, lowcut=20, highcut=200, cutoff=2, fs=500, order=5):
        self.bband,self.aband=self.butter_bandpass(lowcut=20, highcut=200, fs=500, order=5)
        self.blow, self.alow=self.butter_lowpass(cutoff=2, fs=500, order=5)
        
    def butter_bandpass(self,lowcut, highcut, fs, order=5):
        nyq = 0.5 * fs
        low = lowcut / nyq
        high = highcut / nyq
        b, a = butter(order, [low, high], btype='band')
        return b, a
    
    def butter_lowpass(self,cutoff, fs, order=5):
        nyq = 0.5 * fs
        normal_cutoff = cutoff / nyq
        b, a = butter(order, normal_cutoff, btype='low')
        return b, a
    
    def filterEMG(self,MyoChunk): 
        
        #fitting filter delay sizes in case we're working with chunks
        if(np.isscalar(self.Zband)):
            self.Zband=np.zeros((2*self.filtorder,MyoChunk.shape[1]))
            self.Zlow=np.zeros((self.filtorder,MyoChunk.shape[1]))
        
        #smooting out noise frequiencies
        for j in range(MyoChunk.shape[1]):
            MyoChunk[:,j],self.Zband[:,j] = lfilter(self.bband,self.aband, MyoChunk[:,j],-1,self.Zband[:,j])
        
        #rectifying
        np.abs(MyoChunk, out=MyoChunk)
        
        #filtering high frequencies
        for j in range(MyoChunk.shape[1]):
            MyoChunk[:,j],self.Zlow[:,j] = lfilter(self.blow,self.alow, MyoChunk[:,j],-1,self.Zlow[:,j])
    
        return MyoChunk