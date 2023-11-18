import numpy as np
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import cartopy.crs as ccrs
from cartopy.feature import NaturalEarthFeature, LAND, COASTLINE, ShapelyFeature
import matplotlib
import matplotlib.cm as cm
import cartopy.io.shapereader as shpreader
import xarray as xr
import cmocean
import matplotlib.pyplot as plt
from matplotlib.patches import Path, PathPatch

cmap_rain = cmocean.cm.rain

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


shp=shpreader.Reader('../data/shapes/semiarido_nordestino_single.shp')
shape_feature=ShapelyFeature(shp.geometries(),ccrs.PlateCarree())

caatinga=shpreader.Reader('../data/shapes/caatinga.shp')
caatinga_feature=ShapelyFeature(caatinga.geometries(),ccrs.PlateCarree())


for f in shp.records():
        if f.attributes["nome"] == "Bahia":
            a = (f.geometry)
            x, y = a.exterior.coords.xy
            t = [[(a, s) for a, s in zip(x, y)]]

ds=xr.open_dataset("../data/noah_mon_glue.nc")


grain=xr.open_dataset("out_vars.nc")

precip=xr.open_dataset('precip.mon.ltm.0.25x0.25.v2020.nc')
precip.coords['lon'] = (precip.coords['lon'] + 180) % 360 - 180
precip=precip.sortby(precip.lon)
precip=precip.sortby(precip.lat)
precip=precip.sel(lat=slice(-15.75,-2.25),lon=slice(-46.75,-34.25))
precip=precip.mean(dim='time').precip

lon=np.linspace(-49.875,-30.125, num=80)
lat=np.linspace(-19.875,-0.125, num=80)
grain.coords["lat"] = (("south_north"), lat)
grain.coords["lon"] = (("west_east"), lon)
grain.coords["Times"] = pd.date_range(start='1/1/2001', periods=367, freq='M')
grain=grain.rename({'south_north': 'lat','west_east': 'lon', 'Times': 'time'})
grain=grain.sel(time=slice("2001-01-01", "2001-01-31"))

grain=grain.isel(lon=slice(14,64),lat=slice(14,72))

def rgb2hex(r,g,b):
    return "#{:02x}{:02x}{:02x}".format(r,g,b)

fig=plt.figure(figsize=(13.9,11))

gs=gridspec.GridSpec(2,4)
# gs.update(wspace=0.5)
ax=[1,1,1]
ax[0]=fig.add_subplot(gs[0,:2],projection=ccrs.PlateCarree())
ax[1]=fig.add_subplot(gs[0,2:],projection=ccrs.PlateCarree())
ax[2]=fig.add_subplot(gs[1,1:3],projection=ccrs.PlateCarree())


xticks = [-48, -44, -40, -36, -32]
yticks = [-18,-14, -10, -6, -2]

xticks = [-47,-45, -43, -41,-39, -37, -35]
yticks = [-15,-13, -11,-9, -7, -5,-3]
yticklabels=['{}S'.format(i) for i in yticks]
xticklabels=['{}W'.format(i) for i in xticks]


ax[0].set_title('Vegetation Type',fontsize=14)
ax[1].set_title('Soil Type',fontsize=14)
ax[2].set_title('Annual Precipitation (mm/day)',fontsize=14)


# Barra de cores
veg_custom_map = [rgb2hex(0,100,0), #darkgreen
              rgb2hex(0,175,0), #green
              rgb2hex(151,60,65), #bordeaux
              rgb2hex(228,151,95), #orange
              rgb2hex(255,212,177), #lightorange
              rgb2hex(3,253,3), #lightgreen
              rgb2hex(181,224,251), #n sei
              rgb2hex(168,168,168), #grey
              rgb2hex(248,159,207), #pink
              rgb2hex(244,237,200)] #sand
veg_colormap = matplotlib.colors.ListedColormap(veg_custom_map)
levels = [2,4,6,8,9,10,12,13,14,16,17]
norm = matplotlib.colors.BoundaryNorm(boundaries=levels, ncolors=10)
ax[0].pcolor(grain.lon,grain.lat,grain.IVGTYP[0,:,:],transform=ccrs.PlateCarree(),cmap=veg_colormap,norm=norm)
cbar = fig.colorbar(cm.ScalarMappable(norm=norm,cmap=veg_colormap),ticks=[1,3,5,7,8.5,9.5,11,12.5,13.5,15,16.5],ax=ax[0])
cbar.ax.set_yticklabels(['Evergreen Broad', 'Deciduous Broad', 'Closed Shrublands',
                         'Woody Savannas', 'Savannas','Grasslands','Croplands',
                         'Urban', 'Crop/veg','Barren Land'],fontsize=10)


soil=grain.ISLTYP.where(grain.ISLTYP!=14)

# Barra de cores
soil_custom_map = ["#FCFFC9","#EDD788","#E3A946","#D67500","#AB4A3D","#73243C","#1D0B14"]
soil_colormap = matplotlib.colors.ListedColormap(soil_custom_map)
levels = [1,2,3,6,7,9,12,13]
norm = matplotlib.colors.BoundaryNorm(boundaries=levels, ncolors=8)
ax[1].pcolor(grain.lon,grain.lat,soil[0,:,:],transform=ccrs.PlateCarree(),cmap=soil_colormap,norm=norm)
cbar = fig.colorbar(cm.ScalarMappable(norm=norm,cmap=soil_colormap),ticks=[0.5,1.5,2.5,4.5,6.5,8,10.5,12.5],ax=ax[1])
cbar.ax.set_yticklabels(['Sand', 'Loamy Sand', 'Sandy Loam',
                         'Loam', 'Sandy Clay Loam','Clay Loam','Clay'],fontsize=10)

states = NaturalEarthFeature(category='cultural', scale='50m', facecolor='none',
                                name='admin_1_states_provinces_lines')#estados



levels = [1,2,3,6,7,9,12,13]
norm = matplotlib.colors.Normalize(vmin=0,vmax=3)
ax[2].pcolor(precip.lon,precip.lat,precip,transform=ccrs.PlateCarree(),cmap=cmap_rain)
cbar = fig.colorbar(cm.ScalarMappable(norm=norm,cmap=cmap_rain),ax=ax[2])

states = NaturalEarthFeature(category='cultural', scale='50m', facecolor='none',
                                name='admin_1_states_provinces_lines')



ax[0].add_feature(caatinga_feature,edgecolor='grey',linewidth=1,linestyle='-',facecolor='none')
ax[1].add_feature(caatinga_feature,edgecolor='grey',linewidth=1,linestyle='-',facecolor='none')
ax[2].add_feature(caatinga_feature,edgecolor='grey',linewidth=1,linestyle='-',facecolor='none')

for n in [0,1,2]:
    ax[n].gridlines(xlocs=xticks, ylocs=yticks,alpha=0.3)
    ax[n].set_xticks(xticks)
    ax[n].set_xticklabels(xticklabels, fontsize=10)
    ax[n].set_yticks(yticks)
    ax[n].set_yticklabels(yticklabels, fontsize=10)
    cut2shapefile(ax[n], t)
    ax[n].coastlines(alpha=1)   
    ax[n].add_feature(states, edgecolor='black', alpha=1,linestyle='-')#estados
    ax[n].add_feature(shape_feature,edgecolor='black',linewidth=1,linestyle='-',facecolor='none')
     #sab


fig.text(0.03,0.96,'a)',weight='bold',fontsize=13)
fig.text(0.52,0.96,'b)',weight='bold',fontsize=13)
fig.text(0.26,0.47,'c)',weight='bold',fontsize=13)

fig.subplots_adjust(left=0,right=0.94,bottom=0.03,top=0.95,hspace=0.15)
plt.savefig ('studyarea.jpg', dpi=1000)

print(grain.variables)