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

piecewise = False

t, x, y, z = smp.symbols('t, x, y, z')
bbox=(1, -5, -1, 6, 5, 1)
vol_res=(0.5, 0.5, 0.5)
radius = 1  # for circles
height, width = 2, 1  # for rectangles

if piecewise is True:
    # get l, the distance from the origin to the wire
    ls = create_sympy_rectangle(t, height, width, 'x', 0, loc=(-0.5, -1), 
                                rotate_axis='x', rotate_angle=smp.pi/2)  # loc in y, z coords
    #TODO wrap this all up into a fuction that accepts any number of piecwise components
    #np_fn1 = smp.lambdify(t, ls[0])
    #np_fn2 = smp.lambdify(t, ls[1])
    #np_fn3 = smp.lambdify(t, ls[2])
    #np_fn4 = smp.lambdify(t, ls[3])
#
    t_range = np.linspace(0, 1, 50)
    #x1, y1, z1 = return_coords(np_fn1, t_range)
    #x2, y2, z2 = return_coords(np_fn2, t_range)
    #x3, y3, z3 = return_coords(np_fn3, t_range)
    #x4, y4, z4 = return_coords(np_fn4, t_range)
    xs, ys, zs = return_coords(ls, t, t_range)

    plot_coil(xs, ys, zs, 'coil.png')

    B_field = B_volume_piecewise(t, x, y, z, ls, [1, 1, 0, 0], [0, 0, 1, 1], 
                                 bbox=bbox, vol_res=vol_res)

else:
    # get l, the distance from the origin to the wire
    l = create_sympy_circle(t, radius, 'x')

    t_range = np.linspace(0, np.pi *  2, 50)
    xs, ys, zs = return_coords([l], t, t_range)
    plot_coil(xs, ys, zs, 'coil.png')

    B_field = B_volume(t, x, y, z, l, 0, 2*np.pi, bbox=bbox, vol_res=vol_res)

B_complex = B_field[:,:,:,0] - 1j * B_field[:,:,:,1]

plot_mag_phase(B_complex, 'z', 0, vol_res=vol_res, bbox=bbox)
plot_fields(B_field, 'z', 0, vol_res=vol_res, bbox=bbox)
