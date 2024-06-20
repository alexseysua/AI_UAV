import math

import numpy as np

dict_PID_param = {
    'pitch': [4, 0.004, 0.4],
    'throttle': [4, 0.004, 0.4],
    'roll': [4, 0.004, 0.4],
    'yaw': [4, 0.004, 0.4],
}
prev_dangle = 0
prev_dh = 0
sum_e_angle = 0
sum_e_h = 0


def count_vector(a, b):
    return [b['latitude'] - a['latitude'], b['longitude'] - a['longitude']]


def count_angl(a, b):
    scalar = b[0] * a[0] + b[1] * a[1]
    modul_v_a = math.sqrt(a[0] ** 2 + a[1] ** 2)
    modul_v_b = math.sqrt(b[0] ** 2 + b[1] ** 2)
    return math.acos(scalar / (modul_v_a * modul_v_b))


def calculate_vmodul(v):
    return np.linalg.norm(v)


def sum_error(sum_prev, err):
    return sum_prev + err


def pid_reg(list_k, err):
    global prev_dangle, sum_e_angle
    t = 0.1
    err_p = prev_dangle
    sum_err = sum_error(sum_e_angle, err)
    p_i = list_k[0] * err
    i_i = list_k[1] * t * sum_err
    d_i = list_k[2] * (err - err_p) / t
    var = p_i + d_i + i_i
    prev_dangle = err
    return var


def pid_reg_h(list_k, err):
    global prev_dh, sum_e_h
    t = 0.1
    err_p = prev_dh
    sum_err = sum_error(sum_e_h, err)
    p_i = list_k[0] * err
    i_i = list_k[1] * t * sum_err
    d_i = list_k[2] * (err - err_p) / t
    var = p_i + d_i + i_i
    prev_dh = err
    return var


def generate_vars(list_last_positions, cursor, dict_vars):
    coords_n = list_last_positions[cursor - 1]
    coords_p = list_last_positions[cursor - 2]
    coords_0 = list_last_positions[cursor]
    v_n = count_vector(coords_p, coords_n)
    v_o = count_vector(coords_n, coords_0)
    angle = count_angl(v_n, v_o)
    if angle > 80:
        dict_vars['pitch'] *= -1
        dict_vars['roll'] *= -1

    pid_reg(dict_vars['pitch'], angle)
    pid_reg(dict_vars['roll'], angle)

    dh = coords_0[2] - coords_n[2]

    pid_reg_h(dict_vars['throttle'], dh)
    return dict_vars
