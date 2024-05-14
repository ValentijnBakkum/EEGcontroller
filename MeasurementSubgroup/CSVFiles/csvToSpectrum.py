import numpy as np
import math
import matplotlib.pyplot as plt

filename = input("enter file name:\n")

allOutputs = np.genfromtxt('DataCollection/CSVFiles/' + filename + '.csv', delimiter=',')

channels = allOutputs[1:, 0:8].transpose()
counter = allOutputs[1:, 15].transpose()

location_array = [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1), (2, 0), (3, 1), (2, 2)]

for i in range(0, 8):
    plt.subplot2grid((4,3), location_array[i])
    plt.specgram(channels[i], Fs=250)
    plt.title("EEG " + str(i+1))

plt.tight_layout()

plt.savefig('DataCollection/CSVFiles/' + filename + ' spectrum.png')

plt.figure()

for i in range(0, 8):
    plt.subplot2grid((4,3), location_array[i])
    plt.plot(counter, channels[i])
    plt.title("EEG " + str(i+1))

plt.tight_layout()


#plt.show()
plt.savefig('DataCollection/CSVFiles/' + filename + '.png')