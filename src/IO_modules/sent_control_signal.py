import serial

def sent(contorl_vars):
    connRX = serial.Serial(port='/dev/ttyS2',  # порт UART2 до якого підключений польотний контролер
                            # Частота передачі даних, встановлена в налаштуваня польотного контролеру.
                            baudrate=115200)
    for i in contorl_vars.values():
        connRX.write(i)
    connRX.close()