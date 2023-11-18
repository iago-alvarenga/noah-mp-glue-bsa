import xskillscore as xs
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.feature import NaturalEarthFeature, LAND, COASTLINE, ShapelyFeature
import matplotlib.colors as mcolors
from matplotlib.cm import get_cmap
import matplotlib
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import cartopy.io.shapereader as shpreader
import xarray as xr
import glob2
import glob
import cmocean
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.pyplot as plt
from matplotlib.patches import Path, PathPatch


def cut2shapefile(plot_obj, shape_obj):
     
    """
    plot_obj: axis where plot is being made. ex: ax
    shape_obj: basemap shapefile. ex: m.nordeste_do_brasil when shape is read with m.readshapefile(path/to/nordeste_do_brasil, nordeste_do_brasil)
    """
 
    x0,x1 = plot_obj.get_xlim()
    y0,y1 = plot_obj.get_ylim()
     
    edges = [(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)]
    edge_codes = [Path.MOVETO] + (len(edges) - 1) * [Path.LINETO]
     
    verts = shape_obj[0] + [shape_obj[0][0]]
    codes = [Path.MOVETO] + (len(verts) - 1) * [Path.LINETO]
     
    path = Path(verts+edges, codes+edge_codes)
 
    patch = PathPatch(path, facecolor='white', lw=0)
    plot_obj.add_patch(patch)


shp=shpreader.Reader('../data/semiarido_nordestino_single.shp')
shape_feature=ShapelyFeature(shp.geometries(),ccrs.PlateCarree())


for f in shp.records():
        if f.attributes["nome"] == "Bahia":
            a = (f.geometry)
            x, y = a.exterior.coords.xy
            t = [[(a, s) for a, s in zip(x, y)]]

noah_out=xr.open_dataset("../data/noah_mon_glue.nc")
noah_out=noah_out.where(noah_out.IVGTYP.isin([7,8,9,10]))


control_out=xr.open_dataset("../data/out_glue_control.nc")
control_out=control_out.where(control_out.IVGTYP.isin([7,8,9,10]))


modis = xr.open_dataset('../data/modis_lai_2012-2014.nc')
modis = modis.interp(lat=noah_out.lat,lon=noah_out.lon,method='nearest')
correlation=xr.corr(noah_out.LAI,modis.lai,dim='time')
mean_corr=correlation.mean(dim='runs')
correlation_control=xr.corr(control_out.LAI,modis.lai,dim='time')

var=modis.lai.var(dim='time')
mse=xs.mse(noah_out.LAI,modis.lai,dim='time',skipna=True)
rmse=xs.rmse(noah_out.LAI,modis.lai,dim='time',skipna=True)
nse=1-(mse/var)
nse=nse.mean(dim='runs')
rmse=rmse.mean(dim='runs')
var=modis.lai.var(dim='time')
mse_control=xs.mse(control_out.LAI,modis.lai,dim='time',skipna=True)
rmse_control=xs.rmse(control_out.LAI,modis.lai,dim='time',skipna=True)
nse_control=1-(mse_control/var)

dif=rmse-rmse_control

# Plotar figuras
cmap_rain = cmocean.cm.matter
levels = [0, 0.2, 0.4, 0.8, 1, 1.2, 1.5,2,2.5,3]

xticks = [-46, -44,-42, -40, -38, -36]
yticks = [-14,-12, -10, -8, -6, -4]
states = NaturalEarthFeature(category='cultural', scale='50m', facecolor='none',
                                name='admin_1_states_provinces_lines')#estados
norm = matplotlib.colors.BoundaryNorm(boundaries=levels,ncolors=280)



fig, ax = plt.subplots(1,3,figsize=(8,3.5),subplot_kw={'projection':ccrs.PlateCarree()})

ax[0].set(title='GLUE mean RMSE (t)')
ax[0].coastlines(alpha=1)
ax[0].add_feature(states, edgecolor='black', linewidth=0.5) #estados
ax[0].add_feature(shape_feature,edgecolor='black',linewidth=1,linestyle='-',facecolor='none') #sab
ax[0].contourf(rmse.lon,rmse.lat,rmse,transform=ccrs.PlateCarree(),cmap=cmap_rain,norm=norm,levels=levels,zorder=1)
ax[0].gridlines(xlocs=xticks, ylocs=yticks,alpha=0.3)
ax[0].set_xticks(xticks)
ax[0].set_xticklabels(['48W', '44W', '42W', '40W', '38W','36W'],fontsize=9)
ax[0].set_yticks(yticks)
ax[0].set_yticklabels(['14S','12S', '10S','8S', '6S', '4S'],fontsize=9)

cut2shapefile(ax[0], t)

ax[1].contourf(rmse.lon,rmse.lat,rmse_control,transform=ccrs.PlateCarree(),cmap=cmap_rain,norm=norm,levels=levels)
ax[1].set(title='Control run RMSE (t)')
ax[1].coastlines(alpha=1)
ax[1].add_feature(states, edgecolor='black', linewidth=0.5) #estados
ax[1].add_feature(shape_feature,edgecolor='black',linewidth=1,linestyle='-',facecolor='none') #sab
ax[1].gridlines(xlocs=xticks, ylocs=yticks,alpha=0.5)
ax[1].set_xticks(xticks)
ax[1].set_xticklabels(['48W', '44W', '42W', '40W', '38W','36W'],fontsize=9)
ax[1].set_yticks(yticks)
ax[1].set_yticklabels(['14S','12S', '10S','8S', '6S', '4S'],fontsize=9)
cut2shapefile(ax[1], t)
cax=plt.axes([0.09,0.07,0.51,0.040])
fig.colorbar(matplotlib.cm.ScalarMappable(norm=norm,cmap=cmap_rain),ax=ax[1],cax=cax,orientation='horizontal')



cmap_rain = cmocean.cm.balance

levels = [-1.5,-1,-0.5,0.5,1,1.5]

xticks = [-46, -44,-42, -40, -38, -36]
yticks = [-14,-12, -10, -8, -6, -4]
states = NaturalEarthFeature(category='cultural', scale='50m', facecolor='none',
                                name='admin_1_states_provinces_lines')#estados

norm=mcolors.Normalize(vmin=-2,vmax=2)
colors = ("#008455","#008E62","#009870","#00A17E","#35AB8C","#5CB59A","#79BFA8","#93C9B6","#ACD3C4","#C3DDD3","#DAE7E2","#F1F1F1","#EDE1E3","#E9D1D5","#E5C1C8","#E0B2BB","#DBA2AE","#D693A1","#D08394","#CA7487","#C3647B","#BC536E","#B54262")

ax[2].contourf(rmse.lon,rmse.lat,dif,transform=ccrs.PlateCarree(),cmap='seismic',norm=norm)
ax[2].set(title='GLUE minus Control run')
ax[2].coastlines(linewidth=1)
ax[2].add_feature(states, edgecolor='black', linewidth=0.5) #estados
ax[2].add_feature(shape_feature,edgecolor='black',linewidth=1,linestyle='-',facecolor='none') #sab
ax[2].gridlines(xlocs=xticks, ylocs=yticks,alpha=0.5)
ax[2].set_xticks(xticks)
ax[2].set_xticklabels(['48W', '44W', '42W', '40W', '38W','36W'],fontsize=9)
ax[2].set_yticks(yticks)
ax[2].set_yticklabels(['14S','12S', '10S','8S', '6S', '4S'],fontsize=9)
cut2shapefile(ax[2], t)
cax=plt.axes([0.725,0.07,0.22,0.040])
fig.colorbar(matplotlib.cm.ScalarMappable(cmap='seismic',norm=norm),ax=ax[2],cax=cax,orientation='horizontal')

fig.text(0.03,0.95,'a)',weight='bold')
fig.text(0.355,0.95,'b)',weight='bold')
fig.text(0.6,0.95,'c)',weight='bold')

fig.subplots_adjust(top=1,bottom=0.1,left=0.05,right=0.97)
fig.savefig('../figures/rmse_glue_mean.jpg', dpi=1000)

