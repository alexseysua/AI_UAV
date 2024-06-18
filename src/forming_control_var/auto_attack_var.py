import cv2
from PIL import Image

const_d_y = 20
dict_PID_param = {
    'pitch': [4, 0.004, 0.4],
    'throttle': [4, 0.004, 0.4],
    'roll': [4, 0.004, 0.4],
    'yaw': [4, 0.004, 0.4],
}
prev_dy = 0
prev_dx = 0
sum_e_y = 0
sum_e_x = 0


def parameters_definition(result):
    is_need_fast = False
    width = result.boxes.orig_shape[1]
    height = result.boxes.orig_shape[0]
    x0 = result.boxes.xyxy[0][0].item()
    y0 = result.boxes.xyxy[0][1].item()
    x1 = result.boxes.xyxy[0][2].item()
    y1 = result.boxes.xyxy[0][3].item()
    distance_k = width / (x1 - x0) * height / (y1 - y0)
    r_border = width - x1
    l_border = x0
    t_border = y0
    b_border = height - y1
    if distance_k < 2:
        is_need_fast = True
    elif r_border < 100 or l_border < 100 or t_border < 100 or b_border < 100:
        is_need_fast = True

    d_x = (x0 + x1) / 2 - width / 2
    d_y = (y0 + y1) / 2 - height / 2 - const_d_y * distance_k

    # print(d_y)
    # a = int(width / 2 + d_x)
    # b = int(height / 2 - d_y)
    # cent = (a, b)
    # r = cv2.circle(result, cent, 1, (5,5,5), 1)
    # cv2.imshow("s", r)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    return [d_x, d_y, is_need_fast]


def inertial_k(dict_vars, name_var):
    return abs(dict_vars[name_var]) / 100 + 1


def sum_error(sum_prev, err):
    return sum_prev + err


def pid_reg(list_k, err, err_name):
    global prev_dx, prev_dy, sum_e_x, sum_e_y
    t = 0.12  # розраховано на основі поточної швидкодії виконання

    if err_name == 'x':
        err_p = prev_dx
        sum_err = sum_error(sum_e_x, err)
    else:
        err_p = prev_dy
        sum_err = sum_error(sum_e_y, err)

    p_i = list_k[0] * err
    i_i = list_k[1] * t * sum_err
    d_i = list_k[2] * (err - err_p) / t
    # print("error y =", err)
    # print("e", err, p_i, d_i, i_i)
    var = p_i + d_i + i_i
    if err_name == 'x':
        prev_dx = err
    else:
        prev_dy = err
    return var


def calculate_vars(dict_vars, list_param, r, t, p=None, y=None):
    err_x = list_param[0]
    err_y = list_param[0]
    if p is None and y is None:
        dict_vars[r] = pid_reg(dict_PID_param[r], err_x, 'x')
        dict_vars[t] = pid_reg(dict_PID_param[t], err_y, 'y')
    else:
        dict_vars[r] = pid_reg(dict_PID_param[r], err_x, 'x')
        dict_vars[t] = pid_reg(dict_PID_param[t], err_y, 'y')
        dict_vars[p] = pid_reg(dict_PID_param[p], -err_y / 2, 'y')
        dict_vars[y] = pid_reg(dict_PID_param[y], err_x / 2, 'x')


def generate_vars(result, dict_vars):
    list_param = parameters_definition(result)
    k_i_y = 0
    k_i_r = 0
    k_i_p = 0

    # усунення інерції на основі минулого значення змінних керування
    if list_param[0] > 0:
        if dict_vars['yaw'] < 0:
            k_i_y = inertial_k(dict_vars, 'yaw')
        if dict_vars['roll'] < 0:
            k_i_r = inertial_k(dict_vars, 'roll')
    else:
        if dict_vars['yaw'] > 0:
            k_i_y = inertial_k(dict_vars, 'yaw')
        if dict_vars['roll'] > 0:
            k_i_r = inertial_k(dict_vars, 'roll')

    if list_param[1] > 0:
        if dict_vars['pitch'] < 0:
            k_i_p = inertial_k(dict_vars, 'pitch')
    else:
        if dict_vars['pitch'] > 0:
            k_i_p = inertial_k(dict_vars, 'pitch')

    if list_param[2]:
        calculate_vars(dict_vars, list_param, 'roll', 'throttle', 'pitch', 'yaw')
        dict_vars['roll'] = dict_vars['roll'] * k_i_r
        dict_vars['yaw'] = dict_vars['yaw'] * k_i_y
        dict_vars['pitch'] = dict_vars['pitch'] * k_i_p
    else:
        calculate_vars(dict_vars, list_param, 'roll', 'throttle')
        dict_vars['roll'] = dict_vars['roll'] * k_i_r
        dict_vars['yaw'] = 0
        dict_vars['pitch'] = 0

    return dict_vars
