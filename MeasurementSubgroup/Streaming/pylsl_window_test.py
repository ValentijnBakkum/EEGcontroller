import msvcrt
import numpy as np
import matplotlib.pyplot as plt

from scipy.fft import rfft, rfftfreq 
from scipy import signal
from scipy.fft import fftshift
from scipy.signal import butter, lfilter, lfilter_zi

from pylsl import StreamInlet, resolve_stream

# Data settings
duration = 10
sampling_frequency = 250

# Window settings
window = 50
overlap = 0.5

# Plot settings
pause = 0.01
time_plot = 50

choosen_electrode = 0 #int(input("Which electrode should be plotted? (0-7)")) # Electrode election
print("Press 'ESC' to stop the plot") # Stop the plot

sample = [
    -8.915, -5.324, -0.852, 2.978, 5.052, 5.074, 3.566, 1.734, 0.733, 0.760,
    1.122, 1.136, 0.690, 0.025, -0.698, -1.357, -1.436, -0.084, 2.893, 6.272,
    8.181, 7.616, 5.108, 2.132, 0.076, -0.380, 0.543, 1.775, 1.968, 0.497,
    -2.008, -4.265, -5.422, -5.325, -3.989, -1.344, 2.308, 5.953, 8.354, 8.854,
    7.630, 5.296, 2.457, -0.438, -3.049, -5.085, -6.241, -6.130, -4.417,
    -1.381, 1.632, 2.858, 1.620, -0.994, -3.123, -3.630, -2.681, -1.464,
    -1.350, -2.726, -4.481, -4.960, -3.535, -1.135, 0.682, 1.045, 0.289,
    -0.629, -1.034, -0.869, -0.433, -0.080, -0.106, -0.713, -1.766, -2.613,
    -2.515, -1.242, 0.859, 2.981, 4.065, 3.376, 0.992, -2.270, -5.136, -6.235,
    -4.829, -1.382, 2.745, 5.966, 6.902, 4.958, 1.039, -2.707, -4.530, -4.507,
    -4.055, -4.379, -5.510, -6.336, -5.472, -2.392, 2.177, 6.775, 9.951,
    10.825, 9.366, 6.239, 2.394, -1.276, -4.174, -6.090, -7.068, -7.244,
    -6.821, -6.036, -5.058, -3.853, -2.295, -0.532, 0.951, 1.726, 1.672,
    0.934, -0.040, -0.455, 0.426, 2.626, 5.304, 7.223, 7.501, 6.133, 3.881,
    1.676, 0.092, -0.845, -1.533, -2.304, -2.997, -3.064, -2.041, -0.045,
    2.107, 3.496, 3.839, 3.533, 3.155, 3.103, 3.464,    -8.915, -5.324, -0.852, 2.978, 5.052, 5.074, 3.566, 1.734, 0.733, 0.760,
    1.122, 1.136, 0.690, 0.025, -0.698, -1.357, -1.436, -0.084, 2.893, 6.272,
    8.181, 7.616, 5.108, 2.132, 0.076, -0.380, 0.543, 1.775, 1.968, 0.497,
    -2.008, -4.265, -5.422, -5.325, -3.989, -1.344, 2.308, 5.953, 8.354, 8.854,
    7.630, 5.296, 2.457, -0.438, -3.049, -5.085, -6.241, -6.130, -4.417,
    -1.381, 1.632, 2.858, 1.620, -0.994, -3.123, -3.630, -2.681, -1.464,
    -1.350, -2.726, -4.481, -4.960, -3.535, -1.135, 0.682, 1.045, 0.289,
    -0.629, -1.034, -0.869, -0.433, -0.080, -0.106, -0.713, -1.766, -2.613,
    -2.515, -1.242, 0.859, 2.981, 4.065, 3.376, 0.992, -2.270, -5.136, -6.235,
    -4.829, -1.382, 2.745, 5.966, 6.902, 4.958, 1.039, -2.707, -4.530, -4.507,
    -4.055, -4.379, -5.510, -6.336, -5.472, -2.392, 2.177, 6.775, 9.951,
    10.825, 9.366, 6.239, 2.394, -1.276, -4.174, -6.090, -7.068, -7.244,
    -6.821, -6.036, -5.058, -3.853, -2.295, -0.532, 0.951, 1.726, 1.672,
    0.934, -0.040, -0.455, 0.426, 2.626, 5.304, 7.223, 7.501, 6.133, 3.881,
    1.676, 0.092, -0.845, -1.533, -2.304, -2.997, -3.064, -2.041, -0.045,
    2.107, 3.496, 3.839, 3.533, 3.155, 3.103, 3.464,    -8.915, -5.324, -0.852, 2.978, 5.052, 5.074, 3.566, 1.734, 0.733, 0.760,
    1.122, 1.136, 0.690, 0.025, -0.698, -1.357, -1.436, -0.084, 2.893, 6.272,
    8.181, 7.616, 5.108, 2.132, 0.076, -0.380, 0.543, 1.775, 1.968, 0.497,
    -2.008, -4.265, -5.422, -5.325, -3.989, -1.344, 2.308, 5.953, 8.354, 8.854,
    7.630, 5.296, 2.457, -0.438, -3.049, -5.085, -6.241, -6.130, -4.417,
    -1.381, 1.632, 2.858, 1.620, -0.994, -3.123, -3.630, -2.681, -1.464,
    -1.350, -2.726, -4.481, -4.960, -3.535, -1.135, 0.682, 1.045, 0.289,
    -0.629, -1.034, -0.869, -0.433, -0.080, -0.106, -0.713, -1.766, -2.613,
    -2.515, -1.242, 0.859, 2.981, 4.065, 3.376, 0.992, -2.270, -5.136, -6.235,
    -4.829, -1.382, 2.745, 5.966, 6.902, 4.958, 1.039, -2.707, -4.530, -4.507,
    -4.055, -4.379, -5.510, -6.336, -5.472, -2.392, 2.177, 6.775, 9.951,
    10.825, 9.366, 6.239, 2.394, -1.276, -4.174, -6.090, -7.068, -7.244,
    -6.821, -6.036, -5.058, -3.853, -2.295, -0.532, 0.951, 1.726, 1.672,
    0.934, -0.040, -0.455, 0.426, 2.626, 5.304, 7.223, 7.501, 6.133, 3.881,
    1.676, 0.092, -0.845, -1.533, -2.304, -2.997, -3.064, -2.041, -0.045,
    2.107, 3.496, 3.839, 3.533, 3.155, 3.103, 3.464
]

# Parameters
fs = 250  # Sampling frequency (Hz)
t = np.arange(0, 1.8, 1/fs)  # Time array, 1.8 seconds with fs=250 Hz

# Signal frequencies
signal_freq = 10  # Signal frequency (Hz)
noise_freq = 100  # Noise frequency (Hz)

# Generate signal and noise
signal = np.sin(2 * np.pi * signal_freq * t)
noise = 0.5 * np.sin(2 * np.pi * noise_freq * t)

# Combine signal and noise
sample = signal + noise

# initial values
y_win = np.zeros(window)  # window array
t_win = np.zeros(window)  # time array
t = 1
i = 1
aborted = False

#functions
def flatten(xss):
    return [x for xs in xss for x in xs]

def filter(y):
    from scipy.signal import butter, lfilter

    # Define the filter parameters
    lowcut = 2
    highcut = 30
    fs = 250  # Sampling frequency

    # Calculate the filter coefficients
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(4, [low, high], btype='band')

    # Apply the filter to each column of the DataFrame
    y_filtered = lfilter(b, a, np.array(y))
    return y_filtered

# main loop
while not aborted:
    #calculate sample overlap
    overlap_win = int(overlap * window)

    # assign EEG data to array
    y_win[0] = sample[i]
    t_win[0] = t

    # Shift the array with one index
    y_win = np.roll(y_win, -1)
    t_win = np.roll(t_win, -1)

    #print(y_win, "window input")
    #print(t_win)

    # When the overlap is reached but not at i = 0 or i = overlap
    if i % overlap_win == 0 and i != overlap_win and i != 0:
        # apply filter to window
        y_win_filt = filter(y_win)

        # Take the samples that are overlapped
        y_shift = y_win_filt[0:overlap_win+1]
        t_shift = t_win[0:overlap_win+1]

        # Assign the values to an array
        y_shift = np.array(y_shift)
        t_shift = np.array(t_shift)

        # Make the overlapped samples 0 in the original array
        y_win_filt[0:overlap_win] = np.zeros(overlap_win)
        t_win[0:overlap_win] = np.zeros(overlap_win)

        # axis settings
        y_min = np.min(y_shift) - np.std(y_shift) * 5
        y_max = np.max(y_shift) + np.std(y_shift) * 5
        t_min = np.min(t_shift) - np.std(t_shift) * 10
        t_max = np.max(t_shift) + np.std(t_shift) * 2

        #plot the shifted data points
        plt.axis([t_min, t_max, y_min, y_max])
        plt.plot(t_shift, y_shift, 'o-')
        plt.pause(pause)

    # increment
    i += 1
    t += 1

    if i > len(sample) - 1:
        aborted = True

    #if i % 100 == 0:
    #    plt.cla() 

plt.show()


