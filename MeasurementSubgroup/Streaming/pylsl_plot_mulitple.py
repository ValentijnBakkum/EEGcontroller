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

duration = 4 
sampling_frequency = 250 
down_sampling_ratio = 20
choosen_electrode1 = 1 #selection of the electrode to plot
choosen_electrode2 = 2 #selection of the electrode to plot

fig, axs = plt.subplots(8, figsize=(10 , 15))

def main():
    streams = resolve_stream()
    inlet = StreamInlet(streams[0]) # Get the LSL stream from the EEG cap

    aborted = False

    i = 0
    j = 0
    t = np.zeros((int(duration*sampling_frequency/down_sampling_ratio))) # initialize time (x-axis of the plot)
    y = [np.zeros((int(duration*sampling_frequency/down_sampling_ratio))) for _ in range(8)] # initialize data (y-axis of the plot)

    while not aborted:
        j = i//down_sampling_ratio # index of the data to plot
        sample, timestamp = inlet.pull_sample() # get the streamed data

        if i%down_sampling_ratio==0: # plot the data every 10 samples
            # Get the data in real-time
            if j < int(duration*sampling_frequency/down_sampling_ratio):
                t[j] = timestamp
                for k in range(8): # get the data from the 8 electrodes
                    y[k][j] = sample[k]
            # Plot the data when last sample is reached
            else:
                t = np.roll(t, -1) 
                for k in range(8):
                    y[k] = np.roll(y[k], -1)
                    y[k][-1] = sample[k]
                
                t[-1] = timestamp

                std = [np.std(y[k]) for k in range(8)]

                for k in range(8):
                    axs[k].axis([t[0]-1, t[1]+1, np.min(y[k])-std[k], np.max(y[k])+std[k]]) # set the axis of the plot
                    axs[k].plot(t, y[k], 'o-', c='c') # plot the data

                #plt.plot(t, y1, 'o-', c='c') # plot the data

                plt.pause(0.05) # pause the plot for 0.05s
        i += 1
        if msvcrt.kbhit() and msvcrt.getch()[0] == 27: # stop the plot when the user press the 'esc' key
            aborted = True

    plt.show()

if __name__ == '__main__':
    main()