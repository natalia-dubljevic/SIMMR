from scanner import Scanner
from coil import Coil
import numpy as np
import sympy as smp
import matplotlib.pyplot as plt
from segment import Segment
from lines import Curved, Straight
import sim_utils

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
# line1 = Curved(1, 1, 1, 0, 0, 1, 0, 1, 0)
# test_seg1 = Segment(line1, 0, 2 * np.pi)

# test_coil1 = Coil()
# test_coil1.add_segment(test_seg1)

# line2 = Straight(1, 1, 1, 1, 0, 0)
# test_seg2 = Segment(line2, 0, 1)
# line3 = Straight(2, 1, 1, 0, 1, 0)
# test_seg3 = Segment(line3, 0, 1)
# line4 = Straight(2, 2, 1, -1, 0, 0)
# test_seg4 = Segment(line4, 0, 1)
# line5 = Straight(1, 2, 1, 0, -1, 0)
# test_seg5 = Segment(line5, 0, 1)

# test_coil2 = Coil()
# test_coil2.add_segment(test_seg2)
# test_coil2.add_segment(test_seg3)
# test_coil2.add_segment(test_seg4)
# test_coil2.add_segment(test_seg5)

# line6 = Curved(1, 1, 0, -1, 0, 0, 0, -1, 0)
# test_seg6 = Segment(line6, 0, np.pi)
# line7 = Straight(0, 1, 0, 1, 1, 0)
# test_seg7 = Segment(line7, 0, 1)
# line8 = Straight(1, 2, 0, 1, -1, 0)
# test_seg8 = Segment(line8, 1, 0)

# test_coil3 = Coil()
# test_coil3.add_segment(test_seg6)
# test_coil3.add_segment(test_seg7)
# test_coil3.add_segment(test_seg8)

# bbox = (1.0, -5.0, -1.0, 6.0, 5.0, 1.0) # set bounding box; min and max of each of x, y, and z-coords ("frame" of magnetic field)
# vol_res = (0.5, 0.5, 0.5) # volume resolution; "granularity" of map

# test_scanner = Scanner(bbox, vol_res)

# test_scanner.add_coils(test_coil1)
# test_scanner.add_coils(test_coil2)
# test_scanner.add_coils(test_coil3)

# test_scanner.plot_coils()

# TESTING CHUNK COMPLETED
#---------------------------------------------------------------
# TESTING FOR SENSITIVITY MAP GENERATION

'''
bbox = [2.0, 6.0, -5.0, 5.0, -1.0, 1.0] # set bounding box; min and max of each of x, y, and z-coords ("frame" of magnetic field)
vol_res = [0.1, 0.1, 0.1] # volume resolution; "granularity" of map
radius = 0.5  # for circles (coil shape)

test_scanner = Scanner(bbox, vol_res)

c1 = Coil()
l1 = Curved(2, 0, 0, 0, 0.75, 0, 0, 0, 0.75)
s1 = Segment(l1, 0, 2 * np.pi)
c1.add_segment(s1)

c2 = Coil()
l2 = Curved(0, 0, 2, 0.75, 0, 0, 0, 0.75, 0)
s2 = Segment(l2, 0, 2 * np.pi)
c2.add_segment(s2)

c3 = Coil()
l3 = Curved(-2, 0, 0, 0, 0.75, 0, 0, 0, 0.75)
s3 = Segment(l3, 0, 2 * np.pi)
c3.add_segment(s3)

c4 = Coil()
l4 = Curved(0, 0, -2, 0.75, 0, 0, 0, 0.75, 0)
s4 = Segment(l4, 0, 2 * np.pi)
c4.add_segment(s4)

c5 = Coil()
l5 = Curved(1.5, 0, 1.5, -0.53, 0, 0.53, 0, -0.75, 0)
s5 = Segment(l5, 0, 2 * np.pi)
c5.add_segment(s5)

c6 = Coil()
l6 = Curved(-1.5, 0, 1.5, 0.53, 0, 0.53, 0, 0.75, 0)
s6 = Segment(l6, 0, 2 * np.pi)
c6.add_segment(s6)

c7 = Coil()
l7 = Curved(-1.5, 0, -1.5, -0.53, 0, 0.53, 0, -0.75, 0)
s7 = Segment(l7, 0, 2 * np.pi)
c7.add_segment(s7)

c8 = Coil()
l8 = Curved(1.5, 0, -1.5, 0.53, 0, 0.53, 0, 0.75, 0)
s8 = Segment(l8, 0, 2 * np.pi)
c8.add_segment(s8)

test_scanner.add_coils(c1)
test_scanner.add_coils(c2)
test_scanner.add_coils(c3)
test_scanner.add_coils(c4)
test_scanner.add_coils(c5)
test_scanner.add_coils(c6)
test_scanner.add_coils(c7)
test_scanner.add_coils(c8)

test_scanner.plot_coils()

B_field = c1.B_volume() # Choose which coil to generate B_field, etc. for 
'''

# B_complex = B_field[0, :, :, :] - 1j * B_field[1, :, :, :]


# slice = 'z'
# slice_loc = 0

# sim_utils.plot_mag_phase(B_complex, slice, slice_loc, vol_res=vol_res, bbox=bbox)
# sim_utils.plot_fields(B_field, slice, slice_loc, vol_res=vol_res, bbox=bbox)

# import multiprocessing

# print('Number of cpu:' + str(multiprocessing.cpu_count()))

# test_input = []
# for i in range(0, 10000):
#     test_input.append(i)

# print('test_input created')

# import time

# def task(test_input):
#     for num in test_input:
#         num **= num

# time_start = time.time()
# task(test_input)
# time_end = time.time()
# print('Not optimized: ' + str(time_end - time_start) + ' seconds')

# def pool():
#     with multiprocessing.Pool() as pool:
#         pool.map(task, test_input)

# time_start = time.time()
# pool()
# time_end = time.time()
# print('Optimized: ' + str(time_end - time_start) + ' seconds')

# volume_coords = [-1, 1, 0, 0, -1, 1]

# import numpy as np

# x_dim = np.arange(volume_coords[0], volume_coords[1] + 1e-10, 0.5)
# y_dim = np.arange(volume_coords[2], volume_coords[3] + 1e-10, 0.5)
# z_dim = np.arange(volume_coords[4], volume_coords[5] + 1e-10, 0.5)
# output = np.meshgrid(x_dim, y_dim, z_dim, indexing='ij')

# print(output)
# print(output[0].shape)

def check_palindrome(input : str):
    for i in range(len(input) // 2):
        if input[i] != input[len(input) - 1 - i]:
            return False
    return True

# print(check_palindrome('20022002'))

def find_smallest(ints : list):
    smallest = ints[0]
    for n in ints:
        if n < smallest:
            smallest = n
    return smallest

def sort(ints : list):
    sorted = []
    while len(ints) > 0:
        sorted.append(ints.pop(ints.index(find_smallest(ints))))
    return sorted

# print(sort([5, 2, 2, 1, 4]))  

from math import log

P = [0.36, 0.48, 0.16]
Q = [0.333, 0.333, 0.333]

def D(P, Q):
    result = 0
    for i in range(len(P)):
        result += P[i] * log(P[i] / Q[i])
    return result

def M(P, Q):
    result = []
    for i in range(len(P)):
        result.append(0.5 * (P[i] + Q[i]))
    return result

def JSD(P, Q):
    return 0.5 * D(P, M(P, Q)) + 0.5 * D(Q, M(P, Q))

print(JSD(P, Q))