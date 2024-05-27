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
tmin, tmax = -5, 5
win_size = 100
channel = 3 -1 # the -1 is because the array index is from 0-7 and the channel id is from 1-8

# things to be set by future code
#epoch_list = np.array(sampling_rate*[11.12, 20, 30, 40, 47])

# function definitions
def extract_epoch_window(channels, sampleStamp):
    sample_min = int(sampleStamp + (sampling_rate * tmin))
    sample_max = int(sampleStamp + (sampling_rate * tmax))
    window = channels[:, sample_min:sample_max]
    return window

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

def notch_filter (time_signals):
    from scipy.signal import lfilter
    from scipy import signal

    # Remove the DC component
    time_signals = signal.detrend(time_signals)

    # Define the notch filter parameters
    fs = 250  # Sampling frequency
    f0 = 50  # Notch frequency
    Q = 1 # Quality factor

    # Design the notch filter
    b, a = signal.iirnotch(f0, Q, fs)

    # Apply the filter to each column of the DataFrame
    y_filtered = lfilter(b, a, time_signals)

    return y_filtered

def window_averaging(time_signal, window_size):
    from scipy import signal
    win = signal.windows.boxcar(window_size)

    for i in range(0, time_signal[:, 0].size):
        time_signal[i] = signal.convolve(time_signal[i], win, mode='same') / sum(win)

    return time_signal

def baseline_readjustment(time_signal):
    baselines = np.expand_dims(np.mean(time_signal[:, 125:375], axis=1), axis=1)
    pad_length = time_signal[0, :].size - 1
    padded_baselines = np.pad(baselines, ((0, 0), (0, pad_length)), mode='edge')
    output = ((time_signal - padded_baselines)/padded_baselines) * 100
    return output


#def post_fft_filter(fsignal, f_low, f_high, scale_factor):
#    output_array = np.zeros(fsignal.size)
#    output_array[f_low*scale_factor:f_high*scale_factor] = fsignal[f_low*scale_factor:f_high*scale_factor]
#    return np.fft.ihfft(output_array)

# start of actual code
allOutputs = np.genfromtxt('MeasurementSubgroup/Our_measurements/Measurement_prompt/EEGdata-2024-144--14-24-41.csv', delimiter=',')


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

    notched = notch_filter(all_epochs)

    delta_evoked = filter(notched,  1,  4)
    theta_evoked = filter(notched,  4,  8)
    alpha_evoked = filter(notched,  8, 12)
    beta_evoked  = filter(notched, 12, 30)
    gamma_evoked = filter(notched, 30, 50)

    delta_evoked = delta_evoked **2
    theta_evoked = theta_evoked **2
    alpha_evoked = alpha_evoked **2
    beta_evoked  = beta_evoked  **2
    gamma_evoked = gamma_evoked **2

    delta_evoked = np.mean(delta_evoked, axis=0)
    theta_evoked = np.mean(theta_evoked, axis=0)
    alpha_evoked = np.mean(alpha_evoked, axis=0)
    beta_evoked  = np.mean(beta_evoked , axis=0)
    gamma_evoked = np.mean(gamma_evoked, axis=0)

    delta_evoked = window_averaging(delta_evoked, win_size)
    theta_evoked = window_averaging(theta_evoked, win_size)
    alpha_evoked = window_averaging(alpha_evoked, win_size)
    beta_evoked  = window_averaging(beta_evoked , win_size)
    gamma_evoked = window_averaging(gamma_evoked, win_size)

    delta_evoked = baseline_readjustment(delta_evoked)
    theta_evoked = baseline_readjustment(theta_evoked)
    alpha_evoked = baseline_readjustment(alpha_evoked)
    beta_evoked  = baseline_readjustment(beta_evoked )
    gamma_evoked = baseline_readjustment(gamma_evoked)

    delta_ax.plot(delta_evoked[channel, :])
    theta_ax.plot(theta_evoked[channel, :])
    alpha_ax.plot(alpha_evoked[channel, :])
    beta_ax.plot(beta_evoked[channel, :])
    gamma_ax.plot(gamma_evoked[channel, :])

delta_ax.legend(['Right hand', 'Left hand', 'Feet', 'Tongue'])
theta_ax.legend(['Right hand', 'Left hand', 'Feet', 'Tongue'])
alpha_ax.legend(['Right hand', 'Left hand', 'Feet', 'Tongue'])
beta_ax.legend(['Right hand', 'Left hand', 'Feet', 'Tongue'])
gamma_ax.legend(['Right hand', 'Left hand', 'Feet', 'Tongue'])

plt.show()


    # delta 1-4 hz, theta 4-8 hz, alpa 8 - 12 hz, beta low 12-16, beta mid 16-20, beta high 20-30, gamma 30-50 hz