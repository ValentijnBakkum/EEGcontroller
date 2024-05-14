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

from pylsl import StreamInlet, resolve_stream

duration = 10
sampling_frequency = 250
down_sampling_ratio = 10

def filter(y):
    from scipy.signal import butter, filtfilt

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
    y_filtered = filtfilt(b, a, np.array(y))
    return y_filtered

def main():
    streams = resolve_stream()
    inlet = StreamInlet(streams[0])

    aborted = False

    i = 0
    j = 0
    t = np.zeros((int(duration*sampling_frequency/down_sampling_ratio)))
    y = np.zeros((int(duration*sampling_frequency/down_sampling_ratio)))
    choosen_electrode = int(input("Which electrode should be plotted? (0-7)"))
    print("Press 'ESC' to stop the plot")

    while not aborted:
        j = i//down_sampling_ratio # i / 10 and truncated to whole numbers
        sample, timestamp = inlet.pull_sample() 

        if i%down_sampling_ratio==0: # after each 10 samples
            if j < int(duration*sampling_frequency/down_sampling_ratio): # j smaller than 250, 10 seconds
                t[j] = timestamp
                y[j] = sample[choosen_electrode]
            else: # after 10 seconds plot the data in real-time
                t = np.roll(t, -1) # move first element to the end of array
                y = np.roll(y, -1)

                y_filt = filter(y[::-1]) 
                y_filt = np.mean(y_filt)
                sample[choosen_electrode] = int(y_filt)

                t[-1] = timestamp # replace last element with timestamp
                y[-1] = sample[choosen_electrode] # replace last element with sample date
                
                std = np.std(y_filt)

                plt.axis([t[0]-1, t[1]+1, np.min(y)-std, np.max(y)+std])

                plt.plot(t, y, 'o-', c='c')
                
                plt.pause(0.1)

        i += 1
        print(i, j)

        #if i % 1000 == 0:
        #    plt.cla()

        if msvcrt.kbhit() and msvcrt.getch()[0] == 27:
            aborted = True

    plt.show()

if __name__ == '__main__':
    main()