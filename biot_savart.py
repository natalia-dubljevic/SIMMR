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

from utils import B_volume, get_slice, B_volume_piecewise, return_coords, plot_coil
from sympy_utils import create_sympy_circle, create_sympy_rectangle
from sympy.plotting import plot3d_parametric_line

piecewise = True

t, x, y, z = smp.symbols('t, x, y, z')
bbox=(1, -5, -1, 6, 5, 1)
vol_res=(0.5, 0.5, 0.5)
radius = 1  # for circles
height, width = 2, 1  # for rectangles

if piecewise is True:
    # get l, the distance from the origin to the wire
    ls = create_sympy_rectangle(t, height, width, 'x', 0, loc=(-0.5, -1))  # loc in y, z coords
    #TODO wrap this all up into a fuction that accepts any number of pieces
    np_fn1 = smp.lambdify(t, ls[0])
    np_fn2 = smp.lambdify(t, ls[1])
    np_fn3 = smp.lambdify(t, ls[2])
    np_fn4 = smp.lambdify(t, ls[3])

    t_range = np.linspace(0, 1, 50)
    x1, y1, z1 = return_coords(np_fn1, t_range)
    x2, y2, z2 = return_coords(np_fn2, t_range)
    x3, y3, z3 = return_coords(np_fn3, t_range)
    x4, y4, z4 = return_coords(np_fn4, t_range)

    plot_coil([x1, x2, x3, x3], [y1, y2, y3, y4], [z1, z2, z3, z4], 'coil.png')

    B_field = B_volume_piecewise(t, x, y, z, ls, [0, 0, 1, 1], [1, 1, 0, 0], bbox=bbox, vol_res=vol_res)

else:
    # get l, the distance from the origin to the wire
    l = create_sympy_circle(t, radius, 'x')
    np_fn = smp.lambdify(t, l)

    t_range = np.linspace(0, np.pi *  2, 50)
    x0, y0, z0 = return_coords(np_fn, t_range)
    plot_coil(x0, y0, z0, 'coil.png')

    B_field = B_volume(t, x, y, z, l, bbox=bbox, vol_res=vol_res)

Bx = B_field[:,:,:,0]
By = B_field[:,:,:,1]
Bz = B_field[:,:,:,2]

B_complex = Bx - 1j * By

x_dim, y_dim, z_dim = np.arange(bbox[0], bbox[3], vol_res[0]), np.arange(bbox[1], bbox[4], vol_res[1]), np.arange(bbox[2], bbox[5], vol_res[2])
xv, yv, zv = np.meshgrid(x_dim, y_dim, z_dim, indexing='ij')

B_slice = get_slice(B_complex, 'z', 0, vol_res=vol_res, bbox=bbox)
x, y = get_slice(xv, 'z', 0, vol_res=vol_res, bbox=bbox), get_slice(yv, 'z', 0, vol_res=vol_res, bbox=bbox)
B_mag = np.abs(B_slice)
B_phase = np.angle(B_slice)

# TODO put this plot in a function
fig, axes = plt.subplots(nrows=1, ncols=2)
axes[0].contourf(x, y, B_mag, levels=20)
axes[0].set_title('Magnitude')
axes[0].set_xlabel('x' + " (cm)")
axes[0].set_ylabel('y' + " (cm)")
axes[1].contourf(x, y, B_phase, levels=20)
axes[1].set_title('Phase')
axes[1].set_xlabel('x' + " (cm)")
axes[1].set_ylabel('y' + " (cm)")
fig.tight_layout()
plt.savefig('mag_phase.png')

Bx_slice = get_slice(Bx, 'z', 0, vol_res=vol_res, bbox=bbox)
By_slice = get_slice(By, 'z', 0, vol_res=vol_res, bbox=bbox)
Bz_slice = get_slice(Bz, 'z', 0, vol_res=vol_res, bbox=bbox)

# TODO put this plot in a function
fig, axes = plt.subplots(nrows=1, ncols=3)
vmin = min(np.min(Bx_slice), np.min(By_slice), np.min(Bz_slice))
vmax = max(np.max(Bx_slice), np.max(By_slice), np.max(Bz_slice))
norm = mpl.colors.Normalize(vmin=vmin, vmax=vmax)

axes[0].contourf(x, y, Bx_slice, levels=20, norm=norm)
axes[0].set_title('Bx')
axes[0].set_xlabel('x' + " (cm)")
axes[0].set_ylabel('y' + " (cm)")
axes[1].contourf(x, y, By_slice, levels=20, norm=norm)
axes[1].set_title('By')
axes[1].set_xlabel('x' + " (cm)")
axes[1].set_ylabel('y' + " (cm)")
axes[2].contourf(x, y, Bz_slice, levels=20, norm=norm)
axes[2].set_title('Bz')
axes[2].set_xlabel('x' + " (cm)")
axes[2].set_ylabel('y' + " (cm)")
fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap='viridis'), cax=None)
fig.tight_layout()
plt.savefig('B_field_components.png')



# Use plotly to make an interactive 3D plot
#data = go.Cone(x=xv.ravel(), y=yv.ravel(), z=zv.ravel(),
#               u=Bx.ravel(), v=By.ravel(), w=Bz.ravel(),
#               colorscale='Inferno', colorbar=dict(title=r'$x^2$'),
#               sizemode="absolute", sizeref=20)
#
#layout = go.Layout(title=r'Plot Title',
#                     scene=dict(xaxis_title=r'x',
#                                yaxis_title=r'y',
#                                zaxis_title=r'z',
#                                aspectratio=dict(x=1, y=1, z=1),
#                                camera_eye=dict(x=1.2, y=1.2, z=1.2)))
#
#fig = go.Figure(data = data, layout=layout)
#fig.add_scatter3d(x=lx, y=ly, z=lz, mode='lines',
#                  line = dict(color='green', width=10))
#
#fig.write_html('B_field.html')