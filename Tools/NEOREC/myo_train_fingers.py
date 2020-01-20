# -*- coding: utf-8 -*-
"""
Created on Tue Jun 26 21:15:26 2018

@author: Александр
"""

import scipy.io
import numpy as np
import h5py
import PNinterpolate
from EMGfilter import envelopeFilter
import tqdm
from matplotlib import pyplot as plt

class EMGDecoder:
    def __init__(self):
        self.emgFilter=envelopeFilter()
        
    def loadParams(self, path=''):
        self.Tail = 0
        self.emg_buffer = 0
        self.WienerCoordsBuffer = 0
        self.KalmanCoordsBuffer = 0
        self.emg_buffer_size = 500
        if path:
            filterParams = scipy.io.loadmat(path)
        else:
            filterParams = scipy.io.loadmat('filterParams.mat')
        self.lag = int(filterParams['lag'])
        self.forward = int(filterParams['forward'])
        self.downsample = int(filterParams['downsample'])
        self.A = filterParams['A']
        self.W = filterParams['W']
        self.Ex = filterParams['Ex']
        self.Ez = filterParams['Ez']
        
        self.P_after = np.copy(self.Ex)
        self.P_before = np.empty((self.Ez.shape[0], self.Ez.shape[0]))
        self.Kalman_estimate = np.empty((self.W.shape[0],1))
        self.Wiener_Estimate = np.empty((self.W.shape[0],1))
        
    def fit(self, X=None,Y=None,file='experiment_data.h5',numCh=64,offCh=64,Pn=[29,59,77,101,125],lag=2,forward=0,downsample=0):
        self.numCh=numCh
        self.offCh=offCh
        self.Pn=Pn
        self.lag=lag
        self.forward=forward
        self.downsample=downsample
        
        if type(X)==type(None) or type(Y)==type(None):
           #try and read file then
           with h5py.File(file,'r+') as f1:
               raw_data = np.array(f1['protocol1']['raw_data'])
               Y=raw_data[:,[p+self.offCh for p in Pn]]
               X=raw_data[:,:self.numCh]
               del raw_data
        #get the envelope of EMG data and interpolate PN to EMG samplerate
        X=self.emgFilter.filterEMG(X)
        Y=PNinterpolate.interpolatePN(Y)
        
        def offset(data,lag,leftOffset,rightOffset=0):
            return data[leftOffset+lag:data.shape[0]-rightOffset]

        emg_lag=np.empty((X.shape[0]-2-self.lag-self.forward,numCh*(self.lag+1)));
        for l in range(self.lag+1):
            emg_lag[:,l*numCh:(l+1)*numCh]=X[(2+l):(X.shape[0]-self.lag-self.forward+l),:]
        
        Coord=np.copy(Y)

        Vel=np.apply_along_axis(np.diff,0,Coord)
        
        Acc=np.apply_along_axis(np.diff,0,Vel)
            
           

        Coords=np.hstack((np.apply_along_axis(offset,0,Coord,self.lag,2),np.apply_along_axis(offset,0,Vel,self.lag,1),np.apply_along_axis(offset,0,Acc,self.lag,0)))
        print(Coords.shape)
        
        EMG_signals=np.hstack((np.ones((emg_lag.shape[0],1)),emg_lag));
        self.W = np.linalg.pinv(EMG_signals) 
        self.W = self.W @ Coords

        Measurement_Error=Coords-EMG_signals @ self.W;
        Measurement_Error_Covar=np.cov(Measurement_Error.T);
        self.W = self.W.T;
        
        Now=np.hstack((np.apply_along_axis(offset,0,Coord,self.lag,3),np.apply_along_axis(offset,0,Vel,self.lag,2),np.apply_along_axis(offset,0,Acc,self.lag,1)))
        
        Lag=np.hstack((np.apply_along_axis(offset,0,Coord,self.lag,2,1),np.apply_along_axis(offset,0,Vel,self.lag,1,1),np.apply_along_axis(offset,0,Acc,self.lag,0,1)))
        
        self.A=np.linalg.pinv(Lag) @ Now
        
        State_Trans_Error=Now-Lag @ self.A
        State_Trans_Covar=np.cov(State_Trans_Error.T)
        
        self.A=self.A.T
        
        self.Ex = State_Trans_Covar; # process noise
        self.Ez = Measurement_Error_Covar;  # measurement noise
        
        self.P_after = np.copy(self.Ex)
        self.P_before = np.empty((self.Ez.shape[0], self.Ez.shape[0]))
        self.Kalman_estimate = np.empty((self.W.shape[0],1))
        self.Wiener_Estimate = np.empty((self.W.shape[0],1))
        
        scipy.io.savemat('filterParams.mat', mdict={'W': self.W, 'A':self.A, 'Ex': self.Ex, 'Ez':self.Ez})

    def evaluate(self,X=None,Y=None,file='experiment_data.h5', numCh=None,offCh=None,Pn=None,lag=None,forward=None,downsample=None):
        
        numCh = self.numCh if type(numCh)==type(None) else numCh
        offCh = self.offCh if type(offCh)==type(None) else offCh
        Pn = self.Pn if type(Pn)==type(None) else Pn
        lag = self.lag if type(lag)==type(None) else lag
        forward = self.forward if type(forward)==type(None) else forward
        downsample = self.downsample if type(downsample)==type(None) else downsample
        
        if type(X)==type(None) or type(Y)==type(None):
           #try and read file then
           with h5py.File(file,'r+') as f1:
               raw_data = np.array(f1['protocol1']['raw_data'])
               Y=raw_data[:,[p+offCh for p in Pn]]
               X=raw_data[:,:numCh]
               del raw_data
        #get the envelope of EMG data and interpolate PN to EMG samplerate
        X=self.emgFilter.filterEMG(X)
        Y=PNinterpolate.interpolatePN(Y)
    
        emg_lag=np.empty((X.shape[0]-2-lag-forward,numCh*(lag+1)));
        for l in range(lag+1):
            emg_lag[:,l*numCh:(l+1)*numCh]=X[(2+l):(X.shape[0]-lag-forward+l),:]
        
        
        Coord=np.copy(Y)
            
        EMG_signals=np.hstack((np.ones((emg_lag.shape[0],1)),emg_lag))    
        
        WienerCoords=np.empty((EMG_signals.shape[0],self.Ex.shape[1]))
        KalmanCoords=np.empty((EMG_signals.shape[0],self.Ex.shape[1]))
        
        for t in tqdm.tqdm(range(EMG_signals.shape[0])):
            #Predict coordinate by state measurement equation
            X_measurement_estimate=self.W @ EMG_signals[t,:][:,None];
            #Store Wiener Estimate
            WienerCoords[t,:]=X_measurement_estimate.T;
            
            #Kalman
            X_state_estimate = self.A @ self.Kalman_estimate
            self.P_before = self.A @ self.P_after @ self.A.T + self.Ex
            self.P_after=np.linalg.pinv(np.linalg.pinv(self.P_before)+np.linalg.pinv(self.Ez))
            self.Kalman_estimate=self.P_after @ (np.linalg.pinv(self.P_before) @ X_state_estimate+np.linalg.pinv(self.Ez) @ X_measurement_estimate)
                
            KalmanCoords[t,:] = self.Kalman_estimate.T
        
        Kc=KalmanCoords[:,:Coord.shape[1]]
        Tc=Coord[lag+2:,:]
        
        kalmanStabilizationOffset=round(Tc.shape[0]*0.05)
        
        plt.figure()
        for i in range(Kc.shape[1]):
            plt.subplot(Kc.shape[1]*100+11+i)
            plt.plot(Kc[kalmanStabilizationOffset:,i])
            plt.plot(Tc[kalmanStabilizationOffset:,i])
        
        
        for i in range(Kc.shape[1]):
            print(np.corrcoef(Kc[2000:,i].T,Tc[2000:,i].T)[0,1])
    
    def fitEvaluate(self,X=None,Y=None,file='experiment_data.h5',testRatio=1/2,numCh=64,offCh=64,Pn=[29,59,77,101,125],lag=2,forward=0,downsample=0):
        self.numCh=numCh
        self.offCh=offCh
        self.Pn=Pn
        self.lag=lag
        self.forward=forward
        self.downsample=downsample
        
        if type(X)==type(None) or type(Y)==type(None):
           with h5py.File(file,'r+') as f1:
               raw_data = np.array(f1['protocol1']['raw_data'])
               Y=raw_data[:,[p+offCh for p in Pn]]
               X=raw_data[:,:numCh]
               del raw_data
        split=round(X.shape[0]*(1-testRatio))
        self.fit(X[:split,:],Y[:split,:])
        self.evaluate(X[split:,:],Y[split:,:])
    
    def transform(self,EMGchunk):
        
        chunkSize=EMGchunk.shape[0]
        numCh=EMGchunk.shape[1]
        forward=self.forward
        lag=self.lag
        
        if(np.isscalar(self.Tail)):
            
            self.emg_buffer=np.empty((self.emg_buffer_size,1+numCh*(self.lag+1)))
            self.emg_buffer[:,0]=1
            
            self.WienerCoordsBuffer=np.empty((self.emg_buffer_size,self.W.shape[0]))
            self.KalmanCoordsBuffer=np.empty((self.emg_buffer_size,self.W.shape[0]))
            
            self.Tail=np.zeros((lag+1,numCh*(lag+1)))
            
            emg_lag=self.emg_buffer[:chunkSize-lag-forward,1:]
            
            for l in range(lag+1):
                emg_lag[:,l*numCh:(l+1)*numCh]=EMGchunk[(l):(chunkSize-lag-forward+l),:]
                self.Tail[:lag-l,l*numCh:(l+1)*numCh]=EMGchunk[chunkSize-lag+l:chunkSize,:]
            emg_lag=self.emg_buffer[:chunkSize-lag-forward,:]
        else:
            emg_lag=self.emg_buffer[:chunkSize-forward,1:]
            for l in range(lag+1):
                emg_lag[lag-l:chunkSize,l*numCh:(l+1)*numCh]=EMGchunk[0:(chunkSize-lag-forward+l),:]
                emg_lag[0:lag-l,l*numCh:(l+1)*numCh]=self.Tail[:lag-l,l*numCh:(l+1)*numCh]
                self.Tail[:lag-l,l*numCh:(l+1)*numCh]=EMGchunk[chunkSize-lag+l:chunkSize,:]
            emg_lag=self.emg_buffer[:chunkSize-forward,:]
        
        WienerCoords=self.WienerCoordsBuffer[:emg_lag.shape[0],:]
        KalmanCoords=self.KalmanCoordsBuffer[:emg_lag.shape[0],:]
           
        for t in range(emg_lag.shape[0]):
            #Predict coordinate by state measurement equation
            X_measurement_estimate=self.W @ emg_lag[t,:][:,None];
            #Store Wiener Estimate
            WienerCoords[t,:]=X_measurement_estimate.T;
            
            #Kalman
            X_state_estimate = self.A @ self.Kalman_estimate
            P_before = self.A @ self.P_after @ self.A.T + self.Ex
            self.P_after=np.linalg.pinv(np.linalg.pinv(P_before)+np.linalg.pinv(self.Ez))
            self.Kalman_estimate=self.P_after @ (np.linalg.pinv(P_before) @ X_state_estimate+np.linalg.pinv(self.Ez) @ X_measurement_estimate)
                
            KalmanCoords[t,:] = self.Kalman_estimate.T
            
        return WienerCoords, KalmanCoords
        
    
a=EMGDecoder()
a.fitEvaluate(lag=2)
