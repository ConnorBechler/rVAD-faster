from __future__ import division
import pickle
import numpy 
from scipy.signal import lfilter
from copy import deepcopy
import time
import sys

import speechproc as speechproc
# Refs:
#  [1] Z.-H. Tan, A.k. Sarkara and N. Dehak, "rVAD: an unsupervised segment-based robust voice activity detection method," Computer Speech and Language, 2019. 
#  [2] Z.-H. Tan and B. Lindberg, "Low-complexity variable frame rate analysis for speech recognition and voice activity detection." 
#  IEEE Journal of Selected Topics in Signal Processing, vol. 4, no. 5, pp. 798-807, 2010.

# 2017-12-02, Achintya Kumar Sarkar and Zheng-Hua Tan

# Usage: python rVAD_fast_2.0.py inWaveFile  outputVadLabel


winlen, ovrlen, pre_coef, nfilter, nftt = 0.025, 0.01, 0.97, 20, 512
opts=1

def rVAD_fast(finwav, fvad, ftThres=0.5, vadThres=0.4):
    if isinstance(finwav, str):
        fs, data = speechproc.speech_wave(finwav)
    ft, flen, fsh10, nfr10 =speechproc.sflux(data, fs, winlen, ovrlen, nftt)


    # --spectral flatness --
    total_time = time.perf_counter()
    pv01=numpy.zeros(nfr10)
    pv01[numpy.less_equal(ft, ftThres)]=1 
    pitch=deepcopy(ft)
    start = time.perf_counter()
    pvblk=speechproc.pitchblockdetect(pv01, pitch, nfr10, opts)
    print(time.perf_counter() - start)

    # --filtering--
    ENERGYFLOOR = numpy.exp(-50)
    b=numpy.array([0.9770,   -0.9770])
    a=numpy.array([1.0000,   -0.9540])
    start = time.perf_counter()
    fdata=lfilter(b, a, data, axis=0)
    print(time.perf_counter() - start)


    #--pass 1--
    start = time.perf_counter()
    noise_samp, noise_seg, n_noise_samp=speechproc.snre_highenergy(fdata, nfr10, flen, fsh10, ENERGYFLOOR, pv01, pvblk)
    print(time.perf_counter() - start)

    #sets noisy segments to zero
    start = time.perf_counter()
    for j in range(n_noise_samp):
        fdata[range(int(noise_samp[j,0]),  int(noise_samp[j,1]) +1)] = 0 
    print(time.perf_counter() - start)

    start = time.perf_counter()

    vad_seg=speechproc.snre_vad(fdata,  nfr10, flen, fsh10, ENERGYFLOOR, pv01, pvblk, vadThres)
    print(len(vad_seg), vad_seg)
    print(time.perf_counter() - start)
    print(time.perf_counter()-total_time)
    numpy.savetxt(fvad, vad_seg.astype(int),  fmt='%i')

if __name__ == '__main__':
    finwav=str(sys.argv[1])
    fvad=str(sys.argv[2])
    rVAD_fast(finwav, fvad)