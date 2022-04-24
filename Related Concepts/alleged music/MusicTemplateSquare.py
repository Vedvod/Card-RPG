#-------------------------modules-------------------------
import os, random, time, sys, math, winsound, numpy as np, matplotlib.pyplot as plt; from scipy.io.wavfile import write; from scipy import signal

#-----------------------function(s)-----------------------
make_44k_array = lambda duration, frequency: [(0 if frequency == 0 else (-2*round((frequency*x)%1)+1)) for x in duration*np.linspace(0, 1, int(duration*44000))]
m4a = make_44k_array
#import matplotlib.pyplot as plt; plt.plot(m4a(1, 10), data="2 beat A5"); plt.plot(m4a(0.5, 10), data="1 beat A5"); plt.show()

#-------------------------classes-------------------------
class Timer:
    def __init__(self):
        self.start_time=time.time()
    def time(self):
        return time.time()-self.start_time
    def reset(self):
        self.start_time=time.time()

#--------------------------setup--------------------------
o=1; C, D, E, F, G, A, B, r = 16.35, 18.35, 20.60, 21.83, 24.50, 27.50, 30.87, 0; R=r
base_dur=60/float(input("Beats per minute? "))
octave = lambda x, o=5: float(x)*2**o
l=eval(f'''({input("melody in form (frequency, duration): ").replace("|", "")}, ((r, 69), 0))''')
print(l)
sound_array=[]

#------------------------main line------------------------
comp_timer = Timer()
for n, a in enumerate(l, 1):
    try:
        a, dur = octave(a[0][0], a[0][1]), base_dur*float(a[1])
    except:
        a, dur = octave(a[0]), 1
    a=int(eval(str(a).strip("a")))
    sound_array+=(w:=(m4a(dur, a)+[0 for i in range(int(dur/4*44000))]))
    print(f"Note {n} of {len(l)} translated!")
    print(f"It has been {comp_timer.time()} seconds since composition began!")
    #plt.plot(w); plt.show()

data = np.array(sound_array)
scaled = np.int16(data/np.max(np.abs(data)) * 32767)
write('''Test_Square.wav''', 44000, scaled)

input("Press Enter to exit the script...")
