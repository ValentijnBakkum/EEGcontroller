import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import mne

"""
refrence material: https://www.youtube.com/watch?v=zDTsePeDlwo

steps:
1. artifact removal
2. filtering
3. segmentation (epochs)
4. baseline correction
5. averaging
"""
# config
mne.set_log_level('WARNING')

# constant definitions:
sampling_rate = 250
prompt_label = 0x0301
tmin, tmax = -1.5, 4.5
baseline_time = 0.2

# things to be set by future code
#epoch_list = np.array([11.12, 20, 30, 40, 47])

# function definitions
def extract_epoch_window(channels, sampleStamp):
    sample_min = int(sampleStamp + (sampling_rate * tmin))
    sample_max = int(sampleStamp + (sampling_rate * tmax))
    window = channels[:, sample_min:sample_max]

    baseline_period = int(sampling_rate * baseline_time)
    baselines = np.expand_dims(np.mean(channels[:, sample_min-baseline_period:sample_min], axis=1), axis=1)
    pad_length = window[0, :].size - 1
    padded_baselines = np.pad(baselines, ((0, 0), (0, pad_length)), mode='edge')
    output_array = np.subtract(window, padded_baselines)
    return output_array

def fft_to_percent_power(fsignal, f_low, f_high, scale_factor):
    filtered_array = np.zeros(fsignal.size)
    filtered_array[f_low*scale_factor:f_high*scale_factor] = fsignal[f_low*scale_factor:f_high*scale_factor]
    power = np.abs(np.fft.ihfft(filtered_array))**2
    initial_power = np.mean(power[0:int(sampling_rate/4)])
    power = (power/initial_power) - 1 
    return power

# start of actual code
filename = input("enter file name:\n")

rawGDF = mne.io.read_raw_gdf('DataCollection/Testing dataset analysis/' + filename + '.gdf')

(events_A, events_id_A) = mne.events_from_annotations(rawGDF)

run_id = events_id_A[str(0x7FFE)] # start of a run
cue_id = events_id_A[str(prompt_label)]



startOfRun = events_A[run_id == events_A[:, 2] , 0]
startIndex = startOfRun[1] # currently hard coded to look at run 2
stopIndex = startOfRun[2]

event_within_range = np.logical_and((startIndex < events_A[:, 0]), (stopIndex > events_A[:, 0]))

epoch_list = events_A[np.logical_and(cue_id == events_A[:, 2], event_within_range), 0]
epoch_list = epoch_list - startIndex

allOutputs = rawGDF.to_data_frame()

numpyOutputs = allOutputs.to_numpy()

channels = numpyOutputs[startIndex:stopIndex, [1, 8, 10, 12, 20]].transpose()
counter = numpyOutputs[startIndex:stopIndex, 0].transpose()

# code chunk for creating the averaged evoked potential signal.

all_epochs = np.zeros((epoch_list.size, 5, int(sampling_rate * tmax) - int(sampling_rate * tmin)))

for i in range(0, epoch_list.size):
    all_epochs[i] = extract_epoch_window(channels, epoch_list[i])

per_channel_evoked = np.mean(all_epochs, axis=0)
averaged_channels_evoked = np.mean(per_channel_evoked, axis=0)

plt.figure()
plt.plot(averaged_channels_evoked)

fft_evoked = np.fft.hfft(averaged_channels_evoked)
num_fft_samples = fft_evoked.size

fft_scale_factor = int(num_fft_samples/sampling_rate)

delta_evoked = fft_to_percent_power(fft_evoked,  1,  4, fft_scale_factor)
theta_evoked = fft_to_percent_power(fft_evoked,  4,  8, fft_scale_factor)
alpha_evoked = fft_to_percent_power(fft_evoked,  8, 12, fft_scale_factor)
beta_evoked  = fft_to_percent_power(fft_evoked, 12, 30, fft_scale_factor)
gamma_evoked = fft_to_percent_power(fft_evoked, 30, 50, fft_scale_factor)

plt.figure()
ax = plt.subplot2grid((5, 1), (4, 0))
plt.title("Delta")
plt.plot(delta_evoked)
yabs_max = abs(max(ax.get_ylim(), key=abs))
ax.set_ylim(ymin=-yabs_max, ymax=yabs_max)

ax = plt.subplot2grid((5, 1), (3, 0))
plt.title("Theta")
plt.plot(theta_evoked)
yabs_max = abs(max(ax.get_ylim(), key=abs))
ax.set_ylim(ymin=-yabs_max, ymax=yabs_max)

ax = plt.subplot2grid((5, 1), (2, 0))
plt.title("Alpha")
plt.plot(alpha_evoked)
yabs_max = abs(max(ax.get_ylim(), key=abs))
ax.set_ylim(ymin=-yabs_max, ymax=yabs_max)

ax = plt.subplot2grid((5, 1), (1, 0))
plt.title("Beta")
plt.plot(beta_evoked)
yabs_max = abs(max(ax.get_ylim(), key=abs))
ax.set_ylim(ymin=-yabs_max, ymax=yabs_max)

ax = plt.subplot2grid((5, 1), (0, 0))
plt.title("Gamma")
plt.plot(gamma_evoked)
yabs_max = abs(max(ax.get_ylim(), key=abs))
ax.set_ylim(ymin=-yabs_max, ymax=yabs_max)

plt.show()