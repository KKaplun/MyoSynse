# -*- coding: utf-8 -*-
"""
Created on Fri Jun 29 13:15:06 2018

@author: Александр
"""

import time, tqdm
from pylsl import StreamInfo, StreamOutlet
import numpy as np 
import h5py

N1=0
N2=-1
numCh=64

with h5py.File('experiment_data.h5','r+') as f1:
    raw_data = f1['protocol1']['raw_data']
    myoData=np.array(raw_data[N1:N2,:numCh])
    pnData=np.array(raw_data[N1:N2,numCh:])


info = StreamInfo('SimEMG', 'EMG', numCh, 50, 'float32', 'myuid34234')
outletMyo = StreamOutlet(info)

info = StreamInfo('SimPn', 'PN', pnData.shape[1], 50, 'float32', 'myuid88005553535')
outletPn = StreamOutlet(info)


pos=0
chunksize=10

print("now sending data...")

dt_rate=0.02
exptime = myoData.shape[0]/(chunksize/dt_rate)

pbar = tqdm.tqdm(total=exptime)
p=time.time()
t=0

startTime = time.time()

while (time.time() - startTime < exptime):
    # make a new random 8-channel sample; this is converted into a
    # pylsl.vectorf (the data type that is expected by push_sample)
    startwhile = time.time();
    
    t+=startwhile-p
    if(t>1):
        pbar.update(round(t))
        t=0
    
    p=startwhile
    
    chunk = myoData[pos:pos+chunksize,:].tolist()
    outletMyo.push_chunk(chunk)
    
    chunk = pnData[pos:pos+chunksize,:].tolist()
    outletPn.push_chunk(chunk)
    
    pos=pos+chunksize
    
    dif = dt_rate - time.time() + startwhile;
    if(dif > 0):
        time.sleep(dif)
pbar.close()
del(myoData)
del(pnData)