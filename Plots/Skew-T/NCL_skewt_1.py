"""
NCL_skewt_1.py
===============
This script illustrates the following concepts:
   - Drawing a default Skew-T background
   - Customizing the background of a Skew-T plot
See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/skewt_1.ncl
    - Original NCL plots: https://www.ncl.ucar.edu/Applications/Images/skewt_1_1_lg.png and https://www.ncl.ucar.edu/Applications/Images/skewt_1_2_lg.png and https://www.ncl.ucar.edu/Applications/Images/skewt_1_3_lg.png
"""

###############################################################################
# Import packages:
import matplotlib.pyplot as plt
import numpy as np
from metpy.plots import SkewT
from metpy.units import units
import geocat.viz.util as gvutil
"""
###############################################################################
# Plot Skew-T with MetPy Defaults:
## Note that there are not labels on the axes. This is because we have not yet
## plotted any data. Once data is plotted, MetPy will use the units of the
## data to create appropriate labels.
fig = plt.figure(figsize=(9, 9))
skew = SkewT(fig)
ax = skew.ax

skew.plot_dry_adiabats()
skew.plot_moist_adiabats()
skew.plot_mixing_lines()

gvutil.set_titles_and_labels(ax, maintitle="MetPy Default Skew-T")
plt.show()
plt.close()
"""
###############################################################################
# Plot Skew-T that is similar to NCL's default Skew-T plot
fig = plt.figure(figsize=(9, 9))
# The rotation keyword changes how skewed the temperature lines are. MetPy has
# a default skew of 30 degrees
skew = SkewT(fig, rotation=45)
ax = skew.ax

# Choose starting temperatures in Kelvin for the dry adiabats
t0 = units.K * np.arange(253.15, 444.15, 10)
skew.plot_dry_adiabats(t0=t0, linestyles='solid', colors='goldenrod', linewidths=1.5)

# Choose starting temperatures in Kelvin for the moist adiabats
t0 = units.K * np.arange(282.15, 306.15, 4)
skew.plot_moist_adiabats(t0=t0, linestyles='solid', colors='lime', linewidth=1.5)

# Choose mixing ratios
w = np.array([0.001, 0.002, 0.003, 0.005, 0.008, 0.012, 0.020]).reshape(-1, 1)

# Choose the range of pressures that the mixing ratio lines are drawn over
p = units.hPa * np.linspace(1000, 400, 7)

# Plot mixing ratio lines
skew.plot_mixing_lines(w=w, p=p, linestyle='dashed', colors='lime', linewidths=1)

gvutil.set_axes_limits_and_ticks(ax=ax, xlim=[-32, 38], yticks=[1000, 850, 700, 500, 400, 300, 250, 200, 150, 100])
gvutil.set_titles_and_labels(ax=ax, maintitle="NCL Style Plot")

plt.show()
