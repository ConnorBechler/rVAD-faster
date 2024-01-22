import librosa
import soundfile
from rVAD_fast import rVAD_fast as vad
import sys

if __name__ == '__main__':
    finwav=str(sys.argv[1])
    fvad=str(sys.argv[2])

    lib_aud, sr = librosa.load(finwav)
    aud_mono = librosa.to_mono(lib_aud)
    print(librosa.get_duration(filename=finwav))
    n_finwav = finwav.split('/')[-1].split('.')[0]+'_working_mono.wav'
    soundfile.write(n_finwav, aud_mono, sr)

    vad(n_finwav, fvad)

