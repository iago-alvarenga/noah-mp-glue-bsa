import pandas as pd
import seaborn as sns; sns.set()
import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
import xskillscore

dic_var={'vcmx':'VCMX',
         'rmf' :'RMF25',
         'ltovrc':'LTOVRC',
         'sla':'SLA',
         'dilefw':'DILEFW',
         'bb_frac':'BB',
         'smcmax_frac':'SMCMAX',
         'reffrac':'SMCREF',
         'wltfrac':'SMCWLT'}

months=['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']
variables=['vcmx','rmf','ltovrc','sla','dilefw','bb_frac','smcmax_frac','reffrac','wltfrac']

fig, ax = plt.subplots(9,1,figsize=(6,10),sharex=True)

for n,var in enumerate(variables):
    median_list=[]
    p25_list=[]
    p75_list=[]
    for mon in months:
        df=pd.read_csv('../data/filtered_csv_nse_{}.csv'.format(mon))
        df=df[var]
        median=df.median()
        p75=df.quantile(0.75)
        p25=df.quantile(0.25)
        median_list.append(median)
        p25_list.append(p25)
        p75_list.append(p75)
    
    ax[n].plot(months,median_list,color='darkgreen')
    ax[n].fill_between(months,p25_list,p75_list,alpha=0.3,color='darkgreen')
    ax[n].set_title(dic_var[var])
fig.tight_layout()
fig.savefig('../figures/season_param_distr.jpg',dpi=1000)

