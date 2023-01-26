import wave
import numpy as np
import scipy.io.wavfile as wav

from rVAD_fast import rVAD_fast

def get_mask(rvad, wav_dir):
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