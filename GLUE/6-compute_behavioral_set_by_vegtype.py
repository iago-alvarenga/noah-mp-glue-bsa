import numpy as np
import xarray as xr
import pandas as pd
import xskillscore
import matplotlib.pyplot as plt

vtype_dic ={'sav':9,
            'wsa':8,
            'gld':10,
            'shr':7}

scenarios=range(1,5001)

df=pd.read_csv('../data/scenarios_lhs.csv') 
df.index=scenarios

for vtype,vtype_code in vtype_dic.items():
    nse_list=[]
    for scenario in scenarios:

        print('------------------')
        print(vtype)
        print(scenario)
        print('------------------')

        model=xr.open_dataset(f"/home/iagoalvarenga/iago/models/HRLDAS/run/GLUE/runs/out_glue_{scenario}.nc")
        obs = xr.open_dataset('../data/modis_lai_2012-2014.nc')
        obs = obs.interp(lat=model.lat,lon=model.lon,method='nearest')

        vegtype=model.IVGTYP
        model=model.LAI
        obs=obs.lai
        
        model=model.where(vegtype==vtype_code)

        var=obs.var()
        mse=xskillscore.mse(model,obs,skipna=True)
        nse=1-(mse/var).values
        nse_list.append(nse)

    df[f'nse_{vtype}']=nse_list

df.to_hdf('..data/filtered_parameters.h5','data')
