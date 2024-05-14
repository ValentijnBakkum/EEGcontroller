import numpy as np
import mne

# config
mne.set_log_level('WARNING')

# Constants
num_components = 8

allOutputs = np.genfromtxt('DataCollection/CSVFiles/Teeth clincing.csv', delimiter=',')

channels = allOutputs[1:, 0:8].transpose()

# create mne_info object
ch_names =        ['Fz', 
            'C3',  'Cz',  'C4', 
                   'Pz', 
            'PO7', 'Oz',  'PO8']

ch_type = ['eeg' for i in range(8)]
mne_info = mne.create_info(ch_names, float(250), ch_types=ch_type)

#create mne.raw object
raw = mne.io.RawArray(channels, mne_info)
raw.set_montage(mne.channels.make_standard_montage("standard_1005"))
#print(raw)

#actual code
raw.filter(0.5, 40)

ica = mne.preprocessing.ICA(n_components=num_components, random_state=97, max_iter=400)
ica.fit(raw)

ica.plot_components(picks=range(num_components), ch_type='eeg')