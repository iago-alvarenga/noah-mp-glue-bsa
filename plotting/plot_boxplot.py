import numpy as np
import os
import matplotlib.pyplot as plt
import pandas as pd


filtered_lhs=pd.read_csv('../data/filtered_lhs.csv') 

fig, ax = plt.subplots(1,9,figsize=(15,5))

ax[0].set_title('VCMX25')
ax[0].set_ylim(10, 100)
#ax[0].set_xlim(0.8, 1.2)
#ax[0].set_aspect(0.023)
ax[0].boxplot(filtered_lhs['vcmx'],labels=[''],widths = 0.3)
ax[0].set_ylabel('Parameter value',fontsize=12)

ax[1].set_title('RMF25')
ax[1].set_ylim(0, 3)
#ax[1].set_xlim(0.8, 1.2)
#ax[1].set_aspect(0.67)
ax[1].boxplot(filtered_lhs['rmf'],labels=[''],widths = 0.3)

ax[2].set_title('DILEFW')
ax[2].set_ylim(0, 1)
#ax[2].set_xlim(0.8, 1.2)
#ax[2].set_aspect(2)
ax[2].boxplot(filtered_lhs['dilefw'],labels=[''],widths = 0.3)

ax[3].set_title('LTOVRC')
ax[3].set_ylim(0, 2)
#ax[3].set_xlim(0.8, 1.2)
#ax[3].set_aspect(1)
ax[3].boxplot(filtered_lhs['ltovrc'],labels=[''],widths = 0.3)

ax[4].set_title('SLA')
ax[4].set_ylim(10, 90)
#ax[4].set_xlim(0.8, 1.2)
#ax[4].set_aspect(0.025)
ax[4].boxplot(filtered_lhs['sla'],labels=[''],widths = 0.3)

ax[5].set_title('SMCMAX')
ax[5].set_ylim(0, 1)
#ax[5].set_xlim(0.8, 1.2)
#ax[5].set_aspect(2)
ax[5].boxplot(filtered_lhs['smcmax_frac'],labels=[''],widths = 0.3)

ax[6].set_title('SMCREF')
ax[6].set_ylim(0, 1)
#ax[6].set_xlim(0.8, 1.2)
#ax[6].set_aspect(2)
ax[6].boxplot(filtered_lhs['reffrac'],labels=[''],widths = 0.3)

ax[7].set_title('SMCWLT')
ax[7].set_ylim(0, 1)
#ax[7].set_xlim(0.8, 1.2)
#ax[7].set_aspect(2)
ax[7].boxplot(filtered_lhs['wltfrac'],labels=[''],widths = 0.3)

ax[8].set_title('BB')
ax[8].set_ylim(0, 1)
#ax[8].set_xlim(0.8, 1.2)
#ax[8].set_aspect(2)
ax[8].boxplot(filtered_lhs['bb_frac'],labels=[''],widths = 0.3)


fig.tight_layout()
fig.savefig('../figures/boxplot_glue.jpg', dpi=1000)
