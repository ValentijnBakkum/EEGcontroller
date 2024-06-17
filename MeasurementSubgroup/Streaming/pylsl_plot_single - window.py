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
from scipy.signal import welch

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
    y_filtered_band, _= lfilter(b, a, np.array(y), zi = zi)

    # Define the notch filter parameters
    fs = 250  # Sampling frequency
    f0 = 50  # Notch frequency
    Q = 1 # Quality factor

    # Design the notch filter
    b, a = signal.iirnotch(f0, Q, fs)
    zi = lfilter_zi(b,a)*y[0]

    # Apply the filter to each column of the DataFrame
    y_filtered, _ = lfilter(b, a, np.array(y), zi = zi)

    return y_filtered

# Window settings
window = 50
overlap = 0.9

# Plot settings
pause = 0.004

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
y_out = np.array([])
t_out = np.array([])
aborted = False

# main loop
while not aborted:
    # Get data from LSL interface
    sample,timestamp = inlet.pull_sample() 
    #print(sample)

    #calculate sample overlap
    overlap_win = int(overlap * window)

    # assign EEG data to array
    y_win[0] = sample[choosen_electrode] # EEG data 1
    t_win[0] = (i)/250 # Counter from EEG cap in seconds

    # Shift the array with one index
    y_win = np.roll(y_win, -1)
    t_win = np.roll(t_win, -1)

    # if i % 10 == 0:
    #     y_win_filt = filter(y_win)
        
    #     # axis settings
    #     y_min = np.min(y_win_filt) - np.std(y_win_filt)
    #     y_max = np.max(y_win_filt) + np.std(y_win_filt) 
    #     t_min = np.min(t_win) - np.std(t_win)
    #     t_max = np.max(t_win) + np.std(t_win)

    #     #plot the shifted data points
    #     plt.axis([t_min, t_max, y_min, y_max])
    #     plt.plot(t_win[-10:], y_win_filt[-10:], 'o-')
    #     plt.pause(pause)

    #print(y_win, "window input")
    #print(t_win)

    # When a new block of L is reached
    if i % window == 0 and i != window and i != 0:
        # apply filter to window
        y_win_filt = filter(y_win)
        #y_win_filt = y_win

        # # Take the samples that are overlapped
        # y_shift = y_win_filt[0:overlap_win]
        # t_shift = t_win[0:overlap_win]

        # Discard the samples that are overlapped
        y_shift = y_win_filt[overlap_win:]
        t_shift = t_win[overlap_win:]

        # Assign the values to an array
        y_shift = np.array(y_shift)
        t_shift = np.array(t_shift)

        # contatenate to the output signal
        y_out = np.concatenate((y_out, y_shift))
        t_out = np.concatenate((t_out, t_shift))

        max_samples_displayed = 500 # only display 500 samples of the output signal
        if len(y_out) > max_samples_displayed:
            y_out = y_out[-max_samples_displayed:]  # Keep the newest 500 samples
        if len(t_out) > max_samples_displayed:
            t_out = t_out[-max_samples_displayed:]  # Keep the newest 500 samples

        # possibly downsample for better visualization
        y_out_down = y_out[::]
        t_out_down = t_out[::]

        # Define a function to compute moving average
        def moving_average(y, window_size):
            # Pad the signal at the boundaries to avoid boundary effects
            padded_y = np.pad(y, (window_size//2, window_size-1-window_size//2), mode='edge')
            # Compute the moving average
            weights = np.ones(window_size) / window_size
            smoothed = np.convolve(weights, padded_y, mode='valid')
            return smoothed

        # Smooth the signal using a moving average with window size 5
        y_out_down = moving_average(y_out_down, window_size=5)

        plt.plot(t_out_down, y_out_down, 'o-')
        # Set y-axis limits
        plt.ylim(-50, 50)
        plt.pause(pause)

        # remove the old plots after 500 samples
        if max_samples_displayed == 500:
            plt.cla() 

        # # Make the overlapped samples 0 in the original array
        # y_win_filt[0:overlap_win] = np.zeros(overlap_win)
        # t_win[0:overlap_win] = np.zeros(overlap_win
        
    #     # FFT
    #     xf = rfftfreq(int(window*overlap), 1/250)
    #     y_fft = rfft(y_shift)

    #     plt.plot(xf, np.abs(y_fft))
    #     plt.xlim([0, 50]) 
    #     plt.pause(pause)

        # # powerbands
        # # Compute the power spectral density using Welch's method
        # frequencies, psd = welch(y_shift, 250)
        # plt.plot(frequencies,psd)
        # plt.xlim([0, 50]) 
        # plt.pause(pause)

        # # Define frequency bands
        # delta_band = (0.5, 4)
        # theta_band = (4, 8)
        # alpha_band = (8, 12)
        # beta_band = (12, 30)
        # gamma_band = (30, 50)

        # # Function to calculate power in a specific frequency band
        # def bandpower(frequencies, psd, band):
        #     band_freq_indices = np.logical_and(frequencies >= band[0], frequencies <= band[1])
        #     band_power = np.sum(psd[band_freq_indices])
        #     return band_power
        
        # # Calculate power for each band
        # delta_power = bandpower(frequencies, psd, delta_band)
        # theta_power = bandpower(frequencies, psd, theta_band)
        # alpha_power = bandpower(frequencies, psd, alpha_band)
        # beta_power = bandpower(frequencies, psd, beta_band)
        # gamma_power = bandpower(frequencies, psd, gamma_band)

        # # Power values
        # powers = [delta_power, theta_power, alpha_power, beta_power, gamma_power]
        # print(powers)
        # bands = ['Delta (0.5-4 Hz)', 'Theta (4-8 Hz)', 'Alpha (8-13 Hz)', 'Beta (13-30 Hz)', 'Gamma (30-50 Hz)']

        # plt.figure(figsize=(10, 6))
        # plt.bar(bands, powers, color=['blue', 'green', 'red', 'purple', 'orange'])
        # plt.xlabel('Frequency Bands')
        # plt.ylabel('Power')
        # plt.title('EEG Power Band Distribution')
        # plt.pause(pause)

        # # axis settings
        # y_min = np.min(y_shift) - np.std(y_shift) * 5
        # y_max = np.max(y_shift) + np.std(y_shift) * 5
        # t_min = np.min(t_shift) - np.std(t_shift) * 10
        # t_max = np.max(t_shift) + np.std(t_shift) * 2

        # #plot the shifted data points
        # plt.axis([t_min, t_max, y_min, y_max])
        # plt.plot(t_shift, y_shift, 'o-')
        # plt.pause(pause)

    # increment
    i += 1
    t += 1

    if msvcrt.kbhit() and msvcrt.getch()[0] == 27:
        aborted = True