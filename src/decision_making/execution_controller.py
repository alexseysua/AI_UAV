from src.forming_control_var import auto_attack_var, auto_return_var

def controll(c_wars, result):
    if c_wars is None or c_wars['throttle'] == c_wars['yaw'] == c_wars['pitch'] == c_wars['roll']:
        if result is None:
            return 'return'
        else:
            return 'attack'
    elif c_wars['switch1'] == 100 and result is not None:
        return 'attack'
    else:
        return 'simple'
