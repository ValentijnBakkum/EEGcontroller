import numpy as np
import matplotlib.pyplot as plt

def High_pass_filter(data, band_limit, sampling_rate):
     cutoff_index = int(band_limit * data.size / sampling_rate)
     F = np.fft.rfft(data, axis=0)
     F[0:cutoff_index + 1] = 0
     return np.fft.irfft(F, n=data.size).real

filename = input("enter file name:\n")

allOutputs = np.genfromtxt('DataCollection/CSVFiles/' + filename + '.csv', delimiter=',')

channels = allOutputs[1:, 0:8].transpose()

location_array = [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1), (2, 0), (3, 1), (2, 2)]

for i in range(0, 8):
    plt.subplot2grid((4,3), location_array[i])
    plt.specgram(High_pass_filter(channels[i], 1.5, 250), Fs=250)
    plt.title("EEG " + str(i+1))

plt.tight_layout()

#plt.savefig('DataCollection/CSVFiles/' + filename + ' spectrum.png')
plt.show()