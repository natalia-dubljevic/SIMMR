import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad
import plotly.graph_objects as go
from IPython.display import HTML
import sympy as smp
from sympy.vector import cross
from skimage.restoration import unwrap_phase

from utils import create_circle, plot_coil, B_volume
from sympy_utils import create_sympy_circle


lx, ly, lz = create_circle(1, 'x')
plot_coil(lx, ly, lz)


t, x, y, z = smp.symbols('t, x, y, z')

# get l, r, and the separation vector r - l
l = create_sympy_circle(t, 5, 'x')
# in theory a rectangle, but the derivative is undefined
# l = smp.Matrix([smp.functions.Abs(smp.cos(t)) * smp.cos(t) + smp.functions.Abs(smp.sin(t)) * smp.sin(t),
#                 smp.functions.Abs(smp.cos(t)) * smp.cos(t) - smp.functions.Abs(smp.sin(t)) * smp.sin(t),
#                 0])
B_field = B_volume(t, x, y, z, l)
Bx = B_field[:,:,:,0]
By = B_field[:,:,:,1]
Bz = B_field[:,:,:,2]

Bx[Bx>20] = 20
By[By>20] = 20
Bz[Bz>20] = 20

Bx[Bx<-20] = -20
By[By<-20] = -20
Bz[Bz<-20] = -20

Bx_slice = Bx[:, :, 10]
By_slice = By[:, :, 10]
Bz_slice = Bz[:, :, 10]
B_slice = Bx[:, :, 10] - 1j * By[:, :, 10]


x, y, z = np.linspace(5, 10, 5), np.linspace(-10, 10, 21), np.linspace(-10, 10, 21)
xv, yv, zv = np.meshgrid(x, y, z, indexing='ij')
x, y = xv[:, :, 10], yv[:, :, 10]
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


fig, axes = plt.subplots(nrows=1, ncols=3)
axes[0].contourf(x, y, Bx_slice, levels=20)
axes[0].set_title('Bx')
axes[0].set_xlabel('x' + " (cm)")
axes[0].set_ylabel('y' + " (cm)")
axes[1].contourf(x, y, By_slice, levels=20)
axes[1].set_title('By')
axes[1].set_xlabel('x' + " (cm)")
axes[1].set_ylabel('y' + " (cm)")
axes[2].contourf(x, y, Bz_slice, levels=20)
axes[2].set_title('Bz')
axes[2].set_xlabel('x' + " (cm)")
axes[2].set_ylabel('y' + " (cm)")
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