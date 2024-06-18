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

def filter(y, low, high):
    from scipy.signal import butter, lfilter, lfiltic
    from scipy import signal

    # Remove the DC component
    y = signal.detrend(y, axis=0)

    # Define the filter parameters
    lowcut = low
    highcut = high
    fs = 250  # Sampling frequency

    # Calculate the filter coefficients
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(4, [low, high], btype='band')
    #zi = lfilter_zi(b,a)*y[0]

    # Apply the filter to each column of the DataFram
    y_filtered_band= lfilter(b, a, np.array(y))

    # Define the filter parameters
    lowcut = 49
    highcut = 51
    fs = 250  # Sampling frequency

    # Calculate the filter coefficients
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(4, [low, high], btype='bandstop')
    #zi = lfilter_zi(b,a)*y[0]

    # Apply the filter to each column of the DataFram
    y_filtered= lfilter(b, a, np.array(y_filtered_band))

    return y_filtered

# Window settings
window = 500
overlap = 0.25

# Plot settings
pause = 0.01

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

mode = input("What to plot? (EEG, FFT, Powerbands)\n")

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

    # When a new block of L is reached
    if i % overlap_win == 0 and i != overlap_win and i != 0:
        print(i/250, "sec")
        # apply filter to window
        y_win_filt = filter(y_win, 0.5, 38)
        y_win_filt2 = filter(y_win, 8, 30)

        if mode == "EEG":
            #Discard the samples that are overlapped
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
            plt.ylim(-500, 500)
            plt.pause(pause)

            # remove the old plots after 500 samples
            if max_samples_displayed == 500:
                plt.cla() 

        elif mode == "FFT":
        #FFT
        #Apply Hanning window
            # hanning_window = np.hanning(len(y_win_filt))
            # y_win_hann = y_win_filt * hanning_window

            y_win_pad = np.pad(y_win_filt, int(0), 'constant')
            y_win_pad2 = np.pad(y_win_filt2, int(0), 'constant')
            # print(y_win_pad.shape)

            xf = rfftfreq(y_win_pad.shape[0], 1/250)
            y_fft = np.abs(rfft(y_win_pad))
            y_fft2 = np.abs(rfft(y_win_pad2))

            print(y_fft.shape)
            print(y_fft)

            plt.plot(xf, y_fft, label='0.5 - 38 Hz: ML')
            plt.plot(xf, y_fft2, label='8- 30 Hz: MI')
            plt.axvline(4, color='k', linestyle='--', linewidth=1)
            plt.axvline(8, color='k', linestyle='--', linewidth=1)
            plt.axvline(12, color='k', linestyle='--', linewidth=1)
            plt.axvline(30, color='k', linestyle='--', linewidth=1)
            plt.xlim([0, 50]) 
            plt.ylim([0, 10000]) 

            # Add a title
            plt.title('FFT plot of Channel X')

            # Add X and Y axis labels
            plt.xlabel('Frequency (Hz)')
            plt.ylabel('Amplitude')

            # Add a legend with customizations
            plt.legend(loc='upper right', fontsize='medium', title='Legend')

            plt.pause(pause)

            if i % overlap_win == 0:
                plt.cla() 

        elif mode == "Powerbands":
            y_win_pad = np.pad(y_win_filt, int(0.5*window), 'constant')
            y_win_pad2 = np.pad(y_win_filt2, int(0.5*window), 'constant')
            
            # #  PSD
            # # Compute the power spectral density using Welch's method
            frequencies, psd = welch(y_win_pad2, 250)
            # # plt.plot(frequencies,psd)
            # # plt.xlim([0, 50]) 
            # # plt.pause(pause)

            # # Powerbands
            # Define frequency bands
            delta_band = (0.5, 4)
            theta_band = (4, 8)
            alpha_band = (8, 12)
            beta_band = (12, 30)
            gamma_band = (30, 50)

            # Function to calculate power in a specific frequency band
            def bandpower(frequencies, psd, band):
                band_freq_indices = np.logical_and(frequencies >= band[0], frequencies <= band[1])
                band_power = np.sum(psd[band_freq_indices])
                band_power_norm = band_power / (band[1] - band[0])
                return band_power_norm
            
            # Calculate power for each band
            delta_power = bandpower(frequencies, psd, delta_band)
            theta_power = bandpower(frequencies, psd, theta_band)
            alpha_power = bandpower(frequencies, psd, alpha_band)
            beta_power = bandpower(frequencies, psd, beta_band)
            gamma_power = bandpower(frequencies, psd, gamma_band)

            # Power values
            powers = [delta_power, theta_power, alpha_power, beta_power, gamma_power]

            bands = ['Delta (0.5-4 Hz)', 'Theta (4-8 Hz)', 'Alpha (8-13 Hz)', 'Beta (13-30 Hz)', 'Gamma (30-50 Hz)']

            plt.bar(bands, powers, color=['blue', 'green', 'red', 'purple', 'orange'])
            plt.xlabel('Frequency Bands')
            plt.ylabel('Power')
            plt.title('EEG Power Band Distribution')
            plt.ylim([0, 10]) 
            plt.pause(pause)

            if i % overlap_win == 0:
                plt.cla() 

    # increment
    i += 1
    t += 1
    if msvcrt.kbhit() and msvcrt.getch()[0] == 27:
        aborted = True