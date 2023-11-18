import numpy as np
import os
import xarray as xr
import pandas as pd

scenarios=range(1,5001,1)

for i in scenarios:
    
    os.chdir('/home/iagoalvarenga/iago/models/HRLDAS/run/')
    file='param_file_%s.txt'%(str(i))
    print(file)
    test=('cp' + ' ' + 'scenarios_lhs/' + file + ' ' + 'MPTABLE.TBL')
    os.system(test)
    file2='soil_param_file_%s.txt'%(str(i))
    test2=('cp' + ' ' + 'scenarios_lhs/' + file2 + ' ' + 'SOILPARM.TBL')
    os.system(test2)
    os.system('./hrldas.exe')
    os.system("cdo selvar,LAI,IVGTYP output_files/2012010100.LDASOUT_DOMAIN1 out.nc")
    os.system('mv out.nc output_files/out.nc')

    # Abrir Noah

    noah_out=xr.open_dataset("/home/iagoalvarenga/iago/models/HRLDAS/run/output_files/out.nc")
    lon=np.linspace(-46.75,-34.25, num=51)
    lat=np.linspace(-15.75,-2.25, num=55)
    noah_out.coords["lat"] = (("south_north"), lat)
    noah_out.coords["lon"] = (("west_east"), lon)
    noah_out.coords["Times"] = pd.date_range(start='1/1/2012', periods=1096, freq='D')
    noah_out=noah_out.rename({'south_north': 'lat','west_east': 'lon', 'Times': 'time'})
    noah_out=noah_out.sel(time=slice("2012-01-01", "2014-12-31"))
    noah_out=noah_out.where(noah_out.LAI > -999)
    noah_mon=noah_out.resample(time="1MS").mean(dim="time")
    noah_mon.coords["time"] = pd.date_range(start='1/1/2012', periods=36, freq='M')
        
    mask=xr.open_dataset("../data/semiarido_shp.nc")
    mask=xr.concat([mask,mask,mask,mask,mask,mask,mask,mask,mask,mask,mask,mask],dim="time")
    mask=xr.concat([mask,mask,mask],dim="time")
    mask.coords["time"] = pd.date_range(start='1/1/2012', periods=36, freq='M')
    mask=mask.interp(lat=noah_mon.lat,lon=noah_mon.lon,method='nearest')

    # Mascarar

    noah_mon=noah_mon.where(mask.mask > 0)
    noah_mon=noah_mon.where(noah_mon.IVGTYP != 2)
    noah_mon=noah_mon.where(noah_mon.IVGTYP != 4)
    noah_mon=noah_mon.where(noah_mon.IVGTYP != 14)
    noah_mon=noah_mon.where(noah_mon.IVGTYP != 21)
    noah_mon.drop(labels='IVGTYP')
    
    noah_mon.to_netcdf("/home/iagoalvarenga/iago/models/HRLDAS/run/GLUE/runs/out_glue_%s.nc"%(str(i))) 