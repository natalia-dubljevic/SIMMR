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
        ADD DOCUMENTATION
        '''

        self.parameter = smp.symbols('t')

        centre = smp.Matrix([c_x, c_y, c_z])
        dir_1 = smp.Matrix([r1_x, r1_y, r1_z])
        dir_2 = smp.Matrix([r2_x, r2_y, r2_z])
        
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
        ADD DOCUMENTATION
        '''
        self.parameter = smp.symbols('t')

        point = smp.Matrix([p_x, p_y, p_z])
        dir = smp.Matrix([d_x, d_y, d_z])

        self.fn = point + self.parameter * dir
