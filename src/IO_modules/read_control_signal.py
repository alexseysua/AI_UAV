# Дані з приймача надсилаються за визначеним драйвером протоколом
# через те, що у вільному доступі не було знайдно інформацію про
# роботу цього драйвера, цей компонент виконано демонстративно.
# Для подальшої реалізації потрібно протестувати чи знайти протокол
# передачі даних, для коректного їх отримання.

import serial


class ReaderVars:
    def __init__(self):
        self.conn = serial.Serial(port='/dev/ttyS0',  # порт UART до якого підключений приймач
                             baudrate=115200)  # Частота отримання даних, така ж як на приймачу.

    def read_vars(self):
        data_labels = ['throttle', 'yaw', 'pitch', 'roll', 'switch1', 'switch2']
        received_data = {}
        for i in range(6):
            data = int.from_bytes(self.conn.read(8))
            received_data[data_labels[i]] = data
        return received_data

    def __del__(self):
        self.conn.close()
