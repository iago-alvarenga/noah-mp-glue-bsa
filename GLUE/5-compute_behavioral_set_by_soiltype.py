import numpy as np
import xarray as xr
import pandas as pd
import xskillscore
import matplotlib.pyplot as plt

stype_dic ={'sandyloam':3,
            'loam':6,
            'sandyclay':7,
            'clayloam':9}

scenarios=range(1,5001)

df=pd.read_csv('../data/scenarios_lhs.csv') 
df.index=scenarios

for stype,stype_code in stype_dic.items():
    nse_list=[]
    for scenario in scenarios:

        print('------------------')
        print(stype)
        print(scenario)
        print('------------------')

        model=xr.open_dataset(f"/home/iagoalvarenga/iago/models/HRLDAS/run/GLUE/runs/out_glue_{scenario}.nc")
        soil=xr.open_dataset('HRLDAS_setup_2011010100_d1')
        soil=soil.ISLTYP

        soil=soil[0,:,:].values


        soil = xr.DataArray(data=soil,
            coords={"lat": (["lat"], model.lat.values),
                    "lon": (["lon"], model.lon.values)},
            dims=["lat","lon"])

        soil=soil.where(model.LAI[0,:,:]>0)

        soil=soil.where(soil!=1)
        soil=soil.where(soil!=2)
        soil=soil.where(soil!=12)
     
        obs = xr.open_dataset('../data/modis_lai_2012-2014.nc')
        obs = obs.interp(lat=model.lat,lon=model.lon,method='nearest')

        soiltype=soil
        model=model.LAI
        obs=obs.lai
        
        model=model.where(soiltype==stype_code)

        # calculate NSE
        var=obs.var()
        mse=xskillscore.mse(model,obs,skipna=True)
        nse=1-(mse/var).values
        nse_list.append(nse)

    df[f'nse_{stype}']=nse_list

df.to_hdf('../data/filtered_parameters_soil.h5','data')
