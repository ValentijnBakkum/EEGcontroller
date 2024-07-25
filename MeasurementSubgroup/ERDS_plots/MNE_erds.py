"""
.. _ex-tfr-erds:

===============================
Compute and visualize ERDS maps
===============================

This example calculates and displays ERDS maps of event-related EEG data.
ERDS (sometimes also written as ERD/ERS) is short for event-related
desynchronization (ERD) and event-related synchronization (ERS)
:footcite:`PfurtschellerLopesdaSilva1999`. Conceptually, ERD corresponds to a
decrease in power in a specific frequency band relative to a baseline.
Similarly, ERS corresponds to an increase in power. An ERDS map is a
time/frequency representation of ERD/ERS over a range of frequencies
:footcite:`GraimannEtAl2002`. ERDS maps are also known as ERSP (event-related
spectral perturbation) :footcite:`Makeig1993`.

In this example, we use an EEG BCI data set containing two different motor
imagery tasks (imagined hand and feet movement). Our goal is to generate ERDS
maps for each of the two tasks.

First, we load the data and create epochs of 5s length. The data set contains
multiple channels, but we will only consider C3, Cz, and C4. We compute maps
containing frequencies ranging from 2 to 35Hz. We map ERD to red color and ERS
to blue color, which is customary in many ERDS publications. Finally, we
perform cluster-based permutation tests to estimate significant ERDS values
(corrected for multiple comparisons within channels).
"""
# Authors: Clemens Brunner <clemens.brunner@gmail.com>
#          Felix Klotzsche <klotzsche@cbs.mpg.de>
#
# License: BSD-3-Clause
# Copyright the MNE-Python contributors.

# As usual, we import everything we need.

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

def multifile(string_array):
    output = np.empty((0, 11), dtype=float)
    events = np.empty((0,  3), dtype=int)
    i = 0
    for file in string_array:
        output = np.concatenate((output, np.genfromtxt(file, delimiter=',')[1:, :]), axis=0)
        temp_events = np.array([[ 1500, 0, 1],
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
        temp_events[:, 0] = temp_events[:, 0] + (i * 72005)
        events = np.concatenate((events, temp_events), axis=0)
        i = i + 1

    return (output, events)
    



#———————————————————————————————————————————————————————————————————————
#np.genfromtxt('MeasurementSubgroup/Our_measurements/Measurement_prompt/EEGdata-2024-144--14-56-37.csv', delimiter=',')
#(allOutputs, events) = multifile(["EEGdata-2024-149--15-20-21.csv", 
#                                  "EEGdata-2024-149--15-35-40.csv",
#                                  "EEGdata-2024-149--15-45-38.csv",
#                                  "EEGdata-2024-149--15-57-42.csv"
#                                  ])
#———————————————————————————————————————————————————————————————————————
#(allOutputs, events) = multifile(["EEGdata-2024-149--16-41-44.csv"])
#———————————————————————————————————————————————————————————————————————
# (allOutputs, events) = multifile(["Data/2/EEGdata-2024-150--14-48-32.csv",
#                                 "Data/2/EEGdata-2024-150--14-55-28.csv",
#                                 "Data/2/EEGdata-2024-150--15-01-30.csv",
#                                 "Data/2/EEGdata-2024-150--15-07-57.csv",
#                                 "Data/2/EEGdata-2024-150--15-14-53.csv",
#                                 "Data/2/EEGdata-2024-150--15-30-23.csv",
#                                 "Data/2/EEGdata-2024-150--15-36-40.csv",
#                                 "Data/2/EEGdata-2024-150--15-42-38.csv"
#                                 ])
#———————————————————————————————————————————————————————————————————————
# (allOutputs, events) = multifile(["EEGdata-2024-156--14-35-07.csv",
#                                  "EEGdata-2024-156--14-42-54.csv",
#                                  "EEGdata-2024-156--14-51-06.csv",
#                                  "EEGdata-2024-156--14-58-57.csv",
#                                  "EEGdata-2024-156--15-06-57.csv"
#                                  ])
#———————————————————————————————————————————————————————————————————————
# (allOutputs, events) = multifile(['Data/3/EEGdata-2024-156--14-35-07.csv',
#                                 'Data/3/EEGdata-2024-156--14-42-54.csv',
#                                 'Data/3/EEGdata-2024-156--14-51-06.csv',
#                                 'Data/3/EEGdata-2024-156--14-58-57.csv',
#                                 'Data/3/EEGdata-2024-156--15-06-57.csv',
#                                 'Data/3/EEGdata-2024-156--15-21-50.csv',
#                                 'Data/3/EEGdata-2024-156--15-27-22.csv'])
#———————————————————————————————————————————————————————————————————————
(allOutputs, events) = multifile(['Data/4/EEGdata-2024-162--11-15-01.csv',
                                'Data/4/EEGdata-2024-162--11-20-53.csv',
                                'Data/4/EEGdata-2024-162--11-28-38.csv',
                                'Data/4/EEGdata-2024-162--11-35-23.csv'])
#———————————————————————————————————————————————————————————————————————
# (allOutputs, events) = multifile(['Data/1/EEGdata-2024-144--14-24-41.csv',
#                                 'Data/1/EEGdata-2024-144--14-47-17.csv',
#                                 'Data/1/EEGdata-2024-144--14-56-37.csv',
#                                 'Data/1/EEGdata-2024-144--15-28-30.csv',
#                                 'Data/1/EEGdata-2024-144--15-54-35.csv'])
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
    picks=('C3',  'Cz',  'C4'),
    baseline=None,
    preload=True,
)

# .. _cnorm-example:
#
# Here we set suitable values for computing ERDS maps. Note especially the
# ``cnorm`` variable, which sets up an *asymmetric* colormap where the middle
# color is mapped to zero, even though zero is not the middle *value* of the
# colormap range. This does two things: it ensures that zero values will be
# plotted in white (given that below we select the ``RdBu`` colormap), and it
# makes synchronization and desynchronization look equally prominent in the
# plots, even though their extreme values are of different magnitudes.

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

"""
for event in event_ids:
    # select desired epochs for visualization
    tfr_ev = tfr[event]
    fig, axes = plt.subplots(
        1, 4, figsize=(12, 4), gridspec_kw={"width_ratios": [10, 10, 10, 1]}
    )
    for ch, ax in enumerate(axes[:-1]):  # for each channel
        # positive clusters
        _, c1, p1, _ = pcluster_test(tfr_ev.data[:, ch], tail=1, **kwargs)
        # negative clusters
        _, c2, p2, _ = pcluster_test(tfr_ev.data[:, ch], tail=-1, **kwargs)

        # note that we keep clusters with p <= 0.05 from the combined clusters
        # of two independent tests; in this example, we do not correct for
        # these two comparisons
        c = np.stack(c1 + c2, axis=2)  # combined clusters
        p = np.concatenate((p1, p2))  # combined p-values
        mask = c[..., p <= 0.05].any(axis=-1)

        # plot TFR (ERDS map with masking)
        tfr_ev.average().plot(
            [ch],
            cmap="RdBu",
            cnorm=cnorm,
            axes=ax,
            colorbar=False,
            show=False,
            mask=mask,
            mask_style="mask",
        )

        ax.set_title(epochs.ch_names[ch], fontsize=10)
        ax.axvline(0, linewidth=1, color="black", linestyle=":")  # event
        if ch != 0:
            ax.set_ylabel("")
            ax.set_yticklabels("")
    fig.colorbar(axes[0].images[-1], cax=axes[-1]).ax.set_yscale("linear")
    fig.suptitle(f"ERDS ({event})")
    plt.show()
"""

# Similar to `~mne.Epochs` objects, we can also export data from
# `~mne.time_frequency.EpochsTFR` and `~mne.time_frequency.AverageTFR` objects
# to a :class:`Pandas DataFrame <pandas.DataFrame>`. By default, the `time`
# column of the exported data frame is in milliseconds. Here, to be consistent
# with the time-frequency plots, we want to keep it in seconds, which we can
# achieve by setting ``time_format=None``:

df = tfr.to_data_frame(time_format=None)
df.head()

# This allows us to use additional plotting functions like
# :func:`seaborn.lineplot` to plot confidence bands:

df = tfr.to_data_frame(time_format=None, long_format=True)

#print(df)
# Map to frequency bands:
freq_bounds = {"_": 0, "delta": 3, "theta": 7, "alpha": 13, "beta": 35, "gamma": 140}
df["band"] = pd.cut(
    df["freq"], list(freq_bounds.values()), labels=list(freq_bounds)[1:]
)

# Filter to retain only relevant frequency bands:
freq_bands_of_interest = ["alpha", "beta"]
df = df[df.band.isin(freq_bands_of_interest)]
df["band"] = df["band"].cat.remove_unused_categories()

# Order channels for plotting:
df["channel"] = df["channel"].cat.reorder_categories(('C3',  'Cz',  'C4'), ordered=True)

df = df.drop(df.index[df['time'].isin([-1.004])], axis=0)

#df.to_csv('MeasurementSubgroup/ERDS_plots/MNE_erds.csv')

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

# References
# ==========
# .. footbibliography::
