import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from scipy.integrate import quad
import sympy as smp

def create_circle(radius: int, plane: str, plane_loc=0, center=(0, 0), segments=100) -> np.ndarray:
    ''' Return an array of x, y, z coordinates for a circle in a specific plane.

    Parameters
    ----------
    radius : float
        The radius of the circle
    plane: str
        Plane the circle is in, one of x, y, or z
    plane_loc : float
        The location of the plane. Plane of x with loc 0 means we're at the plane x=0
    center : tuple
        The center coordinates of the circle in the plane. In order x, y, z with the plane coordiante skipped
    segments : int
        Number of discrete circle segments ie) how many values of phi
    sympy : bool
        If True, the return is a sympy matrix of parametric coordinate equations

    Returns
    -------
    np.ndarrary
        An array of size [3, segments] containing the coordinates of the circle

    '''
    phi = np.linspace(0, 2*np.pi, 100)
    t, x, y, z = smp.symbols('t, x, y, z')

    if plane == 'x':  # so circle is in yz
        return np.array([np.full(len(phi), plane_loc), radius * np.cos(phi) + center[0], radius * np.sin(phi) + center[1]])
    elif plane == 'y':
        return np.array([radius * np.cos(phi) + center[0], np.full(len(phi), plane_loc), radius * np.sin(phi) + center[1]])
    elif plane == 'z':
        return np.array([radius * np.cos(phi) + center[0], radius * np.sin(phi) + center[1], np.full(len(phi), plane_loc)])
    

def plot_coil(x: np.ndarray, y: np.ndarray, z: np.ndarray, filename='coil.png') -> None:
    '''Save a 3D plot of a coil

    Parameters
    ----------
    x : np.ndarray 
        x coordinates
    y : np.ndarray 
        y coordinates
    z : np.ndarray 
        z coordinates
    filename : str
        Name (with extension) to which the image is saved

    Returns
    -------
    none
        No return, but image is saved
    '''
    fig = plt.figure()
    tick_spacing = 2
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$")
    ax.set_zlabel("$z$")

    ax.plot3D(x, y, z, lw=2)
    for axis in [ax.xaxis,ax.yaxis,ax.zaxis]:
        axis.set_major_locator(mpl.ticker.MultipleLocator(tick_spacing))


    plt.tight_layout()
    plt.savefig(filename)

def B(dBxdt, dBydt, dBzdt, x, y, z):
    return np.array([quad(dBxdt, 0, 2*np.pi, args=(x, y, z))[0],
                     quad(dBydt, 0, 2*np.pi, args=(x, y, z))[0],
                     quad(dBzdt, 0, 2*np.pi, args=(x, y, z))[0]])


def B_volume(t: smp.core.symbol.Symbol, x: smp.core.symbol.Symbol, y: smp.core.symbol.Symbol, z: smp.core.symbol.Symbol, 
      l: smp.Matrix, bbox=(-1, -1, -1, 2, 2, 2)):
    
    r = smp.Matrix([x, y, z])
    sep = r - l

    # define the integrand
    integrand = smp.diff(l, t).cross(sep) / sep.norm()**3

    # get the x, y, and z components of the integrand
    dBxdt = smp.lambdify([t, x, y, z], integrand[0])
    dBydt = smp.lambdify([t, x, y, z], integrand[1])
    dBzdt = smp.lambdify([t, x, y, z], integrand[2])

    x, y, z = np.linspace(5, 10, 5), np.linspace(-10, 10, 21), np.linspace(-10, 10, 21)
    xv, yv, zv = np.meshgrid(x, y, z, indexing='ij')

    B_field = np.vectorize(B, signature='(),(),(),(),(),()->(n)')(dBxdt, dBydt, dBzdt, xv, yv, zv)

    return B_field