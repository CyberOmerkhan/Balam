import serial

data = ["W","W","W","A","Q","E"]
serialized_data = ','.join(map(str, data)) + '\n'

# Замените 'COMPORT' на имя COM-порта, к которому подключен ваш Bluetooth-модуль
with serial.Serial('COM9', 9600, timeout=1) as ser:
    ser.write(serialized_data.encode('utf-8'))
    # мне надо алгоритмы изучить и матан
