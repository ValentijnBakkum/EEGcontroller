import numpy as np
import pandas as pd
from scipy import signal
import matplotlib.pyplot as plt
import torch

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
    lowcut = 2
    highcut = 30
    fs = 250  # Sampling frequency

    # Calculate the filter coefficients
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(8, [low, high], btype='band')

    # Apply the filter to each column of the DataFrame
    df_filt = lfilter(b, a, df_input, axis = 0)

    # import scipy.signal as signal

    # Define the notch filter parameters
    fs = 250  # Sampling frequency
    f0 = 50  # Notch frequency
    Q = 1 # Quality factor

    # Design the notch filter
    b, a = signal.iirnotch(f0, Q, fs)

    # Apply the filter to each column of the DataFrame
    df_filt1 = lfilter(b, a, df_filt)
    return df_filt1

def CAR_filter(logits):
    a, b = logits.shape
    
    # initialise zero array to hold channel average
    channel_average = np.zeros((a, b))

    # compute average for each channel
    for i in range(a):
        for j in range(b):
            channel_average[i, j] = np.mean(logits[i, j, :])
    
    # initialise empty array to hold filtered logits
    logits_CAR = np.empty_like(logits)

    # subtract all readings by channel average to create new 'reference' signals
    for i in range(a):
        for j in range(b):
            logits_CAR[i, j, :] = logits[i, j, :] - channel_average[i, j]
    
    return logits_CAR

# Read the CSV file into a NumPy array
data_csv = pd.read_csv('C:/Users/JackC/Documents/GIthub/EEGcontroller/MeasurementSubgroup/Our_measurements/Measurement_prompt/EEGdata-2024-148--14-48-17.csv', delimiter=',')
data_csv = np.array(data_csv)[:72000,:8] # select the 8 channels and remove 5 samples buffer

#data_csv_car = CAR_filter(data_csv)
data_csv_detr = detrend(data_csv)
data_csv_filt = filter(data_csv_detr)
data_csv_torch = torch.from_numpy(data_csv_filt)


