import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad
import plotly.graph_objects as go
from IPython.display import HTML
import matplotlib as mpl
from scipy.constants import mu_0, pi
import sympy as smp
from sympy.vector import cross
from skimage.restoration import unwrap_phase

from utils import B_volume, get_slice, B_volume_piecewise, return_coords
from sympy_utils import create_sympy_circle, create_sympy_rectangle
from plot_utils import plot_coil, plot_mag_phase, plot_fields
from sympy.plotting import plot3d_parametric_line

piecewise = True # toggle for shape type (shape plot requiring piecewise function vs not requiring piecewise function)

t, x, y, z = smp.symbols('t, x, y, z') # correspond to parametrization variable, x-coord, y-coord, and z-coord, respectively

bbox = (1, -5, -1, 6, 5, 1) # set bounding box; min and max of each of x, y, and z-coords ("frame" of magnetic field)
vol_res = (0.5, 0.5, 0.5) # volume resolution; "granularity" of map
radius = 0.5  # for circles (coil shape)
height, width = 1, 2  # for rectangles (coil shape)

if piecewise is True: # e.g., square, rectangle, etc. coil shape
    # get l, the distance from the origin to the wire
    ls = create_sympy_rectangle(t, height, width, 'x', 0, loc=(-0.5, -1), 
                                rotate_axis='x', rotate_angle=smp.pi/2)  # loc in y, z coords
    t_range = np.linspace(0, 1, 50) # define range of t for parameterization 
    xs, ys, zs = return_coords(ls, t, t_range) # get coil coords in bbox
    plot_coil(xs, ys, zs, 'coil.png') # plot the coil in bbox

    B_field = B_volume_piecewise(t, x, y, z, ls, [1, 1, 0, 0], [0, 0, 1, 1], 
                                 bbox=bbox, vol_res=vol_res)

else: # e.g., circle, ellipse, etc. coil shape
    # get l, the distance from the origin to the wire
    l = create_sympy_circle(t, radius, 'x')

    t_range = np.linspace(0, np.pi *  2, 50)
    xs, ys, zs = return_coords([l], t, t_range)
    plot_coil(xs, ys, zs, 'coil.png')

    B_field = B_volume(t, x, y, z, l, 0, 2*np.pi, bbox=bbox, vol_res=vol_res)

B_complex = B_field[:, :, :, 0] - 1j * B_field[:, :, :, 1]


slice = 'z'
slice_loc = 0

plot_mag_phase(B_complex, slice, slice_loc, vol_res=vol_res, bbox=bbox)
plot_fields(B_field, slice, slice_loc, vol_res=vol_res, bbox=bbox)
