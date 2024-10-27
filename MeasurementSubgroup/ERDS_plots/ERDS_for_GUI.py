# Modified from code by: Clemens Brunner <clemens.brunner@gmail.com>
#                        Felix Klotzsche <klotzsche@cbs.mpg.de>
#
# License: BSD-3-Clause
# Copyright the MNE-Python contributors.

import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.colors import TwoSlopeNorm

import mne
from mne.datasets import eegbci
from mne.io import concatenate_raws, read_raw_edf
from mne.stats import permutation_cluster_1samp_test as pcluster_test

# config
mne.set_log_level('WARNING')

def singlefile(filename):
    output = np.genfromtxt('MeasurementSubgroup/Our_measurements/Measurement_prompt/' + filename, delimiter=',')[1:, :]
    events = np.array([[ 1500, 0, 1],
                        [ 4500, 0, 2],
                        [ 7500, 0, 3],
                        [10500, 0, 4],
                        [13500, 0, 4],
                        [16500, 0, 3],
                        [19500, 0, 2],
                        [22500, 0, 1],
                        [25500, 0, 2],
                        [28500, 0, 3],
                        [31500, 0, 4],
                        [34500, 0, 1],
                        [37500, 0, 1],
                        [40500, 0, 3],
                        [43500, 0, 4],
                        [46500, 0, 2],
                        [49500, 0, 3],
                        [52500, 0, 2],
                        [55500, 0, 4],
                        [58500, 0, 1],
                        [61500, 0, 4],
                        [64500, 0, 1],
                        [67500, 0, 2],
                        [70500, 0, 3]])

    return (output, events)
    

#———————————————————————————————————————————————————————————————————————
#(allOutputs, events) = multifile(["EEGdata-2024-149--16-41-44.csv"])
#———————————————————————————————————————————————————————————————————————
recordings_list = os.listdir('MeasurementSubgroup/Our_measurements/Measurement_prompt')
(allOutputs, events) = singlefile(recordings_list[-2])
#———————————————————————————————————————————————————————————————————————

channels = allOutputs[:, 0:8].transpose()

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

tmin, tmax = -1, 4
event_ids = {'right': 1, "left": 2, 'tongue': 3, 'feet': 4}  # map event IDs to tasks

epochs = mne.Epochs(
    raw,
    events = events,
    event_id=[1, 2, 3, 4],
    tmin=tmin - 0.5,
    tmax=tmax + 0.5,
    picks=(    'Fz', 
        'C3',  'Cz',  'C4', 
               'Pz', 
        'PO7', 'Oz',  'PO8'),
    baseline=None,
    preload=True,
)

freqs = np.arange(2, 36)  # frequencies from 2-35Hz
vmin, vmax = -1, 1.5  # set min and max ERDS values in plot
baseline = (-1, 0)  # baseline interval (in s)
cnorm = TwoSlopeNorm(vmin=vmin, vcenter=0, vmax=vmax)  # min, center & max ERDS

kwargs = dict(
    n_permutations=100, step_down_p=0.05, seed=1, buffer_size=None, out_type="mask"
)  # for cluster test

# Finally, we perform time/frequency decomposition over all epochs.
tfr = epochs.compute_tfr(
    method="multitaper",
    freqs=freqs,
    n_cycles=freqs,
    use_fft=True,
    return_itc=False,
    average=False,
    decim=2,
)
tfr.crop(tmin, tmax).apply_baseline(baseline, mode="percent")

df = tfr.to_data_frame(time_format=None)
df.head()

df = tfr.to_data_frame(time_format=None, long_format=True)

# Map to frequency bands:
freq_bounds = {"_": 0, "delta": 3, "theta": 7, "alpha": 13, "beta": 35, "gamma": 140}
df["band"] = pd.cut(
    df["freq"], list(freq_bounds.values()), labels=list(freq_bounds)[1:]
)

# Filter to retain only relevant frequency bands:
freq_bands_of_interest = ["delta", "theta", "alpha", "beta"]
df = df[df.band.isin(freq_bands_of_interest)]
df["band"] = df["band"].cat.remove_unused_categories()

# Order channels for plotting:
df["channel"] = df["channel"].cat.reorder_categories(('Fz', 'C3', 'Cz', 'C4', 'Pz', 'PO7', 'Oz', 'PO8'), ordered=True)

df = df.drop(df.index[df['time'].isin([-1.004])], axis=0)

g = sns.FacetGrid(df, row="band", col="channel", margin_titles=True)
g.map(sns.lineplot, "time", "value", "condition", n_boot=10)
axline_kw = dict(color="black", linestyle="dashed", linewidth=0.5, alpha=0.5)
g.map(plt.axhline, y=0, **axline_kw)
g.map(plt.axvline, x=0, **axline_kw)
g.set(ylim=(None, 1.5))
g.set_axis_labels("Time (s)", "ERDS")
g.set_titles(col_template="{col_name}", row_template="{row_name}")
g.add_legend(ncol=2, loc="lower center")
g.figure.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.08)


plt.show()

with open("plot_opened.signal", "w") as f:
    f.write("Plot opened")
