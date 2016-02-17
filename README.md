# BECvis
Contains a number of Python tools to visualize Binary Evolution Code outputs.
Binary Evolution Code (BEC) [Maarten Suijs Astronomical Institute Utrecht].

BECvis currently contains tools to:
- Plot Hertzsprung Russel track of multiple BEC models
- Generate gif visualizing dynamic evolution of BEC model radius, luminosity, and temperature.

# plot1
Plots:  HR diagrams 
        Lt trajectory
        Tt trajectory

from multiple BEC *.plot1 output files at once.

# BEC2gif
Generates gif animated image from BEC *.plot1 output files.
Uses existing gif (of some animated star), and transforms to fit evolution data.
Plots side by side with animated HR diagram.
