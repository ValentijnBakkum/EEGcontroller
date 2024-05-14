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
prompt_label = 0
tmin, tmax = -1.5, 4.5
baseline_time = 0.2

# things to be set by future code
epoch_list = np.array(sampling_rate*[11.12, 20, 30, 40, 47])

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

def post_fft_filter(fsignal, f_low, f_high, scale_factor):
    output_array = np.zeros(fsignal.size)
    output_array[f_low*scale_factor:f_high*scale_factor] = fsignal[f_low*scale_factor:f_high*scale_factor]
    return np.fft.ihfft(output_array)

# start of actual code
allOutputs = np.genfromtxt('DataCollection/CSVFiles/Thinking of bicep curl right arm.csv', delimiter=',')

channels = allOutputs[1:, 0:8].transpose()

# code chunk for creating the averaged evoked potential signal.

all_epochs = np.zeros((epoch_list.size, 8, int(sampling_rate * tmax) - int(sampling_rate * tmin)))

for i in range(0, epoch_list.size):
    all_epochs[i] = extract_epoch_window(channels, epoch_list[i])

per_channel_evoked = np.mean(all_epochs, axis=0)
averaged_channels_evoked = np.mean(per_channel_evoked, axis=0)

plt.figure()
plt.plot(averaged_channels_evoked)

fft_evoked = np.fft.hfft(averaged_channels_evoked)
num_fft_samples = fft_evoked.size

fft_scale_factor = int(num_fft_samples/sampling_rate)

delta_evoked = post_fft_filter(fft_evoked,  1,  4, fft_scale_factor)
theta_evoked = post_fft_filter(fft_evoked,  4,  8, fft_scale_factor)
alpha_evoked = post_fft_filter(fft_evoked,  8, 12, fft_scale_factor)
beta_evoked  = post_fft_filter(fft_evoked, 12, 30, fft_scale_factor)
gamma_evoked = post_fft_filter(fft_evoked, 30, 50, fft_scale_factor)

plt.figure()
plt.title("Delta")
plt.plot(delta_evoked)

plt.figure()
plt.title("Theta")
plt.plot(theta_evoked)

plt.figure()
plt.title("Alpha")
plt.plot(alpha_evoked)

plt.figure()
plt.title("Beta")
plt.plot(beta_evoked)

plt.figure()
plt.title("Gamma")
plt.plot(gamma_evoked)

plt.show()


# delta 1-4 hz, theta 4-8 hz, alpa 8 - 12 hz, beta low 12-16, beta mid 16-20, beta high 20-30, gamma 30-50 hz