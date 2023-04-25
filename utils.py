import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from scipy.integrate import quad
import sympy as smp

def create_circle(radius: float, plane: str, plane_loc=0, center=(0, 0), segments=100) -> np.ndarray:
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

    if plane == 'x':  # so circle is in yz
        return np.array([np.full(len(phi), plane_loc), radius * np.cos(phi) + center[0], radius * np.sin(phi) + center[1]])
    elif plane == 'y':
        return np.array([radius * np.cos(phi) + center[0], np.full(len(phi), plane_loc), radius * np.sin(phi) + center[1]])
    elif plane == 'z':
        return np.array([radius * np.cos(phi) + center[0], radius * np.sin(phi) + center[1], np.full(len(phi), plane_loc)])

    
def create_rectangle(height: float, width: float, plane: str, plane_loc=0, loc=(0, 0), segments=100) -> np.ndarray:
    ''' Return an array of x, y, z coordinates for a circle in a specific plane.

    Parameters
    ----------
    height : float
        The height of the rectangle
    width : float
        The width of the rectangle
    plane: str
        Plane the circle is in, one of x, y, or z
    plane_loc : float
        The location of the plane. Plane of x with loc 0 means we're at the plane x=0
    loc : tuple
        The coordinates of the lower left corner of the rectangle. In order x, y, z with the plane coordiante skipped
    segments : int
        Number of discrete line segments
    sympy : bool
        If True, the return is a sympy matrix of parametric coordinate equations

    Returns
    -------
    np.ndarrary
        An array of size [3, segments] containing the coordinates of the rectangle

    '''

    if plane == 'x':  # so circle is in yz
        side_1 = np.array([np.full(segments, plane_loc), np.linspace(loc[1], loc[1] + height, segments), np.full(segments, loc[0])])
        side_2 = np.array([np.full(segments, plane_loc), np.full(segments, loc[1]) + height, np.linspace(loc[0], loc[0] + width, segments)])
        side_3 = np.array([np.full(segments, plane_loc), np.linspace(loc[1], loc[1] + height, segments), np.full(segments, loc[0] + width)])
        side_4 = np.array([np.full(segments, plane_loc), np.full(segments, loc[1]), np.linspace(loc[0], loc[0] + width, segments)])
        return np.concatenate((side_1, side_2, side_3, side_4), axis=-1)
    
    elif plane == 'y':
        side_1 = np.array([np.linspace(loc[1], loc[1] + height, segments), np.full(segments, plane_loc), np.full(segments, loc[0])])
        side_2 = np.array([np.full(segments, loc[1]) + height, np.full(segments, plane_loc), np.linspace(loc[0], loc[0] + width, segments)])
        side_3 = np.array([np.linspace(loc[1], loc[1] + height, segments), np.full(segments, plane_loc), np.full(segments, loc[0] + width)])
        side_4 = np.array([np.full(segments, loc[1]), np.full(segments, plane_loc), np.linspace(loc[0], loc[0] + width, segments)])
        return np.concatenate((side_1, side_2, side_3, side_4), axis=-1)
    
    elif plane == 'z':
        side_1 = np.array([np.full(segments, loc[0]), np.linspace(loc[1], loc[1] + height, segments), np.full(segments, plane_loc)])
        side_2 = np.array([np.linspace(loc[0], loc[0] + width, segments), np.full(segments, loc[1]) + height,np.full(segments, plane_loc)])
        side_3 = np.array([np.full(segments, loc[0] + width), np.linspace(loc[1], loc[1] + height, segments),np.full(segments, plane_loc)])
        side_4 = np.array([np.linspace(loc[0], loc[0] + width, segments), np.full(segments, loc[1]),np.full(segments, plane_loc)])
        return np.concatenate((side_1, side_2, side_3, side_4), axis=-1)

def plot_coil(x: np.ndarray|list, y: np.ndarray|list, z: np.ndarray|list, filename='coil.png') -> None:
    '''Save a 3D plot of a coil

    Parameters
    ----------
    x : np.ndarray|list 
        x coordinates, or list of x coordiates if piecewise
    y : np.ndarray|list 
        y coordinates, or list of y coordiates if piecewise
    z : np.ndarray|list 
        z coordinates, or list of z coordiates if piecewise
    filename : str
        Name (with extension) to which the image is saved

    Returns
    -------
    none
        No return, but image is saved
    '''
    fig = plt.figure()
    tick_spacing = 0.5
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$")
    ax.set_zlabel("$z$")

    if type(x) == list:
        for i, x_coords in enumerate(x):
            y_coords, z_coords = y[i], z[i]
            ax.plot(x_coords, y_coords, z_coords, c='m')
    else:
        ax.plot(x, y, z, c='m')

    for axis in [ax.xaxis,ax.yaxis,ax.zaxis]:
        axis.set_major_locator(mpl.ticker.MultipleLocator(tick_spacing))

    plt.tight_layout()
    plt.savefig(filename)
    #plt.show()

    
def B(lower_lim, upper_lim, dBxdt, dBydt, dBzdt, x, y, z):
    return np.array([quad(dBxdt, lower_lim, upper_lim, args=(x, y, z))[0],
                     quad(dBydt, lower_lim, upper_lim, args=(x, y, z))[0],
                     quad(dBzdt, lower_lim, upper_lim, args=(x, y, z))[0]])

def B_volume_piecewise(t: smp.core.symbol.Symbol, x: smp.core.symbol.Symbol, y: smp.core.symbol.Symbol, z: smp.core.symbol.Symbol, 
                       ls: list, upper_lims: list, lower_lims: list, bbox=(-1, -1, -1, 2, 2, 2), vol_res=(1, 1, 1)) -> np.ndarray:
    B_fields = []
    for i, l in enumerate(ls):
        B_field = B_volume(t, x, y, z, l, bbox=bbox, vol_res=vol_res, upper_lim=upper_lims[i], lower_lim=lower_lims[i])
        B_fields.append(B_field)
    B_field = sum(B_fields)
    return B_field

def B_volume(t: smp.core.symbol.Symbol, x: smp.core.symbol.Symbol, y: smp.core.symbol.Symbol, z: smp.core.symbol.Symbol, 
             l: smp.Matrix, bbox=(-1, -1, -1, 2, 2, 2), vol_res=(1, 1, 1), upper_lim=2*np.pi, lower_lim=0) -> np.ndarray:
    ''' Calculate the B field at every point in a volume of space

    Parameters
    ----------
    t : sympy.core.symbol.Symbol
        Sympy symbol representing parameterizaiton parameter t
    x : sympy.core.symbol.Symbol
        Sympy symbol representing coordinate x in space
    y : sympy.core.symbol.Symbol
        Sympy symbol representing coordinate y in space
    z : sympy.core.symbol.Symbol
        Sympy symbol representing coordinate z in space
    l : sympy.core.symbol.Symbol
        Sympy symbol representing distance l from wire to a point in space.
    vol_res : tuple
        The volume resolution, or voxel dimensions, in x, y, z
    bbox : tuple
        The lower x, y, z bounds followed by the upper x, y, z bounds
    ** kwargs
        Keyword arguments passed to B function, namely upper and lower limit


    Returns
    -------
    np.ndarray
        4D volume of magnetic field components at each point in space. Last dimension is size 3
        representing x, y, and z components
    '''
    # bbox is lower x, y, z loc and then upper x, y, z loc
    r = smp.Matrix([x, y, z])

    sep = r - l

    # define the integrand
    integrand = smp.diff(l, t).cross(sep) / sep.norm()**3

    # get the x, y, and z components of the integrand
    dBxdt = smp.lambdify([t, x, y, z], integrand[0])
    dBydt = smp.lambdify([t, x, y, z], integrand[1])
    dBzdt = smp.lambdify([t, x, y, z], integrand[2])

    x_dim, y_dim, z_dim = np.arange(bbox[0], bbox[3], vol_res[0]), np.arange(bbox[1], bbox[4], vol_res[1]), np.arange(bbox[2], bbox[5], vol_res[2])
    xv, yv, zv = np.meshgrid(x_dim, y_dim, z_dim, indexing='ij')

    B_field = np.vectorize(B, signature='(),(),()->(n)', excluded=[0, 1, 2, 3, 4])(lower_lim, upper_lim, dBxdt, dBydt, dBzdt, xv, yv, zv)

    return B_field

def get_slice(data_volume: np.ndarray, slice: str, slice_loc: float, vol_res=(1, 1, 1), bbox=(-1, -1, -1, 2, 2, 2)) -> np.ndarray:
    ''' Get a slice at a given real-world coordinate (not index)
    Parameters
    ----------
    data_volume : np.ndarray 
        3D volume of data at each point in space
    slice : str 
        Which plane we are taking the slice from. E.g. z=0
    slice_loc : float 
        Real-world slice index
    vol_res : tuple
        The volume resolution, or voxel dimensions, in x, y, z
    bbox : tuple
        The lower x, y, z bounds followed by the upper x, y, z bounds

    Returns
    -------
    np.ndarray
        2D slice taken from data_volume at the desired location
    '''
    if slice == 'x':
        x = np.arange(bbox[0], bbox[3], vol_res[0])
        min_ind = np.argmin(x - slice_loc)
        return data_volume[min_ind, :, :]
    
    elif slice == 'y':
        y = np.arange(bbox[1], bbox[4], vol_res[1])
        min_ind = np.argmin(y - slice_loc)
        return data_volume[:, min_ind, :]
    
    elif slice == 'z':
        z = np.arange(bbox[2], bbox[5], vol_res[2])
        min_ind = np.argmin(z - slice_loc)
        return data_volume[:, :, min_ind]
    
def return_coords(fn: callable, inputs) -> tuple:

    x = [fn(t)[0][0] for t in inputs]
    y = [fn(t)[1][0] for t in inputs]
    z = [fn(t)[2][0] for t in inputs]

    return x, y, z
