from scanner import Scanner
from coil import Coil
import numpy as np

# Code for testing:
coil1 = Coil(False)
coil1.coords = coil1.set_coords(np.array([[0,0,0], [1,0,0], [1,1,0], [0,1,0], [0,0,0]]))

coil2 = Coil(False)
coil2.coords = coil2.set_coords(np.array([[0,0,1], [1,0,1], [1,1,1], [0,1,1], [0,0,1]]))

bbox_test = [1.0, -5.0, -1.0, 6.0, 5.0, 1.0] # set bounding box; min and max of each of x, y, and z-coords ("frame" of magnetic field)
vol_res_test = [0.5, 0.5, 0.5] # volume resolution; "granularity" of map

test = Scanner(bbox_test, vol_res_test, [coil1, coil2])
test.plot_coils()

