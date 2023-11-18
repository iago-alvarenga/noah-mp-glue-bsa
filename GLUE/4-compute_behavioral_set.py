import numpy as np
import xarray as xr
import pandas as pd
from sklearn.metrics import r2_score
import xskillscore

def filter_nan(s,o):
    """
    this functions removed the data  from simulated and observed data
    whereever the observed data contains nan
    
    this is used by all other functions, otherwise they will produce nan as 
    output
    """
    if np.sum(~np.isnan(s*o))>=1:
        data = np.array([s.flatten(),o.flatten()])
        data = np.transpose(data)
        data = data[~np.isnan(data).any(1)]
        s = data[:,0]
        o = data[:,1]
    return s, o

def NS(s,o):
    """
    Nash Sutcliffe efficiency coefficient
    input:
        s: simulated
        o: observed
    output:
        ns: Nash Sutcliffe efficient coefficient
    """
    s,o = filter_nan(s,o)
    return 1 - sum((s-o)**2)/sum((o-np.mean(o))**2)

def correlation(s,o):
    """
    correlation coefficient
    input:
        s: simulated
        o: observed
    output:
        correlation: correlation coefficient
    """
    s,o = filter_nan(s,o)
    if s.size == 0:
        corr = np.NaN
    else:
        corr = np.corrcoef(o, s)[0,1]
        
    return corr

def rmse(s,o):
    """
    Root Mean Squared Error
    input:
        s: simulated
        o: observed
    output:
        rmses: root mean squared error
    """
    s,o = filter_nan(s,o)
    return np.sqrt(np.mean((s-o)**2))

def bias(s,o):
    """
    Bias
    input:
        s: simulated
        o: observed
    output:
        bias: bias
    """
    s,o = filter_nan(s,o)
    return np.mean(s-o)

p25_corr=[]
p50_corr=[]
std_ratio_mean=[]
rmse_all=[]
nse_all=[]

scenarios=range(1,5001,1)


for i in scenarios:
    
    noah_mon = xr.open_dataset("/home/iagoalvarenga/iago/models/HRLDAS/run/GLUE/runs/out_glue_%s.nc"%(str(i)))
    modis = xr.open_dataset('data/modis_lai_2012-2014.nc')
    modis = modis.interp(lat=noah_mon.lat,lon=noah_mon.lon,method='nearest')
    correlation=xr.corr(noah_mon.LAI,modis.lai,dim='time')
    var=modis.lai.var()
    mse=xskillscore.mse(noah_mon.LAI,modis.lai,skipna=True)
    nse=1-(mse/var)
    
    nse=np.array(nse)
    nse_all.append(nse)
      
    
    noah_std=noah_mon.LAI.std(dim='time')
    modis_std=modis.lai.std(dim='time')
    std_ratio=(noah_std/modis_std)-1
    std_mean=std_ratio.mean(dim=['lat','lon'])
    std_ratio_mean.append(std_mean)
      
    p25=correlation.quantile(0.10)
    p25=np.array(p25)
    p25_corr.append(p25)
    
    p50=correlation.quantile(0.50)
    p50=np.array(p50)
    p50_corr.append(p50) 
    
    noah=np.array(noah_mon.LAI)
    noah=np.reshape(noah,(100980))
    modis=np.array(modis.lai)
    modis=np.reshape(modis,(100980))
    rmse_noah=np.array(rmse(noah,modis))
    rmse_all.append(rmse_noah)   
            
p25_corr=pd.DataFrame(p25_corr)
p50_corr=pd.DataFrame(p50_corr)
std_ratio_mean=pd.DataFrame(std_ratio_mean)
rmse_all=pd.DataFrame(rmse_all)
nse_all=pd.DataFrame(nse_all)

obj_func=pd.concat([p25_corr,p50_corr,std_ratio_mean,rmse_all,nse_all],axis=1) 

obj_func.columns = ['p25_corr','p50_corr','std_ratio_mean','rmse','nse_all']
obj_func.index = scenarios


param=pd.read_csv('data/scenarios_lhs.csv') 
param.index=scenarios

obj_func=pd.concat([obj_func, param], axis=1)

filtered=obj_func[(obj_func['nse_all'] > 0.4)]

filtered.to_csv('../data/filtered_lhs.csv', index = True, header=True) 

filtered_lhs=pd.read_csv('../data/filtered_lhs.csv') 

scenarios=list(filtered_lhs['Unnamed: 0'])

datasets = []
for i in scenarios:
    
    noah_mon = xr.open_dataset("/home/iagoalvarenga/iago/models/HRLDAS/run/GLUE/runs/out_glue_%s.nc"%(str(i)))
    datasets.append(noah_mon)

combined = xr.concat(datasets,dim='runs')
combined.coords["runs"] = scenarios

combined.to_netcdf("../data/noah_mon_glue.nc")  