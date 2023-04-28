import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np

from utils import get_slice

def plot_coil(x : list, y : list, z : list, filename='coil.png') -> None:
    '''Save a 3D plot of a coil

    Parameters
    ----------
    x : np.ndarray|list 
        x coordinates, or list of x coordiates if piecewise
    y : np.ndarray|list 
        y coordinates, or list of y coordiates if piecewise
    z : np.ndarray|list 
        z coordinates, or list of z coordiates if piecewise
    filename : str, optional
        Name (with extension) to which the image is saved

    Returns
    -------
    none
        No return, but image is saved
    '''
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$")
    ax.set_zlabel("$z$")

    for i, x_coords in enumerate(x):
        y_coords, z_coords = y[i], z[i]
        ax.plot(x_coords, y_coords, z_coords, c='m')

    #tick_spacing = 0.5
    #for axis in [ax.xaxis,ax.yaxis,ax.zaxis]:
    #    axis.set_major_locator(mpl.ticker.MultipleLocator(tick_spacing))

    plt.tight_layout()
    plt.savefig(filename)
    #plt.show()

    
def plot_mag_phase(B_complex : np.ndarray, slice: str, slice_loc: float, 
                   vol_res=(1, 1, 1), bbox=(-1, -1, -1, 2, 2, 2), 
                   filename='mag_phase.png') -> None:
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
    x_dim = np.arange(bbox[0], bbox[3] + 1e-10, vol_res[0])
    y_dim = np.arange(bbox[1], bbox[4] + 1e-10, vol_res[1])
    z_dim = np.arange(bbox[2], bbox[5] + 1e-10, vol_res[2])
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

    im1 = axes[0].contourf(ax1, ax2, B_mag, levels=20)
    axes[0].set_title('Magnitude')
    axes[0].set_xlabel(ax1_label + " (cm)")
    axes[0].set_ylabel(ax2_label + " (cm)")
    axes[0].set_aspect('equal')

    im2 = axes[1].contourf(ax1, ax2, B_phase, levels=20)
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
                filename='B_field_components.png') -> None:
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
    Bx = B_field[:, :, :, 0]
    By = B_field[:, :, :, 1]
    Bz = B_field[:, :, :, 2]

    x_dim = np.arange(bbox[0], bbox[3] + 1e-10, vol_res[0])
    y_dim = np.arange(bbox[1], bbox[4] + 1e-10, vol_res[1])
    z_dim = np.arange(bbox[2], bbox[5] + 1e-10, vol_res[2])
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

    axes[0].contourf(ax1, ax2, Bx_slice, levels=20, norm=norm, cmap='RdBu_r')
    axes[0].set_title(r'$B_x$')
    axes[0].set_xlabel(ax1_label + " (cm)")
    axes[0].set_ylabel(ax2_label + " (cm)")
    axes[0].set_aspect('equal')

    axes[1].contourf(ax1, ax2, By_slice, levels=20, norm=norm, cmap='RdBu_r')
    axes[1].set_title(r'$B_y$')
    axes[1].set_xlabel(ax1_label+ " (cm)")
    axes[1].set_ylabel(ax2_label + " (cm)")
    axes[1].set_aspect('equal')

    divider = make_axes_locatable(axes[2])
    cax = divider.append_axes('right', size='5%', pad=0.05)
    axes[2].contourf(ax1, ax2, Bz_slice, levels=20, norm=norm, cmap='RdBu_r')
    axes[2].set_title(r'$B_z$')
    axes[2].set_xlabel(ax1_label + " (cm)")
    axes[2].set_ylabel(ax2_label + " (cm)")
    axes[2].set_aspect('equal')

    fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap='RdBu_r'), cax=cax)
    fig.tight_layout()
    plt.savefig(filename, bbox_inches='tight', dpi=250)