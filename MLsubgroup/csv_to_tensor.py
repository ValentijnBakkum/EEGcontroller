import os
import numpy as np
import pandas as pd
from scipy import signal
import matplotlib.pyplot as plt
import torch

class cleaner: 

    # Detrend function (remove DC component)
    def detrend(input):
        # Define the segment size
        prompt_size = 1500
        prompts = 72000/prompt_size

        for i in range(int(prompts)):
            input[1500*i : 1500*(i+1)] = signal.detrend(input[1500*i : 1500*(i+1)], axis = 0)
        
        return input

    # Filter function
    def filter(df_input):
        from scipy.signal import butter, lfilter, lfilter_zi
        from scipy import signal

        # Define the filter parameters
        lowcut = 8
        highcut = 30
        fs = 250  # Sampling frequency

        # Calculate the filter coefficients
        nyquist = 0.5 * fs
        low = lowcut / nyquist
        high = highcut / nyquist
        b, a = butter(4, [low, high], btype='band')

        # Apply the filter to each column of the DataFrame
        df_filt = lfilter(b, a, df_input, axis = 0)

        # Define the filter parameters
        lowcut = 49
        highcut = 51
        fs = 250  # Sampling frequency

        # Calculate the filter coefficients
        nyquist = 0.5 * fs
        low = lowcut / nyquist
        high = highcut / nyquist
        b, a = butter(4, [low, high], btype='bandstop')

        # Apply the filter to each column of the DataFrame
        df_filt1 = lfilter(b, a, df_filt, axis = 0)
        return df_filt1

    def CAR_filter(logits):
        a,b,c = logits.shape
        # initialise zero tensor to hold channel average
        channel_average = torch.zeros(a, b)

        # compute average for each channel
        for i in range(int(logits.size(0))):
            for j in range(int(logits.size(1))):
                for k in range(int(logits.size(2))):
                    channel_average[i][j] += logits[i][j][k]
                channel_average[i][j] = channel_average[i][j] / 16
        
        # initalise empty tensor to hold filtered logits
        logits_CAR = torch.empty(int(logits.size(0)), int(logits.size(1)), int(logits.size(2)))

        # subtract all readings by channel average to create new 'reference' signals
        for i in range(int(logits.size(0))):
            for j in range(int(logits.size(1))):
                for k in range(int(logits.size(2))):
                    logits_CAR[i][j][k] = logits[i][j][k] - channel_average[i][j]
        
        return logits_CAR

    def cursed_reshape(numpy_array):
        output_array = np.empty((0, 1, 529, 8))
        lists_of_epochs = np.array([
        [  6,  90, 138, 150, 234, 258], 
        [ 18,  78, 102, 186, 210, 270], 
        [ 30,  66, 114, 162, 198, 282], 
        [ 42,  54, 126, 174, 222, 246]
        ]) * 250
        reshaped_epochs = lists_of_epochs.reshape(24)
        for epoch in reshaped_epochs:
            temp_array = numpy_array[epoch:(epoch + (2 * 529))]
            output_array = np.concatenate((output_array, temp_array.reshape(2, 1, 529, 8)), axis=0)

        labels_start = np.array([1, 2, 3, 4])
        lables = np.repeat(labels_start, 6*2)

        return (output_array, lables)


