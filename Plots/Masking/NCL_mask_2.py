"""
NCL_mask_2.py
===============
This script illustrates the following concepts:
   - Using keyword zorder to mask areas in a plot
   - Drawing filled land areas on top of a contour plot

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/mask_2.ncl
    - Original NCL plot: https://www.ncl.ucar.edu/Applications/Images/mask_2_lg.png
"""

###############################################################################
# Import packages:
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr

import geocat.datafiles as gdf
from geocat.viz import cmaps as gvcmaps
from geocat.viz import util as gvutil

###############################################################################
# Read in data:

# Open a netCDF data file using xarray default engine and load the data into xarrays
# Disable time decoding due to missing necessary metadata
ds = xr.open_dataset(gdf.get("netcdf_files/atmos.nc"), decode_times=False)

# Extract a slice of the data at first time step
ds = ds.isel(time=0).drop("time")
TS = ds.TS

# Fix the artifact of not-shown-data around 0 and 360-degree longitudes
TS = gvutil.xr_add_cyclic_longitudes(TS, "lon")

##############################################################################
# Plot:

# Generate figure (set its size (width, height) in inches)
fig = plt.figure(figsize=(10, 6))

# Generate axes using Cartopy and draw land masses, coastlines, and lakes
ax = plt.axes(projection=ccrs.PlateCarree())
ax.add_feature(cfeature.LAND, facecolor='lightgray')
ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
ax.add_feature(cfeature.LAKES, linewidth=0.5, edgecolor='black',
               facecolor='None')

# Use geocat.viz.util convenience function to set axes limits & tick values
gvutil.set_axes_limits_and_ticks(ax, xlim=(-180, 180), ylim=(-90,90),
                                 xticks=np.linspace(-180, 180, 13),
                                 yticks=np.linspace(-90, 90, 7))

# Use geocat.viz.util convenience function to add minor and major tick lines
gvutil.add_major_minor_ticks(ax, labelsize=12)

# Use geocat.viz.util convenience function to make latitude, longitude tick labels
gvutil.add_lat_lon_ticklabels(ax)

# Use geocat.viz.util convenience function to add titles
gvutil.set_titles_and_labels(ax, maintitle='Draw land ON TOP of contours',
                             lefttitle=TS.long_name, righttitle=TS.units,
                             lefttitlefontsize=14, righttitlefontsize=14)

plt.show()
