# This script uses nmupy fft(fast fourier transform for simple gaussian in comparision with the discrete fourier tranfrom in another script)
#Taking the simple function e^(-x**2)
import numpy as np
import matplotlib.pyplot as plt

def generate(N):
    """input: N(steps)"""    
    
    t=np.linspace(-50,50,N) # time sample
    x=np.exp(-t**2)
    
    #FFT
    X = np.fft.fft(x)
    X = np.fft.fftshift(X)  #shift zero freq to center

    #Compute frequency axis
    freq = np.fft.fftfreq(N, d=(t[1]-t[0]))
    freq = np.fft.fftshift(freq)  # align with shifted FFT
    
    # plt.subplot(1,2,1)
    plt.plot(t, x)
    plt.grid()
    # plt.title("Time domain")

    # plt.subplot(1,2,2)
    plt.plot(freq, np.abs(X))
    # plt.title("Frequency domain")
    
    plt.show()

generate(1000)
