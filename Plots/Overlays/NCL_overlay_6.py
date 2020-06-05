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
import cartopy.crs as ccrs
import cartopy.feature as cfeature

import geocat.datafiles as gdf
from geocat.viz import util as gvutil

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
t = tf.t
u = uf.u
v = vf.v
u500 = u500f.u
v500 = v500f.v
time = vf.timestep

# Convert Pa to hPa
p = p/100
# Convert K to F
t = (t - 273.15) * 9/5 + 32

###############################################################################
# Create map:
plt.figure(figsize=(10,8))
proj = ccrs.LambertAzimuthalEqualArea(central_longitude=-100, central_latitude=40)

# Set axis projection
ax = plt.axes(projection=proj)
# Set extent to include roughly the United States
ax.set_extent((-128, -58, 18, 65), crs=ccrs.PlateCarree())
ax.add_feature(cfeature.OCEAN, color='lightblue')
ax.add_feature(cfeature.LAND, color='gray')
ax.add_feature(cfeature.LAKES, color='white')
ax.add_feature(cfeature.COASTLINE)

p.plot.pcolormesh(ax=ax)
plt.show()