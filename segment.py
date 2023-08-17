import sympy as smp
from lines import Straight, Curved
import numpy as np

import b_calculation

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from coil import Coil

class Segment():
    '''
    A class used to represent a line segment as a sympy function

    Parameters
    ----------
    line_fn : Curved | Straight
        Line function (currently, only Straight and Curved are supported)
    low_lim : float
        The lower limit of the parameter for the calculation of the segment; integration limit
    up_lim : float
        The upper limit of the parameter for the calculation of the segment; integration limit

    Methods
    -------
    set_fn(self, fn : Curved | Straight) -> Curved | Straight
        Validate and set line function
    get_coords(self) -> list, list, list
        Generate 3D coordinates of segment
    '''

    def __init__(self, fn : Curved | Straight, low_lim : float, up_lim : float, coil : 'Coil' = None, seg_B : np.ndarray = None):
        '''
        Parameters
        ----------
        fn : Curved | Straight
            Either a curved or straight line function
        low_lim : float
            Low parameter (i.e., 't') limit to plot the segment in 3D space
        up_lim : float
            Upper parameter (i.e., 't') limit to plot the segment in 3D space
        coil : Coil
            Coil to which the segment 'belongs'
        '''
        self.coil = None
        self.line_fn = None
        self.seg_B = seg_B
        self.low_lim = low_lim
        self.up_lim = up_lim
        self.set_coil(coil)
        self.set_line_fn(fn)
        if type(self.seg_B) != np.ndarray:
            self.calc_seg_B()

    def validate_line_fn(self, fn : Curved | Straight) -> bool:
        '''
        Validate that fn is correct type 

        Parameters
        ----------
        fn : Curved | Straight
            Line object intended as the line_fn for the segment object

        Returns
        -------
        True
            If passed object is supported line type
        False
            If passed object is not supported line type
        '''

        if (type(fn) == Straight) | (type(fn) == Curved):
            return True
        else:
            return False

    def set_line_fn(self, fn : Curved | Straight) -> bool:
        '''
        Validate and set passed line as segment fn

        Parameters
        ----------
        fn : Curved | Straight
            Line object intended as the line_fn for the segment object

        Returns
        -------
        True
            If self.line_fn set 
        False
            Invalid fn passed 
        '''
        
        if self.validate_line_fn(fn):
            self.line_fn = fn
            return True
        else:
            return False
        
    def get_line_fn(self) -> Curved | Straight:
        '''
        Get the line_fn of the segment object

        Parameters
        ----------
        None

        Returns
        -------
        Curved | Straight
            Line function of the segment (i.e., self.line_fn)
        '''
        return self.line_fn

    def validate_coil(self, coil : 'Coil') -> bool:
        '''
        Validate passed object as voil type

        Parameters
        ----------
        coil : Coil
            Parameter being validated

        Returns
        -------
        True
            If passed object is coil type (or None)
        False
            If passed object is not coil type
        '''
        from coil import Coil
        if (type(coil) is Coil) or (coil is None):
            return True
        else:
            return False 

    def set_coil(self, coil : 'Coil'):
        '''
        Validate and set passed coil as self.coil

        Parameters
        ----------
        coil : Coil
            Coil being passed as the coil to which the segment 'belongs'
        
        Returns
        -------
        True
            If coil is valid and is set
        False
            If invalid type passed
        '''
      
        if self.validate_coil(coil):
            self.coil = coil
            return True
        else:
            return False
        
    def get_coil(self) -> 'Coil':
        '''
        Get the coil object to which the segment belongs

        Parameters
        ----------
        None

        Returns
        -------
        Coil
            The coil object to which it belongs (i.e., self.coil)
        '''

        return self.coil

    def get_coords(self):
        '''
        Get the x-, y-, and z-coordinates in 3D space of a segment object

        Returns
        -------
        list, list, list
            X-, y-, and z-coordinates of the segment
        '''
        t_range = np.linspace(self.low_lim, self.up_lim, 50)
        coords = [[], [], []]

        fn = smp.lambdify(self.line_fn.parameter, self.line_fn.fn, modules=['numpy'])

        for element in t_range:
            coords[0].extend(fn(element)[0])
            coords[1].extend(fn(element)[1])
            coords[2].extend(fn(element)[2])

        return coords[0], coords[1], coords[2]
    
    def calc_seg_B(self):
        '''
        Calculates the segments magnetic effect and sets it as self.seg_B
        '''
        fn = self.line_fn.fn

        x, y, z = smp.symbols(['x', 'y', 'z'])
        r = smp.Matrix([x, y, z])
        sep = r - fn

        t = self.line_fn.parameter

        # Define the integrand
        integrand = smp.diff(fn, t).cross(sep) / sep.norm()**3
        # Get the x, y, and z components of the integrand
        dBxdt = smp.lambdify([t, x, y, z], integrand[0])
        dBydt = smp.lambdify([t, x, y, z], integrand[1])
        dBzdt = smp.lambdify([t, x, y, z], integrand[2])

        # Add small tolerance to endpoint so it's included
        x_dim = np.arange(self.coil.scanner.bbox[0], self.coil.scanner.bbox[1] + 1e-10, self.coil.scanner.vol_res[0])
        y_dim = np.arange(self.coil.scanner.bbox[2], self.coil.scanner.bbox[3] + 1e-10, self.coil.scanner.vol_res[1])
        z_dim = np.arange(self.coil.scanner.bbox[4], self.coil.scanner.bbox[5] + 1e-10, self.coil.scanner.vol_res[2])
        xv, yv, zv = np.meshgrid(x_dim, y_dim, z_dim, indexing='ij')

        self.seg_B = b_calculation.B(self.low_lim, self.up_lim, dBxdt, dBydt, dBzdt, xv, yv, zv)
