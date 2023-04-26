import matplotlib.pyplot as plt
import matplotlib as mpl
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

    
def plot_mag_phase(B_complex, slice: str, slice_loc: float, vol_res=(1, 1, 1), 
                   bbox=(-1, -1, -1, 2, 2, 2), filename='mag_phase.png') -> None:
    x_dim = np.arange(bbox[0], bbox[3], vol_res[0])
    y_dim = np.arange(bbox[1], bbox[4], vol_res[1])
    z_dim = np.arange(bbox[2], bbox[5], vol_res[2])
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
    axes[0].contourf(ax1, ax2, B_mag, levels=20)
    axes[0].set_title('Magnitude')
    axes[0].set_xlabel(ax1_label + " (cm)")
    axes[0].set_ylabel(ax2_label + " (cm)")
    axes[1].contourf(ax1, ax2, B_phase, levels=20)
    axes[1].set_title('Phase')
    axes[1].set_xlabel(ax1_label  + " (cm)")
    axes[1].set_ylabel(ax2_label + " (cm)")
    fig.tight_layout()
    plt.savefig(filename)

    
def plot_fields(B_field, slice: str, slice_loc: float, vol_res=(1, 1, 1), 
                   bbox=(-1, -1, -1, 2, 2, 2), filename='B_field_components.png'):
    Bx = B_field[:,:,:,0]
    By = B_field[:,:,:,1]
    Bz = B_field[:,:,:,2]

    x_dim = np.arange(bbox[0], bbox[3], vol_res[0])
    y_dim = np.arange(bbox[1], bbox[4], vol_res[1])
    z_dim = np.arange(bbox[2], bbox[5], vol_res[2])
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
    norm = mpl.colors.Normalize(vmin=vmin, vmax=vmax)

    fig, axes = plt.subplots(nrows=1, ncols=3)

    axes[0].contourf(ax1, ax2, Bx_slice, levels=20, norm=norm, cmap='RdBu')
    axes[0].set_title(r'$B_x$')
    axes[0].set_xlabel(ax1_label + " (cm)")
    axes[0].set_ylabel(ax2_label + " (cm)")
    axes[1].contourf(ax1, ax2, By_slice, levels=20, norm=norm, cmap='RdBu')
    axes[1].set_title(r'$B_y$')
    axes[1].set_xlabel(ax1_label+ " (cm)")
    axes[1].set_ylabel(ax2_label + " (cm)")
    axes[2].contourf(ax1, ax2, Bz_slice, levels=20, norm=norm, cmap='RdBu')
    axes[2].set_title(r'$B_z$')
    axes[2].set_xlabel(ax1_label + " (cm)")
    axes[2].set_ylabel(ax2_label + " (cm)")
    fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap='RdBu'), cax=None)
    fig.tight_layout()
    plt.savefig('B_field_components.png')