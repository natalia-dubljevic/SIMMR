import sympy as smp

def create_sympy_circle(t: smp.core.symbol.Symbol, radius: int, plane: str, plane_loc=0, center=(0, 0)) -> smp.Matrix:
    if plane == 'x':
        return smp.Matrix([plane_loc, radius * smp.cos(t) + center[0], radius * smp.sin(t) + center[1]])
    elif plane == 'y':
        return smp.Matrix([radius * smp.cos(t) + center[0], plane_loc, radius * smp.sin(t) + center[1]])
    elif plane == 'z':
        return smp.Matrix([radius * smp.cos(t) + center[0], radius * smp.sin(t) + center[1], plane_loc])

    
def create_sympy_rectangle(t: smp.core.symbol.Symbol, height: float, width: float, plane: str, plane_loc=0, loc=(0, 0)) -> smp.Matrix:
    ''' Return piecewise sympy matrices of x, y, z coordinates that outline a rectangle
    '''
    if plane == 'x':
        side_1 = smp.Matrix([plane_loc, t * height + loc[0], loc[1]])
        side_2 = smp.Matrix([plane_loc, loc[0] + height, t * width + loc[1]])
        side_3 = smp.Matrix([plane_loc, t * height + loc[0], loc[1] + width])
        side_4 = smp.Matrix([plane_loc, loc[0], t * width + loc[1]])
        return [side_1, side_2, side_3, side_4]
    
    elif plane == 'y':
        side_1 = smp.Matrix([t * height + loc[0], plane_loc, loc[1]])
        side_2 = smp.Matrix([loc[0] + height, plane_loc, t * width + loc[1]])
        side_3 = smp.Matrix([t * height + loc[0], plane_loc, loc[1] + width])
        side_4 = smp.Matrix([loc[0], plane_loc, t * width + loc[1]])
        return [side_1, side_2, side_3, side_4]
    
    elif plane == 'z':
        side_1 = smp.Matrix([loc[0], t * height + loc[1], plane_loc])
        side_2 = smp.Matrix([t * width + loc[0], loc[1] + height,plane_loc])
        side_3 = smp.Matrix([loc[0] + width, t * height + loc[1], plane_loc])
        side_4 = smp.Matrix([t * width + loc[0], loc[1], plane_loc])
        return [side_1, side_2, side_3, side_4]