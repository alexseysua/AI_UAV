from computer_vision import processing_image
from IO_modules import read_image, read_control_signal, read_telemetry, sent_control_signal, sent_image

list_last_positions = [0, 0, 0, 0]
cursor = 0

def update_last_position(coord):
    global cursor
    list_last_positions[0] = (coord)
    if cursor < 3:
        cursor += 1
    else:
        cursor = 0

def main():
    cap = read_image.CaptureImage()
    frame = cap.get_frame()
    model = processing_image.ObjectDetection
    model.predict(frame)

    vars = read_control_signal.ReaderVars()
    control_vars = vars.read_vars()

    telemetry = read_telemetry.ReaderTelemetries()
    update_last_position(telemetry.read_telemetry())

    close(cap, vars, telemetry)


def close(cap, vars, telemetry):
    cap.__del__()
    vars.__del__()
    telemetry.__del__()


if __name__ == '__main__':
    main()
