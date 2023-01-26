import wave
import numpy as np
import scipy.io.wavfile as wav

from rVAD_fast import rVAD_fast
from src.utils.utils import resample

def get_mask(rvad, wav_dir, ):
    frame_rate, audio = wav.read(wav_dir)
    wav_mask = np.zeros_like(audio, dtype = bool)
    
    with open(rvad, 'r') as f:
        masks = f.readlines()

    prev = 0

    def ms_to_ind(ms):
        return round(frame_rate/1000*ms)

    for ix, m in enumerate(masks):
        m = int(m)
        start_ind = ms_to_ind(ix*10)
        end_ind = ms_to_ind(ix*10 + 25)
        if m == 1:
            wav_mask[start_ind: end_ind] = True
    return wav_mask

def get_rvad_mask(dir, sampling_rate = 44100):
    rvad_file = f'{dir}/rvad_{sampling_rate}'
    audio_dir = f'{dir}/audio_{sampling_rate}.wav'
    try:
        return get_mask(rvad_file, audio_dir)
    except:
        rVAD_fast(audio_dir, rvad_file)
        return get_mask(rvad_file, audio_dir)

def float32_wav(sig:np.ndarray):
    if 'float' in str(sig.dtype):
        return sig.astype('float32')
    if sig.dtype == 'int16':
        nb = 16 # -> 16-bit wav files
    elif sig.dtype == 'int32':
        nb = 32 # -> 32-bit wav files
    max_nb = float(2 ** (nb - 1))
    sig = sig / (max_nb + 1.0)
    return sig.astype('float32')

def read_wave(dir, sampling_rate):
    try:
        rate, wv = wav.read(f'{dir}/audio_{sampling_rate}.wav')
        return float32_wav(wv)
        
    except:
        rate, wv = wav.read(f'{dir}/audio.wav')
        wv = resample(wv, round(len(wv)*sampling_rate/44100)) if rate != sampling_rate else wv
        wav.write(f'{dir}/audio_{sampling_rate}.wav', sampling_rate, wv.astype('float32'))
        return float32_wav(wv)

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    mask = get_rvad_mask('data/g_combined')
    plt.imshow(mask.reshape(1,-1))
    plt.show()
    # from scipy.io.wavfile import write
    # res = get_mask('output', '2022_01_30_14_06_47/audio.wav')
    # print(np.sum(res))
    
    # with wave.open('2022_01_30_14_06_47\\audio.wav', 'rb') as f:
    #     frame_rate = f.getframerate()
    #     print(f.getnframes())
    #     audio = f.readframes(f.getnframes())
    #     audio = np.frombuffer(audio, dtype = 'int16')[res]
    #     from matplotlib import pyplot
    #     pyplot.plot(audio)
    #     pyplot.show()
    # write('test.wav', 44100, audio)
    