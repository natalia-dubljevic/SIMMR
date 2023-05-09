import matplotlib.pyplot as plt
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
    '''

    def __init__(self, bbox : list, vol_res : list):
        '''
        Parameters
        ----------
        bbox : list
            6-element list representing the bounding box for the scanner's magnetic field
        vol_res : list
            3-element list representing the volume resolution (the "granularity" of the simulated field)
        coils : list, optional
            List of the coils present in the simulated scanner; default is an empty list
        '''

        self.bbox = self.set_bbox(bbox)
        self.vol_res = self.set_vol_res(vol_res)
        self.coils = []
    
    def set_bbox(self, bbox: list):
        '''Validate and set self.bbox using passed list

        Parameters
        ----------
        bbox : list
            List of 6floats to set the bbox of the scanner object calling it

        Returns
        -------
        ValueError
            If invalid list passed for bbox
        bbox
            If valid list passed for bbox
        '''
        
        # Verify number of elements in list (should be 6)
        if len(bbox) != 6:
            raise ValueError("Incorect number of elements passed for bounding box; six elements should be passed")

        # Verify element type (should all be floats)
        for elements in bbox:
            if not isinstance(elements, float):
                raise ValueError("Incorrect element type passed for bounding box; all elements should be floats")
        
        # Correctly-formatted list passed, so return bbox
        return bbox
    
    def set_vol_res(self, vol_res : list):
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
        vol_res
            If valid list passed for vol_res
        '''
        
        # Verify number of elements in list (should be 3)
        if len(vol_res) != 3:
                raise ValueError("Incorrect number of elements passed for vol_res; three elements should be passed")
        
        # Verify element type (should all be floats)
        for elements in vol_res:
            if not isinstance(elements, float):
                    raise ValueError("INcorrect element type passed for vol_res; all elements should be floats")
            
        # Correctly-formatted list passed, so return vol_res
        return vol_res

    def plot_coils(self) -> bool:
        '''
        Plots all coils present in the scanner
        '''

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.set_xlabel("$x$")
        ax.set_ylabel("$y$")
        ax.set_zlabel("$z$")

        for coil in self.coils:
            coil.plot_coil(ax)

        plt.tight_layout()
        plt.show()

        print("coils plotted")
        
        return True
    
    def add_coils(self, coil : Coil):
        '''
        ADD DOCUMENTATION
        '''

        if type(coil) != Coil:
            raise TypeError('Ensure object passed as the argument is a coil')
        
        self.coils.append(coil)