"""
NCL_polyg_14.py
================
This script illustrates the following concepts:
    - Drawing polylines and markers using great circle paths
    - Using geographiclib to calculate a great circle path
    - Attaching polylines and markers to a map plot
    
See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/polyg_14.ncl
    - Original NCL plot: https://www.ncl.ucar.edu/Applications/Images/polyg_14_2_lg.png
                         https://www.ncl.ucar.edu/Applications/Images/polyg_14_1_lg.png
"""


###############################################################################

# Import packages:
import numpy as np
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import cartopy.feature as cfeature
from geographiclib.geodesic import Geodesic

from geocat.viz import util as gvutil

###############################################################################
#Plot

def Plot(color, ext, xext, yext, title, style, pt):

    plt.figure(figsize=(8,8))
    ax = plt.axes(projection=ccrs.PlateCarree())

    ax.set_extent(ext, ccrs.PlateCarree())
    ax.add_feature(cfeature.LAND, color='lightgrey')

    plt.plot(xext, yext, style, color= color,  transform=ccrs.Geodetic())

    # This gets geodesic between the two points
    # WGS84 ellipsoid is used
    # yext and xext refer to the start and stop points for the curve
    # [0] being start, [1] being stop
   
    gl = Geodesic.WGS84.InverseLine(yext[0],xext[0], yext[1], xext[1])
    num_points = 10

    # Compute points on the geodesic, and plot them 
    # gl.s13 is the total length of the geodesic
    # the points are equally spaced by 'true distance', but visually 
    # there is a slight distortion due to curvature/projection style 

    for ea in np.linspace(0, gl.s13, num_points):
        g = gl.Position(ea, Geodesic.STANDARD | Geodesic.LONG_UNROLL)
        print("{:.0f} {:.5f} {:.5f} {:.5f}".format(g['s12'], g['lat2'], g['lon2'], g['azi2']))
        lon2 = g['lon2']
        lat2 = g['lat2']
        ax.plot(lon2, lat2, pt, transform=ccrs.PlateCarree())


   # Use geocat.viz.util convenience function to set axes parameters without calling several matplotlib functions
    # Set axes limits, and tick values
    gvutil.set_axes_limits_and_ticks(
    ax,
    xlim=(-125,-60),
    ylim=(15,65),
    xticks=np.linspace(-180, 180, 13),
    yticks=np.linspace(0, 80, 5))

    # Use geocat.viz.util convenience function to make plots look like NCL plots by using latitude, longitude tick labels
    gvutil.add_lat_lon_ticklabels(ax)
    
    # Use geocat.viz.util convenience function to add minor and major tick lines
    gvutil.add_major_minor_ticks(ax, labelsize=12)

    # Use geocat.viz.util convenience function to set titles and labels without calling several matplotlib functions
    gvutil.set_titles_and_labels(
        ax,
        maintitle=title,
        maintitlefontsize=16,
        righttitlefontsize=14,
        xlabel="",
        ylabel="")


# plot first color map
Plot("blue", [-125,-60,15,65],[-120, -64], [20, 60], "1st method: Two Points and Great Circle Path", '-', 'blue')

# plot second color map
Plot("red", [-125,-60,15,65], [-120, -64], [20, 60], "2nd method: Two Points and Great Circle Path", '-', 'ko')


