import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad
import plotly.graph_objects as go
from IPython.display import HTML
import sympy as smp
from sympy.vector import cross
from skimage.restoration import unwrap_phase
phi = np.linspace(0, 2*np.pi, 100)
# circle in the xy plane
def l(phi):
    return 1 * np.array([np.zeros(len(phi)), np.cos(phi), np.sin(phi)])

lx, ly, lz = l(phi)
plt.figure(figsize=(7,7))
plt.plot(lx, lz)
plt.xlabel('$x/R$', fontsize=25)
plt.ylabel('$z/R$', fontsize=25)
plt.savefig('bs_test.png')

t, x, y, z = smp.symbols('t, x, y, z')

# get l, r, and the separation vector r - l
l = 1 * smp.Matrix([0, smp.cos(t), smp.sin(t)])
# in theory a rectangle, but the derivative is undefined
# l = smp.Matrix([smp.functions.Abs(smp.cos(t)) * smp.cos(t) + smp.functions.Abs(smp.sin(t)) * smp.sin(t),
#                 smp.functions.Abs(smp.cos(t)) * smp.cos(t) - smp.functions.Abs(smp.sin(t)) * smp.sin(t),
#                 0])
#l = smp.Matrix([t, 0, 0])
r = smp.Matrix([x, y, z])
sep = r-l

# define the integrand
integrand = smp.diff(l, t).cross(sep) / sep.norm()**3

# get the x, y, and z components of the integrand
dBxdt = smp.lambdify([t, x, y, z], integrand[0])
dBydt = smp.lambdify([t, x, y, z], integrand[1])
dBzdt = smp.lambdify([t, x, y, z], integrand[2])

# get the magentic field by performing the integral over each component
def B(x, y, z):
    return np.array([quad(dBxdt, 0, 2*np.pi, args=(x, y, z))[0],
                     quad(dBydt, 0, 2*np.pi, args=(x, y, z))[0],
                     quad(dBzdt, 0, 2*np.pi, args=(x, y, z))[0]])

# set up a meshgrid to solve for the field in some 3d volume
x, y, z = np.linspace(5, 10, 5), np.linspace(-10, 10, 21), np.linspace(-10, 10, 21)
xv, yv, zv = np.meshgrid(x, y, z, indexing='ij')

B_field = np.vectorize(B, signature='(),(),()->(n)')(xv, yv, zv)
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

fig.write_html('test.html')