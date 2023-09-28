import sympy as smp
import matplotlib.pyplot as plt
import numpy as np
import sympy as smp
import matplotlib.quiver as mquiver
from segment import Segment
import sim_utils
import b_calculation

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from scanner import Scanner

class Coil:
    '''
    A class used to represent the simulated scanners

    ...

    Attributes
    ----------
    segments : List[Segment]
        List of line segments that plot the coil
    scanner : Scanner
        The 'parent' scanner which the coil object is a part of
    
    Methods
    -------
    plot_coil(self, ax : plt.axes) -> bool
        Plots coil on passed axis; True if successful
    add_segment(self, segment : Segment) -> bool
        Adds segment that forms (a part of) the coil; True if successful
    B_volume(self) -> np.ndarray
        Calculate magnetic field at every point in self.scanner.bbox volume resulting from coil
    '''

    def __init__(self, segments : list[Segment] = None, scanner : 'Scanner' = None):
        '''
        Parameters
        ----------
        segments : list[Segment]
            List of line segments that plot the coil; defaults to an empty list
        scanner
            Scanner object to which the coil 'belongs' 
        '''
        segments = segments if segments is not None else []
        if segments == []:
            self.segments = segments
        else:
            for segment in segments:
                self.add_segment(segment)
        self.scanner = None
        self.set_scanner(scanner) # Link coil to its 'parent' scanner - for access to self.scanner.bbox, self.scanner.vol_res, etc.
        self.B_vol = None # For entire area -> should only be calculated on export (i.e., not during prototyping due to computational demands)
        self.B_vol_slice = None # For 'visible' slice (i.e., selected slice) -> should be updated everytime the slice is changed

    def set_scanner(self, scanner : 'Scanner'):
        '''
        Set the coil's scanner (i.e., the scanner to which it belongs)

        Parameters
        ----------
        scanner : Scanner
            The parameter being passed to set the scanner
        
        Returns
        -------
        TypeError
            If passed argument is not a scanner object
        '''

        from scanner import Scanner
        if type(scanner) != Scanner and type(scanner) != None:
            raise TypeError('Scanner object not passed as argument. Ensure passed argument is scanner object')
        
        self.scanner = scanner

    def plot_coil(self, ax : plt.axes, coil_focus : bool = False, seg_focus : int = None, seg_color='black') -> bool:
        '''
        Generate a 3D plot of a coil on a passed pyplot axis

        Parameters
        ----------
        ax : plt.axes
            Pyplot axis upon which to plot
        coil_focus : bool - Optional
            Boolean describing whether coil being plotted is a focus plot
        seg_focus : int - Optional
            Integer representing 
        
        Returns
        -------
        True
            If plotting is complete without problems
        '''

        for segment in self.segments:

            x_coords, y_coords, z_coords = segment.get_coords()

            ax.plot(x_coords, y_coords, z_coords, color = seg_color, lw = 2)

            # Add an arrow to the midpoint to give the direction
            n = len(x_coords) // 2
            o = n + 1
            ax.quiver(
                x_coords[n], y_coords[n], z_coords[n],
                x_coords[o] - x_coords[n], y_coords[o] - y_coords[n], z_coords[o] - z_coords[n],
                color = 'black', pivot = 'middle', length = 5
            )

        return True

    def add_segment(self, segment : Segment):
        '''
        Validate and append a passed segment to the coil attribute segments

        Parameters
        ----------
        segment : Segment
            Segment object to add

        Returns
        -------
        TypeError
            If passed argument is not a segment
        '''

        if type(segment) != Segment:
            raise TypeError('Segment object not passed as argument. Ensure passed argument is a segment object')

        self.segments.append(segment)
        segment.set_coil(self)

        # self.update_mag_vol()

    def B_volume(self) -> np.ndarray:
        ''' 
        Calculate the B field at every point in a volume resulting from a coil

        Given a variable l that represents the distance from the origin to a piece 
        of wire, integrate along that wire to find the B (magnetic) field at each
        point within a defined volume. The volume is bounded by a self.scanner.bbox and space
        is discretized based on the volume resolution.

        Returns
        -------
        np.ndarray
            4D volume of magnetic field components at each point in space. Last 
            dimension is size 3 representing x, y, and z components
        '''

        B_fields = []

        for segment in self.segments:
            B_fields.append(segment.seg_B)

        return sum(B_fields)

    def update_mag_vol(self):
        '''
        Updates self.B_vol to reflect the current B_volume

        Parameters
        ----------
        None

        Returns
        -------
        None

        '''

        if len(self.segments) > 0 and self.scanner is not None:
            self.B_vol = self.B_volume()

    def update_B_vol_slice(self, volume_coords : list):
        '''
        Updates self.B_vol_slice to reflect the current B_volume and slice


        '''
        pass
