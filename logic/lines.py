import numpy as np
import sympy as smp
import matplotlib.pyplot as plt

class Curved:
    '''
    Class representing a curved line segment

    Attributes
    ----------
    fn : sympy.expr
        Sympy expression corresponding to the function describing the curved line (in 3D space)
    parameter : smp.symbols
        Sympy symbol corresponding to the parameter variable for the function
    '''

    def __init__(self, c_x : float, c_y : float, c_z : float,
                 r1_x : float, r1_y : float, r1_z : float,
                 r2_x : float, r2_y : float, r2_z : float):
        '''
        Initialize and generate the curved line function as an ellipse function; assumes
        that the two radii (i.e., r1 and r2) are perpendicular to each other

        Parameters
        ----------
        c_x : float
            X-coordinate of the centre of the ellipse
        c_y : float
            Y-coordinate of the centre of the ellipse
        c_z : float
            Z-coordinate of the centre of the ellipse
        r1_x : float
            X-component of the first radius vector (from the centre of the ellipse)
        r1_y : float
            Y-component of the first radius vector (from the centre of the ellipse)
        r1_z : float
            Z-component of the first radius vector (from the centre of the ellipse)
        r2_x : float
            X-component of the second radius vector (from the centre of the ellipse)
        r2_y : float
            Y-component of the second radius vector (from the centre of the ellipse)
        r2_z : float
            Z-component of the second radius vector (from the centre of the ellipse) 
        '''

        self.parameter = smp.symbols('t')

        centre = smp.Matrix([c_x, c_y, c_z])
        dir_1 = smp.Matrix([r1_x, r1_y, r1_z])
        dir_2 = smp.Matrix([r2_x, r2_y, r2_z])

        # UNDER CONSTRUCTION : MAKING SO THAT IT IS ALWAYS COUNTERCLOCKWISE

        rad1_v = dir_1
        rad2_v = dir_2
        norm_v = dir_1.cross(dir_2)

        t = smp.symbols('t')
        d_fn = smp.sqrt(
            (centre[0] + norm_v[0] * t) ** 2 +
            (centre[1] + norm_v[1] * t) ** 2 +
            (centre[2] + norm_v[2] * t) ** 2
        )

        diff_d_fn = smp.diff(d_fn, t)

        if diff_d_fn.subs(t, 0) > 0:
            tmp = dir_1
            dir_1 = dir_2
            dir_2 = tmp


        # END CONSTRUCTION ZONE
        
        self.fn = centre + dir_1 * smp.cos(self.parameter) + dir_2 * smp.sin(self.parameter)

class Straight:
    '''
    Class representing straight line segment

    Attributes
    ----------
    fn : sympy.expr
        Sympy expression corresponding to the function describing the straight line (in 3D space)
    parameter : smp.symbols
        Sympy symbol corresponding to the parameter variable for the function
    '''

    def __init__(self, p_x : float, p_y : float, p_z : float,
                 d_x : float, d_y : float, d_z : float): 
        '''
        Initialize and generate the straight line function

        Parameters
        ----------
        p_x : float
            X-coordinate of a point on the line
        p_y : float
            Y-coordinate of a point on the line
        p_z : float
            Z-coordinate of a point on the line
        d_x : float
            X-component of the direction vector
        d_y : float
            Y-component of the direction vector
        d_z : float
            Z-component of the direction vector
        '''

        self.parameter = smp.symbols('t')

        point = smp.Matrix([p_x, p_y, p_z])
        dir = smp.Matrix([d_x, d_y, d_z])

        self.fn = point + self.parameter * dir
