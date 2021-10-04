import numpy as np
from scipy.io import wavfile
def freq_band(elements,duration,low = 100,high = 1500):
    fband = np.linspace(low,high,elements)


    SAMPLE_RATE = 44100
    AMPLITUDE = 4096

    t = np.linspace(0,duration,int(SAMPLE_RATE*duration))
    waves = [AMPLITUDE*np.sin(2*np.pi*freq*t) for freq in fband]

    for i,freq in enumerate(fband):
        wavfile.write(f'tones/{freq}.wav',rate=SAMPLE_RATE,data=waves[i].astype(np.int16))



freq_band(200,0.01)
