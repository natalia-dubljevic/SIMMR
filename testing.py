from scanner import Scanner
from coil import Coil
import numpy as np
import sympy as smp
import matplotlib.pyplot as plt
from segment import Segment
from lines import Curved, Straight

# # # Code for testing:
# # coil1 = Coil(False)
# # coil1.coords = coil1.set_coords(np.array([[0,0,0], [1,0,0], [1,1,0], [0,1,0], [0,0,0]]))

# # coil2 = Coil(False)
# # coil2.coords = coil2.set_coords(np.array([[0,0,1], [1,0,1], [1,1,1], [0,1,1], [0,0,1]]))

# # bbox_test = [1.0, -5.0, -1.0, 6.0, 5.0, 1.0] # set bounding box; min and max of each of x, y, and z-coords ("frame" of magnetic field)
# # vol_res_test = [0.5, 0.5, 0.5] # volume resolution; "granularity" of map

# # test = Scanner(bbox_test, vol_res_test, [coil1, coil2])
# # test.plot_coils()

# # ------------------------------------------------------------------
# # PRESERVE - TEST CODE FOR CREATING CURVED SEGMENTS
# # centre = smp.Matrix([0, 1, 1])
# # dir_1 = smp.Matrix([1, 1, 0])
# # dir_2 = smp.Matrix([0, 2, 1])
# # t = smp.symbols('t')

# # print("initial matrices:")
# # print(centre)
# # print(dir_1)
# # print(dir_2)
# # print("done")

# # ellipse_fn = centre + dir_1 * smp.cos(t) + dir_2 * smp.sin(t)
# # print(ellipse_fn)

# # ellipse_fn_test = smp.lambdify(t, ellipse_fn, modules=['numpy'])

# # t_range = np.linspace(0, 2 * np.pi, 100)

# # x_coords, y_coords, z_coords = [], [], []

# # for element in t_range:
# #     x_coords.extend(ellipse_fn_test(element)[0])
# #     y_coords.extend(ellipse_fn_test(element)[1])
# #     z_coords.extend(ellipse_fn_test(element)[2])
# # END SECTION FOR CREATING CURVED SEGMENTS
# # ------------------------------------------------------------------

# t = smp.symbols('t')
# point = smp.Matrix([1, 1, 1])
# dir = smp.Matrix([0, 1, 1])

# straight_fn = point + t * dir

# straight_fn_test = smp.lambdify(t, straight_fn, modules=['numpy'])

# t_range = np.linspace(2, 4, 10)

# x_coords, y_coords, z_coords = [], [], []

# for element in t_range:
#     x_coords.extend(straight_fn_test(element)[0])
#     y_coords.extend(straight_fn_test(element)[1])
#     z_coords.extend(straight_fn_test(element)[2])

# # t, y = smp.symbols(['t', 'y'])
# # x = 0.05*t + 0.2/((y - 5)**2 + 2)
# # lam_x = smp.lambdify([t, y], x, modules=['numpy'])

# # x_vals = np.linspace(0, 10, 101)
# # y_vals = np.linspace(0, 10, 101)
# # z_vals = lam_x(x_vals, y_vals)

# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# ax.set_xlabel("$x$")
# ax.set_ylabel("$y$")
# ax.set_zlabel("$z$")

# ax.plot(x_coords, y_coords, z_coords, c = 'm')
# plt.tight_layout
# plt.show()

# -------------------------------------------------
# NEW TESTING - ENTIRE SCANNER SYSTEM (I THINK) ...
line1 = Curved(1, 1, 1, 0, 0, 1, 0, 1, 0)

test_seg1 = Segment(line1, 0, 2 * np.pi)

test_coil1 = Coil()

test_coil1.add_segment(test_seg1)

bbox = (1.0, -5.0, -1.0, 6.0, 5.0, 1.0) # set bounding box; min and max of each of x, y, and z-coords ("frame" of magnetic field)
vol_res = (0.5, 0.5, 0.5) # volume resolution; "granularity" of map

test_scanner = Scanner(bbox, vol_res)

test_scanner.add_coils(test_coil1)

test_scanner.plot_coils()

print("completed")