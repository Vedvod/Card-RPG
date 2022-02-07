#-------------------------modules-------------------------
import os, random, time, sys, math, winsound, numpy as np, matplotlib.pyplot as plt; from scipy.io.wavfile import write; from scipy import signal

#-----------------------function(s)-----------------------
t=np.linspace(0, 1, 44000)
list_frac=lambda list_, fraction: list(list_)*math.floor(fraction) + list(list_)[:round((len(list_))*(fraction%1))]
make_44k_array = lambda duration, frequency: list_frac(signal.sawtooth(2*np.pi*t*frequency, 0.8), duration)
m4a = make_44k_array
import matplotlib.pyplot as plt; plt.plot(m4a(1, 10), data="2 beat A5"); plt.plot(m4a(0.5, 10), data="1 beat A5"); plt.show()

#-------------------------classes-------------------------
class Timer:
    def __init__(self):
        self.start_time=time.time()
    def time(self):
        return time.time()-self.start_time
    def reset(self):
        self.start_time=time.time()

#--------------------------setup--------------------------
o=0.8; G, A, B, C, D, r= 392*o, 440*o, 493.88*o, 523.25*o, 587.33*o, 0
l=[B, A, G, A, B, B, "aB", A, A, "aA", B, D, "aD", B, A, G, A, B, B, B, B, A, A, B, A, "aG"]
sound_array=[]

#------------------------main line------------------------
comp_timer = Timer()
for n, a in enumerate(l, 1):
    dur=0.35
    if str(a)[0] == "a":
        dur*=2 
    a=int(eval(str(a).strip("a")))
    sound_array+=(w:=(m4a(dur, a)))+[0 for i in range(int(dur/4*44000))]
    print(f"Note {n} of {len(l)} translated!")
    print(f"It has been {comp_timer.time()} seconds since composition began!")
    #plt.plot(w); plt.show()

data = np.array(sound_array)
scaled = np.int16(data/np.max(np.abs(data)) * 32767)
write('''saw's lamb.wav''', 44000, scaled)
input("Press Enter to exit the script...")
