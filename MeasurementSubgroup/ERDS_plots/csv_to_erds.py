import matplotlib.pyplot as plt
import numpy as np

"""
refrence material: https://www.youtube.com/watch?v=zDTsePeDlwo

steps:
1. artifact removal
2. filtering
3. segmentation (epochs)
4. baseline correction
5. averaging
"""
# constant definitions:
sampling_rate = 250
tmin, tmax = -1.5, 4.5
baseline_time = 0.2

# things to be set by future code
#epoch_list = np.array(sampling_rate*[11.12, 20, 30, 40, 47])

# function definitions
def extract_epoch_window(channels, sampleStamp):
    sample_min = int(sampleStamp + (sampling_rate * tmin))
    sample_max = int(sampleStamp + (sampling_rate * tmax))
    window = channels[:, sample_min:sample_max]

    baseline_period = int(sampling_rate * baseline_time)
    baselines = np.expand_dims(np.mean(channels[:, sample_min-baseline_period:sample_min], axis=1), axis=1)
    pad_length = window[0, :].size - 1
    if -1 == pad_length:
        raise Exception(f"value in epoch_list out of range of collected data.\nsample stamp: {sampleStamp}")
    padded_baselines = np.pad(baselines, ((0, 0), (0, pad_length)), mode='edge')
    output_array = np.subtract(window, padded_baselines)
    return output_array

def filter(time_signal, flow, fhigh):
    from scipy.signal import butter, lfilter
    from scipy import signal

    # Define the filter parameters
    fs = 250  # Sampling frequency

    # Calculate the filter coefficients
    nyquist = 0.5 * fs
    low = flow / nyquist
    high = fhigh / nyquist
    b, a = butter(4, [low, high], btype='band')

    # Apply the filter to each column of the DataFrame
    y_filtered_band = lfilter(b, a, time_signal)

    return y_filtered_band

def notch_filter (time_signal):
    from scipy.signal import lfilter
    from scipy import signal

    # Remove the DC component
    time_signal = signal.detrend(time_signal, axis=0)

    # Define the notch filter parameters
    fs = 250  # Sampling frequency
    f0 = 50  # Notch frequency
    Q = 1 # Quality factor

    # Design the notch filter
    b, a = signal.iirnotch(f0, Q, fs)

    # Apply the filter to each column of the DataFrame
    y_filtered = lfilter(b, a, time_signal)

    return y_filtered

#def post_fft_filter(fsignal, f_low, f_high, scale_factor):
#    output_array = np.zeros(fsignal.size)
#    output_array[f_low*scale_factor:f_high*scale_factor] = fsignal[f_low*scale_factor:f_high*scale_factor]
#    return np.fft.ihfft(output_array)

# start of actual code
allOutputs = np.genfromtxt('MeasurementSubgroup/Our_measurements/EEGdata-2024-144--14-56-37.csv', delimiter=',')


channels = allOutputs[1:, 0:8].transpose()

# this bit looks confusing, but the hard coded values are in time and the * sampling rate turns it from time to samples
# 0 = Right hand, 1 = Left hand, 2 = Feet, 3 = tongue.
lists_of_epochs = np.array([
    [  6,  90, 138, 150, 234, 258], 
    [ 18,  78, 102, 186, 210, 270,], 
    [ 30,  66, 114, 162, 198, 282], 
    [ 42,  54, 126, 174, 222, 246]
    ]) * sampling_rate

#create figures
averaged_fig,   averaged_ax = plt.subplots()
delta_fig,      delta_ax    = plt.subplots()
theta_fig,      theta_ax    = plt.subplots()
alpha_fig,      alpha_ax    = plt.subplots()
beta_fig,       beta_ax     = plt.subplots()
gamma_fig,      gamma_ax    = plt.subplots()

#set titles
delta_ax.set_title("Delta")
theta_ax.set_title("Theta")
alpha_ax.set_title("Alpha")
beta_ax.set_title("Beta")
gamma_ax.set_title("Gamma")

for k in range(0,4):
    # code chunk for creating the averaged evoked potential signal.
    epoch_list = lists_of_epochs[k]

    all_epochs = np.zeros((epoch_list.size, 8, int(sampling_rate * tmax) - int(sampling_rate * tmin)))

    for i in range(0, epoch_list.size):
        all_epochs[i] = extract_epoch_window(channels, epoch_list[i])

    per_channel_evoked = np.mean(all_epochs, axis=0)
    averaged_channels_evoked = np.mean(per_channel_evoked, axis=0)

    #plt.figure()
    averaged_ax.plot(averaged_channels_evoked**2)

    notched_average = notch_filter(averaged_channels_evoked)

    delta_evoked = filter(notched_average,  1,  4)
    theta_evoked = filter(notched_average,  4,  8)
    alpha_evoked = filter(notched_average,  8, 12)
    beta_evoked  = filter(notched_average, 12, 30)
    gamma_evoked = filter(notched_average, 30, 50)

    delta_ax.plot(delta_evoked**2)
    theta_ax.plot(theta_evoked**2)
    alpha_ax.plot(alpha_evoked**2)
    beta_ax.plot(beta_evoked**2)
    gamma_ax.plot(gamma_evoked**2)

plt.show()


    # delta 1-4 hz, theta 4-8 hz, alpa 8 - 12 hz, beta low 12-16, beta mid 16-20, beta high 20-30, gamma 30-50 hz