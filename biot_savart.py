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

from utils import create_circle, plot_coil, B_volume, create_rectangle, get_slice
from sympy_utils import create_sympy_circle, create_sympy_rectangle

height, width = 2, 1  # height is like y, width like x
lx, ly, lz = create_circle(5, 'x')
#lx, ly, lz = create_rectangle(height, width, 'x', 0, loc=(-0.5, -1))
plot_coil(lx, ly, lz)


t, x, y, z = smp.symbols('t, x, y, z')

# get l, r, and the separation vector r - l
l = create_sympy_circle(t, 1, 'x')
#ls = create_sympy_rectangle(t, height, width, 'x', 0, loc=(-0.5, -1))

I = 1
R = 1
factor = mu_0 * I / (4 * pi * R)
factor = 1

bbox=(1, -5, -1, 6, 5, 1)
vol_res=(0.5, 0.5, 0.5)

#B_field_1 = factor * B_volume(t, x, y, z, ls[0], upper_lim=1, lower_lim=0, bbox=bbox, vol_res=vol_res)
#B_field_2 = factor * B_volume(t, x, y, z, ls[1], upper_lim=1, lower_lim=0, bbox=bbox, vol_res=vol_res)
#B_field_3 = factor * B_volume(t, x, y, z, ls[2], upper_lim=0, lower_lim=1, bbox=bbox, vol_res=vol_res)
#B_field_4 = factor * B_volume(t, x, y, z, ls[3], upper_lim=0, lower_lim=1, bbox=bbox, vol_res=vol_res)

#B_field = B_field_1 + B_field_2 + B_field_3 + B_field_4

B_field = factor * B_volume(t, x, y, z, l, bbox=bbox, vol_res=vol_res)
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
data = go.Cone(x=xv.ravel(), y=yv.ravel(), z=zv.ravel(),
               u=Bx.ravel(), v=By.ravel(), w=Bz.ravel(),
               colorscale='Inferno', colorbar=dict(title=r'$x^2$'),
               sizemode="absolute", sizeref=20)

layout = go.Layout(title=r'Plot Title',
                     scene=dict(xaxis_title=r'x',
                                yaxis_title=r'y',
                                zaxis_title=r'z',
                                aspectratio=dict(x=1, y=1, z=1),
                                camera_eye=dict(x=1.2, y=1.2, z=1.2)))

fig = go.Figure(data = data, layout=layout)
fig.add_scatter3d(x=lx, y=ly, z=lz, mode='lines',
                  line = dict(color='green', width=10))

fig.write_html('B_field.html')