import sympy as smp

def rotation_matrix(axis: str, angle: float) -> smp.Matrix:
    '''Produce matrices for rotation around a given axis.
    
    Produce matrices for counter-clockwise rotation around a given axis in 
    3D. Counter-clockwise is relative to the positive axis is facing the 
    observer.

    Parameters
    ----------
    axis : str
        The axis (x, y, or z) about which to rotate
    angle : float
        The angle in radians to rotate around a given axis
    
    Returns
    -------
    sympy.Matrix
        The 3x3 sympy rotation matrix associated with the desired rotation
    '''
    if axis.lower() =='x':
        return smp.Matrix([
                [1, 0, 0], 
                [0, smp.cos(angle), -1 * smp.sin(angle)], 
                [0, smp.sin(angle), smp.cos(angle)]
                ])
    
    elif axis.lower() =='y':
        return smp.Matrix([
                [smp.cos(angle), 0, smp.sin(angle)], 
                [0, 1, 0], 
                [-1 * smp.sin(angle), 0, smp.cos(angle)]
                ])
    
    elif axis.lower() == 'z':
        return smp.Matrix([
                [smp.cos(angle), -1 * smp.sin(angle), 0], 
                [smp.sin(angle), smp.cos(angle), 0], 
                [0, 0, 1]
                ])

    
def create_sympy_circle(t: smp.core.symbol.Symbol, radius: float, plane: str, 
                        plane_loc=0, center=(0, 0), rotate_angle=None, 
                        rotate_axis=None) -> smp.Matrix:
    ''' Return piecewise sympy matrices of x, y, z coordinates for a rectangle

    Parameters
    ----------
    t : sympy.core.symbol.Symbol
        Sympy symbol representing parameterizaiton parameter t
    radius : float
        The radius of the circle
    plane : str
        One of x, y, z. In the case of x=0, the plane is x
    plane_loc : float, optional
        The plane location. In the case of x=0, the location is 0
    center : tuple, optional
        The two coordinates indicating the center of the circle within its plane
    rotate_angle : float, optional
        The rotation angle the rectangle will be rotated around a given axis
    rotate_axis : str, optional
        The axis the rectangle is rotated around
    
    Returns
    -------
    sympy.Matrix
        A sympy matrix with the coordinates for a circle

    '''

    if plane.lower() == 'x':
        circle =  smp.Matrix([
                    plane_loc, 
                    radius * smp.cos(t) + center[0], 
                    radius * smp.sin(t) + center[1]
                    ])
    
    elif plane.lower() == 'y':
        circle =  smp.Matrix([
                    radius * smp.cos(t) + center[0], 
                    plane_loc, 
                    radius * smp.sin(t) + center[1]
                    ])
    
    elif plane.lower() == 'z':
        circle =  smp.Matrix([
                    radius * smp.cos(t) + center[0], 
                    radius * smp.sin(t) + center[1], 
                    plane_loc
                    ])
        
    if rotate_axis is not None:
        rot_matrix = rotation_matrix(rotate_axis, rotate_angle)
        circle = rot_matrix * circle
    
    return circle


def create_sympy_rectangle(t: smp.core.symbol.Symbol, height: float, 
                           width: float, plane: str, plane_loc=0, loc=(0, 0), 
                           rotate_angle=None, rotate_axis=None) -> smp.Matrix:
    ''' Return piecewise sympy matrices of x, y, z coordinates for a rectangle

    Parameters
    ----------
    t : sympy.core.symbol.Symbol
        Sympy symbol representing parameterization parameter t
    height : float
        The height of the rectangle
    width : float
        The width of the rectangle
    plane : str
        One of x, y, z. In the case of x=0, the plane is x
    plane_loc : float, optional
        The plane location. In the case of x=0, the location is 0
    loc : tuple, optional
        The two coordinates indicating the lower left corner of the rectangle 
        within its plane
    rotate_angle : float, optional
        The rotation angle the rectangle will be rotated around a given axis
    rotate_axis : str, optional
        The axis the rectangle is rotated around
    
    Returns
    -------
    list
        List of sympy Matrices. Each matrix contains the coordinates for one 
        side of the rectangle

    '''
    if plane.lower() == 'x':
        side_1 = smp.Matrix([
                plane_loc, 
                loc[0], 
                t * height + loc[1]
                ])
        
        side_2 = smp.Matrix([
                plane_loc, 
                t * width + loc[0], 
                loc[1] + height
                ])
        
        side_3 = smp.Matrix([
                plane_loc, 
                loc[0] + width, 
                t * height + loc[1]
                ])
        
        side_4 = smp.Matrix([
                plane_loc, 
                t * width + loc[0], 
                loc[1]
                ])

    elif plane.lower() == 'y':
        side_1 = smp.Matrix([
                t * height + loc[0], 
                plane_loc, 
                loc[1]
                ])
        
        side_2 = smp.Matrix([
                loc[0] + height, 
                plane_loc, 
                t * width + loc[1]
                ])
        
        side_3 = smp.Matrix([
                t * height + loc[0], 
                plane_loc, 
                loc[1] + width
                ])
        
        side_4 = smp.Matrix([
                loc[0], 
                plane_loc, 
                t * width + loc[1]
                ])
    
    elif plane.lower() == 'z':
        side_1 = smp.Matrix([
                loc[0], 
                t * height + loc[1], 
                plane_loc
                ])
        
        side_2 = smp.Matrix([
                t * width + loc[0], 
                loc[1] + height,
                plane_loc
                ])
        
        side_3 = smp.Matrix([
                loc[0] + width, 
                t * height + loc[1], 
                plane_loc
                ])
        
        side_4 = smp.Matrix([
                t * width + loc[0], 
                loc[1], 
                plane_loc
                ])

    if rotate_axis is not None:
        rot_matrix = rotation_matrix(rotate_axis, rotate_angle)
        side_1 = rot_matrix * side_1
        side_2 = rot_matrix * side_2
        side_3 = rot_matrix * side_3
        side_4 = rot_matrix * side_4

    return [side_1, side_2, side_3, side_4]