import sympy as smp


def create_sympy_circle(t: smp.core.symbol.Symbol, radius: int, plane: str, plane_loc=0, center=(0, 0)) -> smp.Matrix:
    if plane == 'x':
        return smp.Matrix([plane_loc, radius * smp.cos(t) + center[0], radius * smp.sin(t) + center[1]])
    elif plane == 'y':
        return smp.Matrix([radius * smp.cos(t) + center[0], plane_loc, radius * smp.sin(t) + center[1]])
    elif plane == 'z':
        return smp.Matrix([radius * smp.cos(t) + center[0], radius * smp.sin(t) + center[1], plane_loc])
