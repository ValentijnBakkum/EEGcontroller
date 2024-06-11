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
    a,b,c = logits.shape
    # initialise zero tensor to hold channel average
    channel_average = torch.zeros(2880, 256)

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

def freq_filter(logits):

    # set parameters
    fs = 250
    T = 1 / fs
    L = 256

    # perform FFT
    fft_logits = torch.fft.fftn(logits, dim=(1,))

    # create frequency mask
    frequencies = torch.fft.fftfreq(L, d=T)
    mask = (frequencies >= 0.5) & (frequencies <= 30)
    full_mask = torch.zeros_like(fft_logits, dtype=torch.bool)
    full_mask[:, :len(mask), :] = mask[None, :, None]
    reversed_mask = torch.flip(mask, dims=[0])  
    full_mask[:, -len(mask):, :] = reversed_mask[None, :, None]

    # apply frequency mask
    fft_logits_masked = fft_logits * full_mask

    mask = (frequencies >= 52) & (frequencies <= 48)
    full_mask = torch.zeros_like(fft_logits, dtype=torch.bool)
    full_mask[:, :len(mask), :] = mask[None, :, None]
    reversed_mask = torch.flip(mask, dims=[0])  
    full_mask[:, -len(mask):, :] = reversed_mask[None, :, None]

    # apply frequency mask
    fft_logits_masked1 = fft_logits_masked * full_mask

    # perform IFFT
    logits_filtered = torch.fft.ifftn(fft_logits_masked1, dim=(1,)).real

    return logits_filtered

# Read the CSV file into a NumPy array
data_csv1 = pd.read_csv('C:/Users/JackC/Documents/GIthub/EEGcontroller/MeasurementSubgroup/Our_measurements/Measurement_prompt/EEGdata-2024-149--15-20-21.csv', delimiter=',') 
data_csv2 = pd.read_csv('C:/Users/JackC/Documents/GIthub/EEGcontroller/MeasurementSubgroup/Our_measurements/Measurement_prompt/EEGdata-2024-149--15-35-40.csv', delimiter=',') 
data_csv3 = pd.read_csv('C:/Users/JackC/Documents/GIthub/EEGcontroller/MeasurementSubgroup/Our_measurements/Measurement_prompt/EEGdata-2024-149--15-45-38.csv', delimiter=',') 
data_csv4 = pd.read_csv('C:/Users/JackC/Documents/GIthub/EEGcontroller/MeasurementSubgroup/Our_measurements/Measurement_prompt/EEGdata-2024-149--15-57-42.csv', delimiter=',')

data_csv1 = data_csv1.iloc[:72000,:8] # select the 8 EEG channels and remove 5 samples buffer
data_csv2 = data_csv2.iloc[:72000,:8] # select the 8 EEG channels and remove 5 samples buffer
data_csv3 = data_csv3.iloc[:72000,:8] # select the 8 EEG channels and remove 5 samples buffer
data_csv4 = data_csv4.iloc[:72000,:8] # select the 8 EEG channels and remove 5 samples buffer

data_csv = pd.concat([data_csv1, data_csv2, data_csv3, data_csv4], ignore_index=True)

data_csv_detr = detrend(data_csv) # remove DC component
#data_csv_filt = filter(data_csv_detr) # filter the signal
length = 1125

data_csv = np.array(data_csv)
data_csv_res = data_csv.reshape(int(length), 1, 256, 8) # 288 seconds per recording, 250 samples per seconds

data_csv_torch = torch.from_numpy(data_csv_res) # Change to Torch format

logits = data_csv_torch.squeeze(1)
#data_csv_car = CAR_filter(logits)
data_csv_filt = freq_filter(logits)
logits = data_csv_filt.unsqueeze(1)

print(logits.shape)

#torch.Size([2880, 1, 256, 16])
# 2880 seconsd could be variable
# extra dimension
# 256 samples per sec
# 16 channels

# 4 recordings from 1 subjects into first dimension
# with label? and counter, new columns 
# separate array [1125, 256, 2]
# Raw recording to send? complete recording

