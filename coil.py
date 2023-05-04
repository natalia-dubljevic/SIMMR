import sympy as smp
import matplotlib.pyplot as plt
import numpy as np

class Coil:
    '''
    A class used to represent the simulated scanners

    ...

    Attributes
    ----------
    piecewise : boolean
        Toggle for type of function required to plot coil (e.g., True for rectangle, False for circle)
    coords : np.array
        Numpy array containing a matrix representing the x-, y-, and z-coordinates in the first, second, and third column respectively
    
    Methods
    -------
    '''
    def __init__(self, piecewise : bool):
        self.piecewise = self.set_piecewise(piecewise)
        self.coords = self.set_coords

    def set_piecewise(self, piecewise : bool):
        '''
        Validate and return piecewise using passed boolean

        Parameters
        ----------
        piecewise : bool
            Boolean defining whether the function to model the coil is piecewise or not

        Returns
        -------
        ValueError
            If invalid parameter passed 
        piecewise
            If valid parameter passed
        '''

        # Verify passed parameter is boolean
        if not isinstance(piecewise, bool):
            raise ValueError("Must pass boolean to set piecewise")
        
        # Passed parameter valid, so return piecewise
        return piecewise
        
    def set_coords(self, coords : np.array):
        '''
        Validate and return coords using passed coords

        Parameters
        ----------
        coords : smp.Matrix
            Sympy matrix containing x, y, and z-coordinates of the coil

        Returns
        -------
        ValueError
            If passed matrix is invalid
        coords
            If passed matrix (coords) are valid coordinates
        '''
        
        # Verify correct number of columns (should be three, for the x-, y-, and z-coordinates)
        if np.shape(coords)[1] != 3:
            raise ValueError("Matrix describes incorrect number of coordinates (i.e., matrix should only have three columns)")
        
        # Passed parameter validated; return coords
        return coords
    
    # def plot_coil(self, filename : str) -> bool:
    def plot_coil(self, ax : plt.axes) -> bool:
        '''Save a 3D plot of a coil

        Parameters
        ----------

        Returns
        -------
        True
            If plot is generated and saved to the passed filename
        '''

        ax.plot(self.coords[:,0], self.coords[:,1], self.coords[:,2], c='m')
        return True
