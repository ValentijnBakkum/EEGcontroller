'''
Created by Victor Delvigne
ISIA Lab, Faculty of Engineering University of Mons, Mons (Belgium)
IMT Nord Europe, Villeneuve d'Ascq (France)
victor.delvigne@umons.ac.be
Source: TBD
Copyright (C) 2021 - UMons/IMT Nord Europe
This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.
This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.
You should have received a copy of the GNU Lesser General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
'''
import msvcrt
import numpy as np
import matplotlib.pyplot as plt

from scipy.fft import rfft, rfftfreq 
from scipy import signal
from scipy.fft import fftshift
from scipy.signal import butter, lfilter, lfilter_zi

from pylsl import StreamInlet, resolve_stream

def filter(y):
    from scipy.signal import butter, lfilter, lfiltic
    from scipy import signal

    # Remove the DC component
    y = signal.detrend(y, axis=0)

    # Define the filter parameters
    lowcut = 2
    highcut = 30
    fs = 250  # Sampling frequency

    # Calculate the filter coefficients
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(8, [low, high], btype='band')
    zi = lfilter_zi(b,a)*y[0]

    # Apply the filter to each column of the DataFram
    y_filtered_band, _ = lfilter(b, a, np.array(y), zi=zi)

    # Define the notch filter parameters
    fs = 250  # Sampling frequency
    f0 = 50  # Notch frequency
    Q = 1 # Quality factor

    # Design the notch filter
    b, a = signal.iirnotch(f0, Q, fs)
    zi = lfilter_zi(b,a)*y[0]

    # Apply the filter to each column of the DataFrame
    y_filtered, _ = lfilter(b, a, np.array(y), zi=zi)

    return y_filtered

# Window settings
window = 50
overlap = 0.5

# Plot settings
pause = 0.1

streams = resolve_stream()
inlet = StreamInlet(streams[0])
counter_init, timestamp = inlet.pull_sample()

choosen_electrode = 0 #int(input("Which electrode should be plotted? (0-7)")) # Electrode election
print("Press 'ESC' to stop the plot") # Stop the plot

# initial values
y_win = np.zeros(window)  # window array
t_win = np.zeros(window)  # time array
t = 1
i = 1
aborted = False

# main loop
while not aborted:
    # Get data from LSL interface
    sample,timestamp = inlet.pull_sample() 

    #calculate sample overlap
    overlap_win = int(overlap * window)

    # assign EEG data to array
    y_win[0] = sample[choosen_electrode] # EEG data 1
    t_win[0] = (sample[15] - counter_init[15])/250 # Counter from EEG cap in seconds

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

    #if i % 100 == 0:
    #    plt.cla() 

    if msvcrt.kbhit() and msvcrt.getch()[0] == 27:
        aborted = True

    #if i % 500 == 0:
    #    plt.cla() 