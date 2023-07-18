import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from scipy.integrate import quad_vec
import sympy as smp
from mpl_toolkits.axes_grid1 import make_axes_locatable

def B(lower_lim : float, upper_lim : float, dBxdt : callable, dBydt : callable, 
      dBzdt : callable, x : float, y : float, z : float) -> np.ndarray:
    '''Integrate dBdt along the length of the wire for a given point in space
    '''
    x_comp = quad_vec(dBxdt, lower_lim, upper_lim, args=(x, y, z))[0]
    if type(x_comp) == float:
        x_comp = np.full(x.shape, x_comp)
    y_comp = quad_vec(dBydt, lower_lim, upper_lim, args=(x, y, z))[0]
    if type(y_comp) == float:
        y_comp = np.full(y.shape, y_comp)
    z_comp = quad_vec(dBzdt, lower_lim, upper_lim, args=(x, y, z))[0]
    if type(z_comp) == float:
        z_comp = np.full(z.shape, z_comp)
    
    return np.array([x_comp, y_comp, z_comp])

# def B_volume_piecewise(t: smp.core.symbol.Symbol, x: smp.core.symbol.Symbol, 
#                        y: smp.core.symbol.Symbol, z: smp.core.symbol.Symbol, 
#                        ls: list, lower_lims: list, upper_lims: list, 
#                        bbox=(-1, -1, -1, 2, 2, 2), vol_res=(1, 1, 1)) -> np.ndarray:
#     '''Calculate the B field at every point in a volume for a piecewise function

#     Given a list of variables l that each represent the distance from the origin 
#     to a distinct piece of wire, integrate along the wires to find the net 
#     B (magnetic) field at each point within a defined volume. The volume is 
#     bounded by a bbox and space is discretized based on the volume resolution.

#     Parameters
#     ----------
#     t : sympy.core.symbol.Symbol
#         Sympy symbol representing parameterizaiton parameter t
#     x : sympy.core.symbol.Symbol
#         Sympy symbol representing coordinate x in space
#     y : sympy.core.symbol.Symbol
#         Sympy symbol representing coordinate y in space
#     z : sympy.core.symbol.Symbol
#         Sympy symbol representing coordinate z in space
#     ls : list
#         List of sympy symbols representing distance l from wire to a point in 
#         space.
#     lower_lims : list
#         A list of the lower limits of integration for each piece
#     upper_lims : list
#         A list of the upper limits of integration for each piece
#     bbox : tuple, optional
#         The lower x, y, z bounds followed by the upper x, y, z bounds
#     vol_res : tuple, optional
#         The volume resolution, or voxel dimensions, in x, y, z

#     Returns
#     -------
#     np.ndarray
#         4D volume of magnetic field components at each point in space. Last 
#         dimension is size 3 representing x, y, and z components
#     '''
#     B_fields = []
#     for i, l in enumerate(ls):
#         B_field = B_volume(t, x, y, z, l, bbox=bbox, vol_res=vol_res, 
#                            upper_lim=upper_lims[i], lower_lim=lower_lims[i])
#         B_fields.append(B_field)

#     B_field = sum(B_fields)
#     return B_field


# def B_volume(coil : Coil) -> np.ndarray:
#     ''' Calculate the B field at every point in a volume

#     Given a variable l that represents the distance from the origin to a piece 
#     of wire, integrate along that wire to find the B (magnetic) field at each
#     point within a defined volume. The volume is bounded by a bbox and space
#     is discretized based on the volume resolution.

#     Parameters
#     ----------

#     Returns
#     -------
#     np.ndarray
#         4D volume of magnetic field components at each point in space. Last 
#         dimension is size 3 representing x, y, and z components
#     '''

#     B_fields = []
    
#     for segment in coil.segments:

#         fn = segment.line_fn.fn

#         x, y, z = smp.symbols(['x', 'y', 'z'])
#         r = smp.Matrix([x, y, z])
#         sep = r - fn

#         t = segment.line_fn.parameter
        
#         # Define the integrand
#         integrand = smp.diff(fn, t).cross(sep) / sep.norm()**3
#         # Get the x, y, and z components of the integrand
#         dBxdt = smp.lambdify([t, x, y, z], integrand[0])
#         dBydt = smp.lambdify([t, x, y, z], integrand[1])
#         dBzdt = smp.lambdify([t, x, y, z], integrand[2])

#         # Add small tolerance to endpoint so it's included
#         x_dim = np.arange(coil.scanner.bbox[0], coil.scanner.bbox[3] + 1e-10, coil.scanner.vol_res[0])
#         y_dim = np.arange(coil.scanner.bbox[1], coil.scanner.bbox[4] + 1e-10, coil.scanner.vol_res[1])
#         z_dim = np.arange(coil.scanner.bbox[2], coil.scanner.bbox[5] + 1e-10, coil.scanner.vol_res[2])
#         xv, yv, zv = np.meshgrid(x_dim, y_dim, z_dim, indexing='ij')

#         B_field_fn = np.vectorize(B, signature='(),(),()->(n)', 
#                                 excluded=[0, 1, 2, 3, 4])
        
#         B_fields.append(B_field_fn(segment.low_lim, segment.up_lim, dBxdt, dBydt, dBzdt, xv, yv, zv))

#     return sum(B_fields)


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
        x = np.arange(bbox[0], bbox[1] + 1e-10, vol_res[0])
        min_ind = np.argmin(np.abs(x - slice_loc))
        return data_volume[min_ind, :, :]
    
    elif slice.lower() == 'y':
        y = np.arange(bbox[2], bbox[3] + 1e-10, vol_res[1])
        min_ind = np.argmin(np.abs(y - slice_loc))
        return data_volume[:, min_ind, :]
    
    elif slice.lower() == 'z':
        z = np.arange(bbox[4], bbox[5] + 1e-10, vol_res[2])
        min_ind = np.argmin(np.abs(z - slice_loc))
        return data_volume[:, :, min_ind]
    
def plot_mag_phase(B_complex : np.ndarray, slice: str, slice_loc: float, 
                   vol_res=(1, 1, 1), bbox=(-1, -1, -1, 2, 2, 2), 
                   filename='mag_phase_stephen_test_II.png') -> None:
    '''Plot the magnitude and phase of the sensitivity map in a given plane

    Parameters
    ----------
    B_field : np.ndarray
        The complex phase sensitivity in a given volume. The shape is h, w, l, 3,
        where the last dimension is the x, y, z components
    slice : float, optional
        The plane location. In the case of x=0, the location is 0
    slice_loc : tuple, optional
        The two coordinates indicating the lower left corner of the rectangle 
    bbox : tuple, optional
        The bounds defining the volume the B field is defined within. A tuple 
        of the lower x, y, z bounds followed by the upper x, y, z bounds
    vol_res : tuple, optional
        The voxel size of the volume in which the B field is defined. A tuple of
        the volume resolution, or voxel dimensions, in x, y, z
    filename : str
        The filename (indlucing the extension) of the image being saved

    Returns
    -------
    none
    '''
    x_dim = np.arange(bbox[0], bbox[1] + 1e-10, vol_res[0])
    y_dim = np.arange(bbox[2], bbox[3] + 1e-10, vol_res[1])
    z_dim = np.arange(bbox[4], bbox[5] + 1e-10, vol_res[2])
    xv, yv, zv = np.meshgrid(x_dim, y_dim, z_dim, indexing='ij')

    B_slice = get_slice(B_complex, slice, slice_loc, vol_res=vol_res, bbox=bbox)
    B_mag = np.abs(B_slice)
    B_phase = np.angle(B_slice)

    if slice == 'x':
        ax1_label, ax2_label = 'y', 'z'
        ax2 = get_slice(yv, slice, slice_loc,vol_res=vol_res, bbox=bbox)
        ax1 = get_slice(zv, slice, slice_loc, vol_res=vol_res, bbox=bbox)
    elif slice == 'y':
        ax1_label, ax2_label = 'x', 'z'
        ax2 = get_slice(xv, slice, slice_loc,vol_res=vol_res, bbox=bbox)
        ax1 = get_slice(zv, slice, slice_loc, vol_res=vol_res, bbox=bbox)
    elif slice == 'z':
        ax1_label, ax2_label = 'x', 'y'
        ax2 = get_slice(xv, slice, slice_loc,vol_res=vol_res, bbox=bbox)
        ax1 = get_slice(yv, slice, slice_loc, vol_res=vol_res, bbox=bbox)

    fig, axes = plt.subplots(nrows=1, ncols=2)

    divider1 = make_axes_locatable(axes[0])
    cax1 = divider1.append_axes('right', size='5%', pad=0.05)
    divider2 = make_axes_locatable(axes[1])
    cax2 = divider2.append_axes('right', size='5%', pad=0.05)

    im1 = axes[0].contourf(ax2, ax1, B_mag, levels=20)
    axes[0].set_title('Magnitude')
    axes[0].set_xlabel(ax1_label + " (cm)")
    axes[0].set_ylabel(ax2_label + " (cm)")
    axes[0].set_aspect('equal')

    im2 = axes[1].contourf(ax2, ax1, B_phase, levels=20)
    axes[1].set_title('Phase')
    axes[1].set_xlabel(ax1_label  + " (cm)")
    axes[1].set_ylabel(ax2_label + " (cm)")
    axes[1].set_aspect('equal')

    fig.colorbar(im1, cax=cax1, orientation='vertical')
    fig.colorbar(im2, cax=cax2, orientation='vertical')

    fig.tight_layout()
    plt.savefig(filename, bbox_inches='tight', dpi=250)

    
def plot_fields(B_field : np.ndarray, slice: str, slice_loc: float, 
                vol_res=(1, 1, 1), bbox=(-1, -1, -1, 2, 2, 2), 
                filename='B_field_components_stephen_test.png'):
    '''Plot the x, y, and z components of the Magnetic field.

    Parameters
    ----------
    B_field : np.ndarray
        The magnetic field in a given volume. The shape is h, w, l, 3, where the
        last dimension is the x, y, z components
    slice : float, optional
        The plane location. In the case of x=0, the location is 0
    slice_loc : tuple, optional
        The two coordinates indicating the lower left corner of the rectangle 
    bbox : tuple, optional
        The bounds defining the volume the B field is defined within. A tuple 
        of the lower x, y, z bounds followed by the upper x, y, z bounds
    vol_res : tuple, optional
        The voxel size of the volume in which the B field is defined. A tuple of
        the volume resolution, or voxel dimensions, in x, y, z
    filename : str
        The filename (indlucing the extension) of the image being saved

    Returns
    -------
    none
    '''
    Bx = B_field[0, :, :, :]
    By = B_field[1, :, :, :]
    Bz = B_field[2, :, :, :]

    x_dim = np.arange(bbox[0], bbox[1] + 1e-10, vol_res[0])
    y_dim = np.arange(bbox[2], bbox[3] + 1e-10, vol_res[1])
    z_dim = np.arange(bbox[4], bbox[5] + 1e-10, vol_res[2])
    xv, yv, zv = np.meshgrid(x_dim, y_dim, z_dim, indexing='ij')

    Bx_slice = get_slice(Bx, slice, slice_loc, vol_res=vol_res, bbox=bbox)
    By_slice = get_slice(By, slice, slice_loc, vol_res=vol_res, bbox=bbox)
    Bz_slice = get_slice(Bz, slice, slice_loc, vol_res=vol_res, bbox=bbox)

    if slice == 'x':
        ax1_label, ax2_label = 'y', 'z'
        ax2 = get_slice(yv, slice, slice_loc,vol_res=vol_res, bbox=bbox)
        ax1 = get_slice(zv, slice, slice_loc, vol_res=vol_res, bbox=bbox)
    elif slice == 'y':
        ax1_label, ax2_label = 'x', 'z'
        ax2 = get_slice(xv, slice, slice_loc,vol_res=vol_res, bbox=bbox)
        ax1 = get_slice(zv, slice, slice_loc, vol_res=vol_res, bbox=bbox)
    elif slice == 'z':
        ax1_label, ax2_label = 'x', 'y'
        ax2 = get_slice(xv, slice, slice_loc,vol_res=vol_res, bbox=bbox)
        ax1 = get_slice(yv, slice, slice_loc, vol_res=vol_res, bbox=bbox)

    vmin = min(np.min(Bx_slice), np.min(By_slice), np.min(Bz_slice))
    vmax = max(np.max(Bx_slice), np.max(By_slice), np.max(Bz_slice))
    norm = mpl.colors.TwoSlopeNorm(vmin=vmin, vcenter=0., vmax=vmax)

    fig, axes = plt.subplots(nrows=1, ncols=3)

    axes[0].contourf(ax2, ax1, Bx_slice, levels=20, norm=norm, cmap='RdBu_r')
    axes[0].set_title(r'$B_x$')
    axes[0].set_xlabel(ax1_label + " (cm)")
    axes[0].set_ylabel(ax2_label + " (cm)")
    axes[0].set_aspect('equal')

    axes[1].contourf(ax2, ax1, By_slice, levels=20, norm=norm, cmap='RdBu_r')
    axes[1].set_title(r'$B_y$')
    axes[1].set_xlabel(ax2_label+ " (cm)")
    axes[1].set_ylabel(ax1_label + " (cm)")
    axes[1].set_aspect('equal')

    #divider = make_axes_locatable(axes[2])
    #cax = divider.append_axes('right', size='5%', pad=0.05)
    axes[2].contourf(ax2, ax1, Bz_slice, levels=20, norm=norm, cmap='RdBu_r')
    axes[2].set_title(r'$B_z$')
    axes[2].set_xlabel(ax1_label + " (cm)")
    axes[2].set_ylabel(ax2_label + " (cm)")
    axes[2].set_aspect('equal')

    cax = fig.add_axes([axes[2].get_position().x1 + 0.1, axes[2].get_position().y0, 0.02, axes[2].get_position().y1 - axes[2].get_position().y0])
    plt.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap='RdBu_r'), cax=cax)
    # fig.tight_layout()
    # plt.savefig(filename, bbox_inches='tight', dpi=250)
    return cax