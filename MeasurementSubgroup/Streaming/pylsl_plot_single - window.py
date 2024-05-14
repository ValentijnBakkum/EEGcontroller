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

import msvcrt
import numpy as np
import matplotlib.pyplot as plt

from pylsl import StreamInlet, resolve_stream

# Data settings
duration = 10
sampling_frequency = 250
down_sampling_ratio = 10

# Window settings
window = 30
overlap = 0.5

# Plot settings
pause = 0.001

i, j, k, l = 0, 0, 0, 0

y = np.zeros(window)  # array of size of window
y_r1 = np.zeros(int(window / 2))  # array of size of window
y_r2 = np.zeros(window)  # array of size of window
y_l1 = []
y_win = np.zeros(window)  # window array

t_r1 = np.zeros(int(window / 2))  # array of size of window
t_r2 = np.zeros(window)  # array of size of window
t_l1 = []
t_win = np.zeros(window)  # window array

streams = resolve_stream()
inlet = StreamInlet(streams[0])
counter_init, timestamp = inlet.pull_sample()

choosen_electrode = 0 #int(input("Which electrode should be plotted? (0-7)")) # Electrode election
print("Press 'ESC' to stop the plot") # Stop the plot

aborted = False

def flatten(xss):
    return [x for xs in xss for x in xs]

while not aborted:
    sample,timestamp = inlet.pull_sample() 

    # Get a new sample when window is full
    if i % window != 0:
        y_win[k] = sample[choosen_electrode] # EEG data 1
        t_win[k] = (sample[15] - counter_init[15])/250 # Counter from EEG cap in seconds
    # Reset the k when window is full
    else:
        k = 0
        y_win[k] = sample[choosen_electrode]
        t_win[k] = (sample[15] - counter_init[15])/250

    # Get the next sample
    k += 1
    i += 1

    # If i is greater than window (initialized window), increment j
    if i > window:
        j += 1

    #print(y_win, "win")

    # Shift the window
    if i % window == 0 and j == 0:  # when i is a multiple of window and j is 0
        # y 
        y_l = y_win[:int(overlap * window)]  # left side of the shifted window
        y_r = y_win[int(overlap * window):]  # right side of the shifted window

        #y_l1.append(y_l.tolist())  # append the shifted values to the list
        #print(y_l)
        y_l1 = y_l.tolist()

        y_out = np.concatenate((y_l, y_r))  # concatenate the left and right side of the shifted window

        # t
        t_l = t_win[:int(overlap * window)]  # left side of the shifted window 
        t_r = t_win[int(overlap * window):]  # right side of the shifted window

        #t_l1.append(t_l.tolist())  # append the shifted values to the list
        t_l1 = t_l.tolist()

        t_out = np.concatenate((t_l, t_r))  # concatenate the left and right side of the shifted window

        l = 1  # l counter to 1
        #print(t_out, "out1")

        y_filt = filter(y_out)  # filter the data
        y_out = y_filt

        y_min = np.min(y_out) - np.std(y_out) * 2
        y_max = np.max(y_out) + np.std(y_out) * 2
        t_min = np.min(t_out) - np.std(t_out) * 5
        t_max = np.max(t_out) + np.std(t_out) * 2

        #plot the shifted data points
        plt.axis([t_min, t_max, y_max, y_min])
        plt.plot(t_l1, y_l1, 'o-')
        plt.pause(pause)

    elif j % int(window * overlap) == 0 and l != 0:  # when j is a multiple of window*overlap and l is not 0
        overlap_win = int(overlap * window * l) % window # calculate the overlap
        overlap_win1 = int(overlap * window * (l + 1)) % window # calculate the overlap

        if overlap_win1 < overlap_win:
            y_l = np.concatenate((y_win[overlap_win:], np.array(y_win[:overlap_win1+1])))  # part of window that is shifted and will be used for the plot
            t_l = np.concatenate((t_win[overlap_win:], np.array(t_win[:overlap_win1+1])))  # part of window that is shifted and will be used for the plot
        else:
            y_l = y_win[overlap_win:overlap_win1+1]  # part of window that is shifted and will be used for the plot
            t_l = t_win[overlap_win:overlap_win1+1]  # part of window that is shifted and will be used for the plot

        #print(y_l, "overlap")
        # y
        #y_l1.append(y_l.tolist())  # append the shifted values to the list
        #print(y_l)
        y_l1 = y_l.tolist()

        y_l = y_win[:overlap_win]  # left side of the shifted window

        y_out = np.concatenate((y_r, y_l))  # concatenate the left and right side of the shifted window

        y_r = y_win[overlap_win1:]  # new right side of the shifted window

        # t
        #t_l1.append(t_l.tolist())  # append the shifted values to the list
        t_l1 = t_l.tolist()

        t_l = t_win[:overlap_win]  # left side of the shifted window

        t_out = np.concatenate((t_r, t_l))  # concatenate the left and right side of the shifted window

        t_r = t_win[overlap_win1:]  # new right side of the shifted window


        l += 1  # increment l counter

        #print(y_out, "out2")
        #print(t_out, "out2")

        y_out = filter(y_out)  # filter the data

        y_min = np.min(y_out) - np.std(y_out) * 2
        y_max = np.max(y_out) + np.std(y_out) * 2
        t_min = np.min(t_out) - np.std(t_out) * 10
        t_max = np.max(t_out) + np.std(t_out) * 2

        #plot the shifted data points
        plt.axis([t_min, t_max, y_max, y_min])
        plt.plot(t_l1, y_l1, 'o-')
        plt.pause(pause)

    if msvcrt.kbhit() and msvcrt.getch()[0] == 27:
        aborted = True

    #if i % 500 == 0:
    #    plt.cla() 

#y_l1 = flatten(y_l1)
#t_l1 = flatten(t_l1)

plt.show()


#    while not aborted:
#         j = i//down_sampling_ratio # i / 10 and truncated to whole numbers
#         sample, timestamp = inlet.pull_sample() 

#         # take the average value of 10 samples and set this as sample data
#         if i%down_sampling_ratio!=0:
#             y_ave[k] = sample[choosen_electrode]
#             k += 1
#         else:
#             sample[choosen_electrode] = np.mean(y_ave)
#             y_ave = np.zeros(down_sampling_ratio)
#             k = 0

#         if i%down_sampling_ratio==0: # after each 10 samples
#             if j < int(duration*sampling_frequency/down_sampling_ratio): # j smaller than 250, 10 seconds to initialize array
#                 t[j] = timestamp
#                 y[j] = sample[choosen_electrode]
#             else: # after 10 seconds plot the data in real-time
#                 t = np.roll(t, -1) # move first element to the end of array
#                 y = np.roll(y, -1)


#                 t[-1] = timestamp # replace last element with timestamp
#                 #y[-1] = sample[choosen_electrode] # replace last element with sample date
#                 y[-1] = np.mean(y_ave)
                
#                 std = np.std(y)

#                 plt.axis([t[0]-1, t[1]+1, np.min(y)-std, np.max(y)+std])

#                 plt.plot(t, y, 'o-', c='c')
                
#                 plt.pause(0.1)

#         i += 1
#         print(i, j) \\

#         #if i % 1000 == 0:
#         #    plt.cla() 

# import msvcrt
# import numpy as np
# import matplotlib.pyplot as plt

# from pylsl import StreamInlet, resolve_stream

# duration = 10
# sampling_frequency = 250
# down_sampling_ratio = 10
# window = 10
# overlap = 0.4

# i = 0
# j = 0
# k = 0
# l = 0

# t = np.zeros((int(duration*sampling_frequency/down_sampling_ratio)))

# y = np.zeros(window) # array of size of window
# y_r1 = np.zeros(int(window/2)) # array of size of window
# y_r2 = np.zeros(window) # array of size of window
# y_l1 = []
# y_win = np.zeros(window) # window array

# choosen_electrode = 0 #int(input("Which electrode should be plotted? (0-7)")) # Electrode election
# print("Press 'ESC' to stop the plot") # Stop the plot

# sample = 1
# aborted = False

# while not aborted:

#     # Get a new sample when window is full
#     if  i != 0 and i % window != 0:
#         y_win[k] = sample#[choosen_electrode] 
#     # Reset the k when window is full
#     else:
#         k = 0
#         y_win[k] = sample#[choosen_electrode]

#     # Get the next sample
#     k += 1
#     i = i + 1

#     print(y_win, "win")

#     # Shift the window
#     if i % window == 0: # when i is not 0 and i is a multiple of window
#         y_l = y_win[:int(overlap*window)] # left side of the shifted window
#         y_r = y_win[int(overlap*window):]  # right side of the shifted window
#         y_out = np.concatenate((y_l, y_r))  # concatenate the left and right side of the shifted window
#         l = 1 # l counter to 1
#         print(y_out, "out1")

#     elif i % int(window*overlap) == 0 and l != 0: # when i is not 0 and i is a multiple of window*overlap
#         y_l = y_win[int(overlap*window*(l)):int(overlap*window*(l+1))]  # part of window that is shifted and will be used for the plot
#         y_l1.append(np.array(y_l)) # append the shifted values to the list

#         y_l = y_win[:int(overlap*window*(l))] # left side of the shifted window

#         print(y_l,y_r,"lr")

#         y_out = np.concatenate((y_r, y_l)) # concatenate the left and right side of the shifted window

#         y_r = y_win[int(overlap*window*(l+1)):] # new right side of the shifted window
#         l = l + 1 # increment l counter

#         print(y_out, "out2")
    
#     if i > 23:
#         aborted = True

#     sample = sample + 1

# plt.plot(y, 'o-', c='c')
# #plt.show()