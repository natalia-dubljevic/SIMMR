from collections.abc import Iterable
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from scipy.integrate import quad
import sympy as smp



def B(lower_lim : float, upper_lim : float, dBxdt : callable, dBydt : callable, 
      dBzdt : callable, x : float, y : float, z : float) -> np.ndarray:
    '''Integrate dBdt along the length of the wire for a given point in space
    '''
    return np.array([quad(dBxdt, lower_lim, upper_lim, args=(x, y, z))[0],
                     quad(dBydt, lower_lim, upper_lim, args=(x, y, z))[0],
                     quad(dBzdt, lower_lim, upper_lim, args=(x, y, z))[0]])


def B_volume_piecewise(t: smp.core.symbol.Symbol, x: smp.core.symbol.Symbol, 
                       y: smp.core.symbol.Symbol, z: smp.core.symbol.Symbol, 
                       ls: list, lower_lims: list, upper_lims: list, 
                       bbox=(-1, -1, -1, 2, 2, 2), vol_res=(1, 1, 1)) -> np.ndarray:
    '''Calculate the B field at every point in a volume for a piecewise function

    Given a list of variables l that each represent the distance from the origin 
    to a distinct piece of wire, integrate along the wires to find the net 
    B (magnetic) field at each point within a defined volume. The volume is 
    bounded by a bbox and space is discretized based on the volume resolution.

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
    ls : list
        List of sympy symbols representing distance l from wire to a point in 
        space.
    lower_lims : list
        A list of the lower limits of integration for each piece
    upper_lims : list
        A list of the upper limits of integration for each piece
    bbox : tuple, optional
        The lower x, y, z bounds followed by the upper x, y, z bounds
    vol_res : tuple, optional
        The volume resolution, or voxel dimensions, in x, y, z

    Returns
    -------
    np.ndarray
        4D volume of magnetic field components at each point in space. Last 
        dimension is size 3 representing x, y, and z components
    '''
    B_fields = []
    for i, l in enumerate(ls):
        B_field = B_volume(t, x, y, z, l, bbox=bbox, vol_res=vol_res, 
                           upper_lim=upper_lims[i], lower_lim=lower_lims[i])
        B_fields.append(B_field)

    B_field = sum(B_fields)
    return B_field


def B_volume(t: smp.core.symbol.Symbol, x: smp.core.symbol.Symbol, 
             y: smp.core.symbol.Symbol, z: smp.core.symbol.Symbol, 
             l: smp.Matrix, lower_lim, upper_lim, bbox=(-1, -1, -1, 2, 2, 2), 
             vol_res=(1, 1, 1)) -> np.ndarray:
    ''' Calculate the B field at every point in a volume

    Given a variable l that represents the distance from the origin to a piece 
    of wire, integrate along that wire to find the B (magnetic) field at each
    point within a defined volume. The volume is bounded by a bbox and space
    is discretized based on the volume resolution.

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
        Sympy symbol representing distance l from origin to wire
    lower_lim : float
        The lower limit of integration
    upper_lim : float
        The upper limit of integration
    bbox : tuple, optional
        The lower x, y, z bounds followed by the upper x, y, z bounds
    vol_res : tuple, optional
        The volume resolution, or voxel dimensions, in x, y, z

    Returns
    -------
    np.ndarray
        4D volume of magnetic field components at each point in space. Last 
        dimension is size 3 representing x, y, and z components
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

    # add small tolerance to endpoint so it's included
    x_dim = np.arange(bbox[0], bbox[3] + 1e-10, vol_res[0])
    y_dim = np.arange(bbox[1], bbox[4] + 1e-10, vol_res[1])
    z_dim = np.arange(bbox[2], bbox[5] + 1e-10, vol_res[2])
    xv, yv, zv = np.meshgrid(x_dim, y_dim, z_dim, indexing='ij')

    B_field_fn = np.vectorize(B, signature='(),(),()->(n)', 
                              excluded=[0, 1, 2, 3, 4])
    B_field = B_field_fn(lower_lim, upper_lim, dBxdt, dBydt, dBzdt, xv, yv, zv)

    return B_field


def get_slice(data_volume: np.ndarray, slice: str, slice_loc: float, 
              vol_res=(1, 1, 1), bbox=(-1, -1, -1, 2, 2, 2)) -> np.ndarray:
    ''' Get a slice at a given physical real-world coordinate

    Parameters
    ----------
    data_volume : np.ndarray 
        3D volume of data at each point in space
    slice : str 
        Which plane we are taking the slice from. E.g. z=0
    slice_loc : float 
        Real-world slice index
    vol_res : tuple, optional
        The volume resolution, or voxel dimensions, in x, y, z
    bbox : tuple, optional
        The lower x, y, z bounds followed by the upper x, y, z bounds

    Returns
    -------
    np.ndarray
        2D slice taken from data_volume at the desired location
    '''
    if slice.lower() == 'x':
        x = np.arange(bbox[0], bbox[3] + 1e-10, vol_res[0])
        min_ind = np.argmin(np.abs(x - slice_loc))
        return data_volume[min_ind, :, :]
    
    elif slice.lower() == 'y':
        y = np.arange(bbox[1], bbox[4] + 1e-10, vol_res[1])
        min_ind = np.argmin(np.abs(y - slice_loc))
        return data_volume[:, min_ind, :]
    
    elif slice.lower() == 'z':
        z = np.arange(bbox[2], bbox[5] + 1e-10, vol_res[2])
        min_ind = np.argmin(np.abs(z - slice_loc))
        return data_volume[:, :, min_ind]
    

def return_coords(fns: list, t : smp.core.symbol.Symbol, inputs : Iterable) -> tuple:
    '''Return lists of x, y, z coords from a list of lambdified functions

    Parameters
    ----------
    fns : list
        This is a list of lambdified functions. Generally, the list will only be
        length > 1 if the function you are trying to represent is piecwise
    t : smp.core.symbol.Symbol
        The parametrization parameter
    inputs : Iterable
        The values taken on by t
    
    Returns
    -------
    tuple
        A tuple of size 3 containing lists of x, y, and z coordinates for your
        function at t = inputs. This is useful for plotting your function
    
    '''
    xs = []
    ys = []
    zs = []
    for fn in fns:
        np_fn = smp.lambdify(t, fn)
        x = [np_fn(t)[0][0] for t in inputs]
        y = [np_fn(t)[1][0] for t in inputs]
        z = [np_fn(t)[2][0] for t in inputs]

        xs.append(x)
        ys.append(y)
        zs.append(z)
    return xs, ys, zs