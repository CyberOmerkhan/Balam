
# Загрузка шаблонов и их соответствующих действий
import cv2
import requests
import numpy as np

import zmq
import json
import serial

# Создать контекст ZeroMQ
context = zmq.Context()

# Создать сокет типа REQ (запрос)
socket = context.socket(zmq.REQ)

# Установить соединение с сервером Raspberry Pi по его IP-адресу
server_ip = "10.0.0.214"  # Замените на IP-адрес вашего Raspberry Pi
server_port = "5555"
socket.connect(f"tcp://{server_ip}:{server_port}")



# Загрузка шаблонов и их соответствующих действий
templates = {
    'S': {'templates': [
            cv2.imread('arrow_up_template_1.png', 0),
            cv2.imread('arrow_up_template_2.png', 0),
            cv2.imread('arrow_up_template_3.png', 0),
            cv2.imread('resized_arrow_up_template_1.png', 0),
            cv2.imread('resized_1_arrow_up_template_1.png', 0),
            cv2.imread('resized_2_arrow_up_template_1.png', 0)
        ], 'action': 'вперёд'},
    'W': {'templates': [
            cv2.imread('arrow_down_template_1.png', 0),
            cv2.imread('arrow_down_template_2.png', 0),
            cv2.imread('arrow_down_template_3.png', 0),
            cv2.imread('resized_arrow_down_template_1.png', 0),
            cv2.imread('resized_1_arrow_down_template_1.png', 0),
            cv2.imread('resized_2_arrow_down_template_1.png', 0)
        ], 'action': 'назад'},
    'A': {'templates': [
            cv2.imread('arrow_right_template_1.png', 0),
            cv2.imread('arrow_right_template_2.png', 0),
            cv2.imread('arrow_right_template_3.png', 0),
            cv2.imread('resized_arrow_right_template_1.png', 0),
            cv2.imread('resized_1_arrow_right_template_1.png', 0),
            cv2.imread('resized_2_arrow_right_template_1.png', 0),

        ], 'action': 'поворот на право'},
    'D': {'templates': [
            cv2.imread('arrow_left_template_1.png', 0),
            cv2.imread('arrow_left_template_2.png', 0),
            cv2.imread('arrow_left_template_3.png', 0),
            cv2.imread('resized_arrow_left_template_1.png', 0),
            cv2.imread('resized_1_arrow_left_template_1.png', 0),
            cv2.imread('resized_2_arrow_left_template_1.png', 0)

        ], 'action': 'поворот на лево'},
    'Q': {'templates': [
            cv2.imread('stop_template_1.png', 0),
            cv2.imread('stop_template_2.png', 0),
            cv2.imread('stop_template_3.png', 0),
            cv2.imread('resized_stop_template_1.png', 0),
            cv2.imread('resized_1_stop_template_1.png', 0),
            cv2.imread('resized_2_stop_template_1.png', 0)
        ], 'action': 'стоять на месте'},
    'E': {'templates': [
            cv2.imread('camera_template_1.png', 0),
            cv2.imread('camera_template_2.png', 0),
            cv2.imread('camera_template_3.png', 0),
            cv2.imread('resized_camera_template_1.png', 0),
            cv2.imread('resized_1_camera_template_1.png', 0),
            cv2.imread('resized_2_camera_template_1.png', 0)
        ], 'action': 'снять фото'},
    'F': {'templates': [
            cv2.imread('action_template_1.png', 0),
            cv2.imread('action_template_2.png', 0),
            cv2.imread('action_template_3.png', 0),
            cv2.imread('resized_action_template_1.png', 0),
            cv2.imread('resized_1_action_template_1.png', 0),
            cv2.imread('resized_2_action_template_1.png', 0)
        ], 'action': 'взаимодействие'},
    'G': {'templates': [
            cv2.imread('microphone_template_1.png', 0),
            cv2.imread('microphone_template_2.png', 0),
            cv2.imread('microphone_template_3.png', 0),
            cv2.imread('resized_microphone_template_1.png', 0),
            cv2.imread('resized_1_microphone_template_1.png', 0),
            cv2.imread('resized_2_microphone_template_1.png', 0)
        ], 'action': 'запись звука'}
}

# Функция для обнаружения иконок на изображении
def detect_icons(image, templates):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    icons_positions = []

    for key, template_data in templates.items():
        for template in template_data['templates']:
            h, w = template.shape[::-1]

            res = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
            threshold = 0.8
            loc = np.where(res >= threshold)

            for pt in zip(*loc[::-1]):
                x, y = pt
                icons_positions.append({'icon': key, 'x': x, 'y': y, 'width': w, 'height': h})

    return icons_positions

# Остальные функции остаются без изменений

# Функция для объединения близких иконок
def merge_icons(icons_positions):
    merged_icons = []
    for icon in icons_positions:
        merged = False
        for merged_icon in merged_icons:
            if abs(icon['x'] - merged_icon['x']) <= 15 and abs(icon['y'] - merged_icon['y']) <= 15:
                merged_icon['x'] = min(icon['x'], merged_icon['x'])
                merged_icon['y'] = min(icon['y'], merged_icon['y'])
                merged_icon['width'] = max(icon['x'] + icon['width'], merged_icon['x'] + merged_icon['width']) - merged_icon['x']
                merged_icon['height'] = max(icon['y'] + icon['height'], merged_icon['y'] + merged_icon['height']) - merged_icon['y']
                merged = True
                break

        if not merged:
            merged_icons.append(icon)

    return merged_icons

# Функция для обработки фотографии

def process_photo(image):
    icons_positions = detect_icons(image, templates)
    merged_icons = merge_icons(icons_positions)

    # Отображение иконок на фотографии
    for icon_pos in merged_icons:
        x, y, w, h = icon_pos['x'], icon_pos['y'], icon_pos['width'], icon_pos['height']
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow('Photo', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Функция для обработки кадров с камеры
def process_camera_frames():
    capture = cv2.VideoCapture(0)

    while True:
        ret, frame = capture.read()

        if not ret:
            print('Ошибка при чтении кадра с камеры')
            break

        cv2.imshow('Camera', frame)

        key = cv2.waitKey(1)
        if key == ord('q'):
            break
        elif key == ord('g'):

            icons_positions = detect_icons(frame, templates)
            merged_icons = merge_icons(icons_positions)
            merged_icons.sort(key=lambda icon: (icon['y'], -icon['x']))

            # Формирование нового массива только с названиями иконок
            sorted_icons = [icon['icon'] for icon in merged_icons]
            sorted_icons.append("Q", "E")
            print("merged icons")
            print(merged_icons)
            print("sorted icons")
            print(sorted_icons)

            serialized_data = ','.join(map(str, sorted_icons)) + '\n'

            # Замените 'COMPORT' на имя COM-порта, к которому подключен ваш Bluetooth-модуль
            with serial.Serial('COM', 9600, timeout=1) as ser:
                ser.write(serialized_data.encode('utf-8'))
            process_photo(frame)
            # Запуск обработки кадров с камеры
            process_camera_frames()
            # Введите массив для отправки (как список Python)
            array = sorted_icons
            # Сериализовать массив в JSON-строку
            array_json = json.dumps(array)
            # Отправить JSON-строку серверу
            socket.send_string(array_json)
            # Получить ответ от сервера
            response = socket.recv_string()


    capture.release()
    cv2.destroyAllWindows()
process_camera_frames()
