import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
from coil import Coil

class Scanner:
    '''
    A class used to represent the simulated scanner

    ...

    Attributes
    ----------
    bbox : list
        A 6-element tuple representing the bounding box for the scanner's magnetic field
    vol_res : list
        Volume resolution; the "granularity" of the simulated field
    coils : list
        List of coils present in the simulated scanner

    Methods
    -------
    set_bbox(self, bbox : list) -> list
        Validate and return passed list for setting bbox
    set_vol_res(self, vol_res : list) -> list
        Validate and return passed list for setting vol_res
    plot_coils(self) -> bool
        3D plot all coils present in the scanner; return True if successful
    add_coils(self, coil : Coil) -> bool
        Validate and add passed coil to the list of coils present in the scanner
    '''

    def __init__(self, bbox : list, vol_res : list, coils : list[Coil] = []):
        '''
        Parameters
        ----------
        bbox : list
            6-element list representing the bounding box for the scanner's magnetic field
            (x-min, x-max, y-min, y-max, z-min, z-max)
        vol_res : list
            3-element list representing the volume resolution (the "granularity" of the simulated field)
        coils : list, optional
            List of the coils present in the simulated scanner; default is an empty list
        '''

        self.bbox = None
        self.set_bbox(bbox)
        self.vol_res = None
        self.set_vol_res(vol_res)
        self.coils = coils
    
    def set_bbox(self, bbox : list):
        '''Validate and set self.bbox using passed list

        Parameters
        ----------
        bbox : list
            List of 6 floats to set the bbox of the scanner object calling it

        Returns
        -------
        ValueError
            If invalid list passed for bbox
        '''
        
        if len(bbox) != 6:
            raise ValueError("Incorect number of elements passed for bounding box; six elements should be passed")

        for elements in bbox:
            if not isinstance(elements, float):
                raise ValueError("Incorrect element type passed for bounding box; all elements should be floats")
        
        self.bbox = bbox

    def get_bbox(self) -> list:
        '''
        Get the scanner's bounding box

        Parameters
        ----------
        None

        Returns
        -------
        self.bbox : list
        '''

        return self.bbox
    
    def set_vol_res(self, vol_res : list) -> list:
        '''
        Set self.vol_res using passed list
        INQUIRE: SHOULD VALIDATION BE PRESENT (beyond size of list and type float)

        Parameters
        ----------
        vol_res : list
            List of 3 floats to set the vol_res of the scanner object calling it

        Returns
        -------
        ValueError
            If invalid list passed for vol_Res
        '''

        if len(vol_res) != 3:
                raise ValueError("Incorrect number of elements passed for vol_res; three elements should be passed")

        for elements in vol_res:
            if not isinstance(elements, float):
                    raise ValueError("INcorrect element type passed for vol_res; all elements should be floats")
            
        self.vol_res = vol_res

    def get_vol_res(self) -> list:
        '''
        Get the scanner's volume resolution

        Parameters
        ----------
        None

        Returns
        -------
        self.vol_res : list
        '''

        return self.vol_res

    def plot_coils(self) -> bool:
        '''
        Plots all coils present in the scanner

        Returns
        -------
        True
            If coils successfully plotted
        '''

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.set_xlabel("$x$")
        ax.set_ylabel("$y$")
        ax.set_zlabel("$z$")

        for coil in self.coils:
            coil.plot_coil(ax)

        plt.tight_layout()
        plt.gca().set_aspect('equal')
        plt.show()
        
        return True
    
    def add_coils(self, coil : Coil):
        '''
        Validate and append passed coil to list of coils present in the scanner object

        Parameters
        ----------
        coil : Coil
            Coil to add to the list of coils 
        '''

        if type(coil) != Coil:
            raise TypeError('Ensure object passed as the argument is a coil')
        
        self.coils.append(coil)
        coil.set_scanner(self) 
    
    def del_coils(self, coil : Coil):
        '''
        Remove the pointed to coil from the list of coils present in the scanner object

        Parameters
        ----------
        coil : Coil
            Pointer to the coil to be removed from the list of coils
        '''
        
        if type(coil) != Coil:
            raise TypeError('Ensure object passed as the argument is a coil')
        
        self.coils.remove(coil)
        coil.scanner = None
    
    def get_coils(self, index : int) -> Coil:
        '''
        Get a coil by index number

        Parameters
        ----------
        index : int
            Index number of coil requested
        '''

        if index >= len(self.coils):
            raise ValueError('Requested index does not exist')
        
        return self.coils[index]