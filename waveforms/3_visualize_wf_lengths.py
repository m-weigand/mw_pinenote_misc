#!/usr/bin/env python
import matplotlib.pylab as plt
import pandas as pd
import seaborn as sns

from read_file import waveform_file

sns.set_theme()

wff = waveform_file('02_waveform.img')

temperatures = wff.header()['temperatures']

counts = []
for wf in range(0, 7):
    for temp in temperatures:
        lut = wff.get_lut(wf, temp)
        counts += [(wf, temp, len(lut) / 1024)]

df = pd.DataFrame(counts, columns=['waveform', 'temperature', 'count'])

df['count'] = df['count'].astype(int)
df['waveform'] = df['waveform'].replace({
    0: '0: RESET',
    1: '2: DU',
    2: '4: GC16',
    3: '6: GL16',
    4: '7: GLR16',
    5: '5: GLD16/GCC16',
    6: '1: A2',
    7: '3: DU4',
},
value=None)
table = df.pivot('temperature', 'waveform', 'count')
fig, ax = plt.subplots(figsize=(9, 6))
sns.heatmap(
    table, annot=True, fmt="d", linewidths=.5, ax=ax,
    cbar_kws={
        'label': 'number of phases'
    },
)
ax.set_ylabel('Temperature [degC]')
ax.set_title(
    'Length of waveforms (in phase counts) for different temperatures',
    loc='left',
)
ax.set_xlabel('')
for label in ax.get_xticklabels():
    label.set_ha("right")
    label.set_rotation(45)
fig.tight_layout()
fig.savefig('default_waveform_lengths.jpg', dpi=300)
fig.show()
