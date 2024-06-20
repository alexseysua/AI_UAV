from computer_vision import processing_image
from IO_modules import read_image, read_control_signal, read_telemetry, sent_control_signal, sent_image
from decision_making import execution_controller, prioritization
from forming_control_var import auto_attack_var, auto_return_var

list_last_positions = [{}, {}, {}, {}]
cursor = 0


def update_last_position(coord):
    global cursor
    list_last_positions[0] = coord
    if cursor < 3:
        cursor += 1
    else:
        cursor = 0


def main():
    cap = read_image.CaptureImage()
    frame = cap.get_frame()
    model = processing_image.ObjectDetection
    result_img_proc = model.predict(frame)

    vars = read_control_signal.ReaderVars()
    control_vars = vars.read_vars()
    telemetry = read_telemetry.ReaderTelemetries()
    update_last_position(telemetry.read_telemetry())

    res = execution_controller.controll(control_vars, result_img_proc)

    if res == 'simple':
        sent_control_signal.sent(control_vars)
        sent_image.sent(frame)
    elif res == 'return':
        sent_control_signal.sent(auto_return_var.generate_vars(list_last_positions, cursor, control_vars))
    else:
        sent_control_signal.sent(auto_attack_var.generate_vars(result_img_proc, control_vars))

    close(cap, vars, telemetry)


def close(cap, vars, telemetry):
    cap.__del__()
    vars.__del__()
    telemetry.__del__()


if __name__ == '__main__':
    main()
