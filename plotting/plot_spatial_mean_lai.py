import numpy as np
import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

noah_out=xr.open_dataset("../data/noah_mon_glue.nc")
modis = xr.open_dataset('../data/modis_lai_2012-2014.nc')
modis = modis.interp(lat=noah_out.lat,lon=noah_out.lon,method='nearest')
spatial_mean=noah_out.LAI.mean(dim=['lat','lon'])
spatial_mean_modis=modis.lai.mean(dim=['lat','lon'])
control=xr.open_dataset("../data/out_glue_control.nc")
spatial_mean_control=control.LAI.mean(dim=['lat','lon'])
median_mean=spatial_mean.median(dim='runs')
p05_mean=spatial_mean.quantile(0.05,dim='runs')
p95_mean=spatial_mean.quantile(0.95,dim='runs')


r_model, p_value = pearsonr(median_mean, spatial_mean_modis)
r_control, p_value = pearsonr(spatial_mean_control, spatial_mean_modis)


fig,ax = plt.subplots(2,1,figsize=(10,8))

month=pd.date_range(start='1/1/2012', periods=36, freq='M')
ax[0].plot(month, spatial_mean_modis, marker='', color='black', linewidth=2,label='MODIS')
ax[0].plot(month, median_mean, marker='', color='black', linewidth=2,linestyle='--',label=f'Median (r = {r_model:{4}.{2}})')
ax[0].fill_between(month,median_mean,p95_mean,color='grey',alpha=0.3)
ax[0].fill_between(month,p05_mean,median_mean,color='grey',alpha=0.3)
ax[0].plot(month, spatial_mean_control, marker='', color='red', linewidth=2,label=f'Control (r = {r_control:{4}.{2}})')
ax[0].set_ylabel('Leaf Area Index',fontsize=12)
ax[0].legend()


noah_out=xr.open_dataset("../data/out_validation.nc")
modis = xr.open_dataset('../data/modis_lai_2001-2007.nc')
modis=modis.sel(time=slice("2001-01-01", "2003-12-31"))
modis = modis.interp(lat=noah_out.lat,lon=noah_out.lon,method='nearest')
latmean=noah_out.LAI.mean(dim='lat')
spatial_mean=latmean.mean(dim='lon')
spatial_mean_median=spatial_mean.median(dim='runs')
latmean_modis=modis.lai.mean(dim='lat')
spatial_mean_modis=latmean_modis.mean(dim='lon')
control=xr.open_dataset("../data/out_glue_control_validation.nc")
latmean_control=control.LAI.mean(dim='lat')
spatial_mean_control=latmean_control.mean(dim='lon')
median_mean=spatial_mean.median(dim='runs')
p05_mean=spatial_mean.quantile(0.05,dim='runs')
p95_mean=spatial_mean.quantile(0.95,dim='runs')
noah_out=xr.open_dataset("../data/out_validation.nc")
median=noah_out.LAI.median(dim='runs')
latmean=noah_out.LAI.mean(dim='lat')
spatial_mean_filt=latmean.mean(dim='lon')
median=noah_out.LAI.median(dim='runs')
p95=noah_out.LAI.quantile(0.95,dim='runs')
p05=noah_out.LAI.quantile(0.05,dim='runs')
latmean=noah_out.LAI.mean(dim='lat')
spatial_mean_filt=latmean.mean(dim='lon')
spatial_mean_median_filt=spatial_mean.median(dim='runs')
spatial_mean_p95_filt=spatial_mean_filt.quantile(0.95,dim='runs')
spatial_mean_p05_filt=spatial_mean_filt.quantile(0.05,dim='runs')

r_model, p_value = pearsonr(median_mean, spatial_mean_modis)

r_control, p_value = pearsonr(spatial_mean_control, spatial_mean_modis)

month=pd.date_range(start='1/1/2001', periods=36, freq='M')
ax[1].plot(month, spatial_mean_modis, marker='', color='black', linewidth=2,label='MODIS')
ax[1].plot(month, median_mean, marker='', color='black', linewidth=2,linestyle='--',label=f'Median (r = {r_model:{4}.{2}})')
ax[1].fill_between(month,median_mean,p95_mean,color='grey',alpha=0.3)
ax[1].fill_between(month,p05_mean,median_mean,color='grey',alpha=0.3)

ax[1].plot(month, spatial_mean_control, marker='', color='red', linewidth=2,label=f'Control (r = {r_control:{4}.{2}})')
ax[1].set_ylabel('Leaf Area Index',fontsize=12)
ax[1].legend()

plt.subplots_adjust(right=0.95,top=0.93,bottom=0.06,left=0.1)
plt.figtext(0.03, 0.94, 'a)', fontsize=14)
plt.figtext(0.03, 0.47, 'b)', fontsize=14)
fig.savefig('../figures/spatial_mean_LAI.jpg', dpi=1000)