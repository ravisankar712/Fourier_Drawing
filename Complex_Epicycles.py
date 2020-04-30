import numpy as np
from scipy.integrate import simps
from p5 import *

#this is used only because the p5 draw recogonizes only OOP
class Clock():

    def __init__(self, t0):
        self.initial_time = t0
        self.time = t0
    def tick(self, dt):
        self.time -= dt
    def reset(self):
        if self.time < self.initial_time - 2*np.pi:
            self.time = self.initial_time
            return True
        else: return False


#gives fourier terms corresponding to -N, ... ,N (2N + 1 terms)
def complex_FT(signal, xs, N):

    out = []
    P = xs[-1] - xs[0]

    for n in range(-N, N+1, 1):
        I = (signal) * np.exp(xs * (- 2*np.pi*n/P) * 1j)
        cN = simps(I, xs) * (1/P)
        out.append(cN)

    return out

#gets the amplitude, frequency and phase of a given 2N+1 fourier coefficients
def AFP(F_signal, xs):

    out = []
    P = xs[-1] - xs[0]
    N = len(F_signal)

    for i in range(N):
        ci = F_signal[i]
        amp = abs(ci)
        freq = 2*np.pi*(i - (N-1)/2)/P
        phase = np.arctan2(ci.imag, ci.real)
        out.append([amp, freq, phase])
    return out


def sketch_epicycles(terms):
    
    #translate(x_pos, y_pos)
    x = 0.0
    y = 0.0
    no_fill()
    

    for k in range(len(terms) - 1):
        r, freq, phi = terms[k]
        stroke_weight(3)
        stroke(0, 200, 255, 50)
        circle((x, y), 2*r)
        x_old = x
        y_old = y

        x += r * np.cos(freq * t.time - phi)
        y += r * np.sin(freq * t.time - phi)
        stroke(255, 100)
        stroke_weight(2)
        line((x_old, y_old), (x, y))

    return x, y


t = Clock(0)

#geting the data
data = np.loadtxt('data.txt')
scale = 100
N_terms = 30
xs = np.linspace(-np.pi, np.pi, len(data))
#making the data into a complex signal
signal = np.array([data[i][0] + data[i][1]*1j for i in range(len(data))]) * scale
Fourier_sig = complex_FT(signal, xs, N_terms)
terms = AFP(Fourier_sig, xs)
terms = sorted(terms, key=lambda x:x[0], reverse = True)
path = []

def setup():
    size(1000, 1000)
    

def draw():
    background(20, 20, 20)
    translate(width/2, height/2)

    x, y = sketch_epicycles(terms)
    path.append([x, y])

    c = int(round(abs(t.time/(2*np.pi)) * 255))
    stroke(255-c, c, 0)
    stroke_weight(3)
    for i in range(len(path)-1):
        if i == 0:
            pass
        else:
            line((path[-1-i][0], path[-1-i][1]), (path[-2-i][0], path[-2-i][1]))
            
    dt = 1.0/len(terms) 
    t.tick(dt)
    if t.reset():
        path.clear()

    #incase want to save each frames to make a video
    #save_frame()

run()
        
    


        
        

    
    
