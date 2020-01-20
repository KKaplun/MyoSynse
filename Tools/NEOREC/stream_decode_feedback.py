# -*- coding: utf-8 -*-
"""
Created on Thu Jun 28 18:13:30 2018

@author: Александр
"""

from pylsl import StreamInlet, resolve_stream, StreamInfo, StreamOutlet, cf_double64
import time
import numpy as np
import socket
import struct
from EMGfilter import envelopeFilter
from EMGdecode import EMGDecoder

# for stream recieve emulation
debug = False

fps = 30
expTime = 1000
tpf = 1/fps

numCh = 64
srate = 500
pos = 0

#PN channels for finger joints
fingersrange = np.array([59, 77, 101, 125])
#avatar channels for finger joints
fsendrange = np.array([14,23,32,41])

avatarBuffer = np.zeros(96)
pnbuff = np.zeros((len(fingersrange)))
emgfilter=envelopeFilter()
emgdecoder=EMGDecoder()

#initializing Avatar server
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('127.0.0.1', 12001)
client_address = ('127.0.0.1', 9001)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)

info = StreamInfo('EMGDdecode', 'EMG', 4, fps, cf_double64, 'myuid34234')
outletEMG = StreamOutlet(info)

#LSL resolving
print("trying to resolve streams")
if debug:
    print('debug')
    streams = resolve_stream('name', 'SimEMG')
    myoInlet = StreamInlet(streams[0])

    streams = resolve_stream('name', 'SimPn')
    pnInlet = StreamInlet(streams[0])
else:
    print('not debug somehow')
    streams = resolve_stream('name', 'NVX136_Data')
    myoInlet = StreamInlet(streams[0])

    streams = resolve_stream('name', 'AxisNeuron')
    pnInlet = StreamInlet(streams[0])


print("stream resolved")

startTime = time.time()

while (time.time() - startTime < expTime):

    start = time.time()

    chunk, timestamp = myoInlet.pull_chunk()
    chunk = np.asarray(chunk)
    chunk_size = chunk.shape[0]

    pnchunk, timestamp = pnInlet.pull_chunk()
    pnchunk = np.asarray(pnchunk)
    pnchunk_size = pnchunk.shape[0]

    if pnchunk_size > 0:
        pnchunk = pnchunk[:, fingersrange]
        for i in range(pnchunk.shape[1]):
            t = pnchunk[:, i]
            nans = np.isnan(t)
            if sum(~nans) == 0:
                t = pnbuff[i]
            else:
                t = np.median(t[~nans])
            pnbuff[i] = t
    else:
        print('empty pn chunk encountered')

    if chunk_size > 0:

        chunk = chunk[:, :numCh]
        chunk = emgfilter.filterEMG(chunk)
        WienerCoords, KalmanCoords = emgdecoder.decodeEMG(chunk)
        
        #getting the last samples
        prediction = KalmanCoords[-1,:len(fingersrange)]
        fact = np.copy(pnbuff)
        
        print(prediction.reshape(1,-1))
        outletEMG.push_chunk(prediction.reshape(1,-1))
        
        
        avatarBuffer[fsendrange] = prediction
        avatarBuffer[fsendrange+3] = prediction
        avatarBuffer[fsendrange+6] = prediction/2

        avatarBuffer[fsendrange+48] = fact
        avatarBuffer[fsendrange+3+48] = fact
        avatarBuffer[fsendrange+6+48] = fact/2
        
        #sending to the Avatar
        data2 = struct.pack('%df' % len(avatarBuffer), *list(map(float, avatarBuffer)))
        sock.sendto(data2, client_address)
        
    else:
        print('empty chunk encountered')

    dif = tpf - time.time() + start
    if dif > 0:
        time.sleep(dif)
    else:
        print("not enough time for chunk processing, latency is ", dif, ' s')
