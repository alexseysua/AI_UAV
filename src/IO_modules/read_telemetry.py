# Дані з GPS та польотного контролеру надсилаються за визначеним
# драйвером протоколом через те, що у вільному доступі не було знайдено
# інформацію про роботу цього драйвера, цей скрипт виконано демонстративно.
# Для подальшої реалізації потрібно протестувати чи знайти протокол
# передачі даних, для коректного їх отримання від цих компонентів.

import serial, pynmea2


class ReaderTelemetries:
    def __init__(self):
        self.connGPS = serial.Serial(port='/dev/ttyS3',  # порт UART3 до якого підключений GPS
                                     baudrate=9600)  # Частота отримання даних, така ж як на GPS.
        self.connBar = serial.Serial(port='/dev/ttyS4',  # порт UART4 до якого підключений польотний контролер
                                     # Частота отримання даних, встановлена в налаштуваня польотного контролеру.
                                     baudrate=9600)

    def read_telemetry(self):
        received_data = {'latitude': 0, 'longitude': 0, 'altitude': 0}
        data_g = self.connGPS.readline().decode('latin1')
        data_g = pynmea2.parse(data_g)
        received_data['latitude'] = data_g.latitude()
        received_data['longitude'] = data_g.longtitude()

        data_b = self.connBar.readline()
        received_data['altitude'] = int.from_bytes(data_b)
        return received_data

    def __del__(self):
        self.connGPS.close()
        self.connBar.close()
