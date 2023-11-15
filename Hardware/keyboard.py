import cv2
import requests
import numpy as np

# Загрузка шаблонов и их соответствующих действий
templates = {
    'S': {'template': cv2.imread('arrow_up_template.png', 0), 'action': 'вперёд'},
    'W': {'template': cv2.imread('arrow_down_template.png', 0), 'action': 'назад'},
    'A': {'template': cv2.imread('arrow_right_template.png', 0), 'action': 'поворот на право'},
    'D': {'template': cv2.imread('arrow_left_template.png', 0), 'action': 'поворот на лево'},
    'Q': {'template': cv2.imread('stop_template.png', 0), 'action': 'стоять на месте'},
    'E': {'template': cv2.imread('camera_template.png', 0), 'action': 'снять фото'},
    'F': {'template': cv2.imread('action_template.png', 0), 'action': 'взаимодействие'},
    'G': {'template': cv2.imread('microphone_template.png', 0), 'action': 'запись звука'}
}

# Функция для обнаружения иконок на изображении
def detect_icons(image, templates):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    icons_positions = []

    for key, template_data in templates.items():
        template = template_data['template']
        h, w = template.shape[::-1]

        res = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8
        loc = np.where(res >= threshold)

        for pt in zip(*loc[::-1]):
            x, y = pt
            icons_positions.append({'icon': key, 'x': x, 'y': y, 'width': w, 'height': h})

    return icons_positions

def send_icons_data(icons_positions):
    url = 'http://your_server_url'
    response = requests.post(url, json=icons_positions)
    return response.json()

# Функция для объединения близких иконок
def merge_icons(icons_positions):
    merged_icons = []
    for icon in icons_positions:
        merged = False
        for merged_icon in merged_icons:
            if abs(icon['x'] - merged_icon['x']) <= 3 and abs(icon['y'] - merged_icon['y']) <= 3:
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
            print(merged_icons)
            print(sorted_icons)
            process_photo(frame)

    capture.release()
    cv2.destroyAllWindows()

# Запуск обработки кадров с камеры
process_camera_frames()
