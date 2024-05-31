import numpy as np
import mne
from mne_icalabel import label_components

# config
mne.set_log_level('WARNING')

# Constants
num_components = 8

allOutputs = np.genfromtxt('C:/Users/JackC/Documents/GitHub/EEGcontroller/MeasurementSubgroup/Our_measurements/Measurement_prompt/EEGdata-2024-149--15-45-38.csv', delimiter=',')

channels = allOutputs[1:, 0:8].transpose()


print(channels.shape)

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

ica = mne.preprocessing.ICA(n_components=num_components, random_state=0, max_iter=1000)
ica.fit(raw)

# # assuming you have a Raw and ICA instance previously fitted
# labels = label_components(raw, ica, method='iclabel')
# print(labels)

ica.plot_components(picks=range(num_components), ch_type='eeg')

# ica.exclude = [0,1]

# # ica.apply() changes the Raw object in-place, so let's make a copy first:
# reconst_raw = raw.copy()
# ica.apply(reconst_raw)

# raw.plot(order=raw, n_channels=len(raw), show_scrollbars=False)
# reconst_raw.plot(
#     order=raw, n_channels=len(raw), show_scrollbars=False
# )
# del reconst_raw