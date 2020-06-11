"""
NCL_overlay_6.py
===============
This script illustrates the following concepts:
   - Overlaying shaded contours on filled contours
   - Filling contours with multiple shaded patterns
   - Overlaying vectors on filled contours
   - Using the "palette" resources to assign a color palette to color vectors and contours

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/overlay_6.ncl
    - Original NCL plots: https://www.ncl.ucar.edu/Applications/Images/overlay_6_lg.png
"""

###############################################################################
# Import packages:
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.colors as mcolors
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import cartopy.crs as ccrs
import cartopy.feature as cfeature

import geocat.datafiles as gdf
from geocat.viz import util as gvutil
from geocat.viz import cmaps as gvcmaps

###############################################################################
# Read in data:

# Open a netCDF data file using xarray default engine and load the data into xarrays
uf = xr.open_dataset(gdf.get("netcdf_files/Ustorm.cdf"))
vf = xr.open_dataset(gdf.get("netcdf_files/Vstorm.cdf"))
pf = xr.open_dataset(gdf.get("netcdf_files/Pstorm.cdf"))
tf = xr.open_dataset(gdf.get("netcdf_files/Tstorm.cdf"))
u500f = xr.open_dataset(gdf.get("netcdf_files/U500storm.cdf"))
v500f = xr.open_dataset(gdf.get("netcdf_files/V500storm.cdf"))

p = pf.p.isel(timestep=0).drop('timestep')
t = tf.t.isel(timestep=0).drop('timestep')
u = uf.u.isel(timestep=0).drop('timestep')
v = vf.v.isel(timestep=0).drop('timestep')
u500 = u500f.u.isel(timestep=0).drop('timestep')
v500 = v500f.v.isel(timestep=0).drop('timestep')
time = vf.timestep

# Convert Pa to hPa
p = p/100
# Convert K to F
t = (t - 273.15) * 9/5 + 32

###############################################################################
# Create map:
fig = plt.figure(figsize=(8,7))
proj = ccrs.LambertAzimuthalEqualArea(central_longitude=-100, central_latitude=40)

# Set axis projection
ax = plt.axes([0, 0.2, 0.8, 0.7], projection=proj)
cax1 = inset_axes(ax, width='5%', height='100%', loc='lower right',
                   bbox_to_anchor=(0.125, 0, 1, 1),
                   bbox_transform=ax.transAxes,
                   borderpad=0)

cax2 = inset_axes(ax, width='100%', height='7%', loc='lower left',
                   bbox_to_anchor=(0, -0.15, 1, 1),
                   bbox_transform=ax.transAxes,
                   borderpad=0)
cax2.xaxis.set_label_position('top')
# Set extent to include roughly the United States
transparent = (0, 0, 0, 0) # RGBA value for a transparent color
ax.set_extent((-128, -58, 18, 65), crs=ccrs.PlateCarree())
ax.add_feature(cfeature.OCEAN, color='lightskyblue', zorder=0)
ax.add_feature(cfeature.LAND, color='silver', zorder=1)
ax.add_feature(cfeature.LAKES, linewidth=0.5, edgecolor='black', facecolor=transparent, zorder=3)
ax.add_feature(cfeature.COASTLINE, linewidth=0.5, zorder=3)

# Import color mab for pressure level contour
p_cmap = gvcmaps.StepSeq25
pressure = p.plot.contourf(ax=ax, transform=ccrs.PlateCarree(), cmap=p_cmap, levels=np.arange(975, 1050, 5), add_colorbar=False, add_labels=False, zorder=2)
plt.colorbar(pressure, cax=cax1, ticks=np.arange(980, 1045, 5))
cax1.yaxis.set_label_text(label='\n'.join('Sea Level Pressure'), fontsize=14, rotation=0)#, position=(0,0.1))
cax1.yaxis.set_label_coords(-0.5, 0.9)

# Add streamline overlay
ax.streamplot(u500.lon, u500.lat, u500.data, v500.data, transform=ccrs.PlateCarree(), color='black', arrowstyle='->', linewidth=0.5, density=2, zorder=4)

# Add vector grid
# First thin the data the the vector grid is less cluttered
x = u['lon'].data[0:36:2]
y = u['lat'].data[0:33:2]
u = u.data[0:33:2,0:36:2]
v = v.data[0:33:2,0:36:2]
t = t.data[0:33:2,0:36:2]

# Import color map for vectors
wind_cmap = gvcmaps.amwg_blueyellowred
bounds = np.arange(-30,120,10)
norm = mcolors.BoundaryNorm(bounds, wind_cmap.N)

Q = ax.quiver(x, y, u, v, t, transform=ccrs.PlateCarree(), zorder=5, headwidth=5, cmap=wind_cmap, norm=norm)
plt.colorbar(Q, cax=cax2, ticks=np.arange(-20,110,10), norm=norm, orientation='horizontal')
cax2.xaxis.set_label_text(label='Surface Temperature', fontsize=14)
cax2.xaxis.set_label_position('top')

ax.quiverkey(Q, 0.925, 0.025, 20, label='20', zorder=5)
ax.add_patch(mpatches.Rectangle(xy=[0.85, 0], width=0.15, height=0.0925, facecolor='white', transform=ax.transAxes, zorder=4))

# Add title
ax.set_title('January 1996 Snow Storm\n1996 01 05 00:00 + 0', fontweight='bold', fontsize=16)
plt.show()
