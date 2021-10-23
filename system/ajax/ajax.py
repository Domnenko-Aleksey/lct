import os
import glob
from pathlib import Path
import json
import fiona
import numpy as np
import matplotlib.pyplot as plt

import tensorflow as tf
import cv2


# Загрузка файла
def image_upload_ajax(SITE):
    print('PATH: /system/ajax.py -> image_upload_ajax')

    tif_file = SITE.post['tif_file'].file.read()
    tif_file_name = SITE.post['tif_file'].filename.lower()
    tfw_file = SITE.post['tfw_file'].file.read()

    # Сохраняем 'tif' файл
    with open('files/source/' + tif_file_name, 'wb') as f:
        f.write(tif_file)

    # Выделяем имя файла
    name = tif_file_name.split('.')[0]

    # Сохраняем 'tfw' файл
    with open('files/source/' + name + '.tfw', 'wb') as f:
        f.write(tfw_file)

    answer = {'answer': 'success', 'name': name}
    return {'ajax': json.dumps(answer)}


# Обработка файлов tif, tfw    
def image_processing_ajax(SITE):
    print('PATH: /system/ajax.py -> image_processing_ajax')

    # model = tf.keras.models.load_model('files/model/lod-segmentation_model.h5')  # Первая модель Артёма
    model = tf.keras.models.load_model('files/model/model_m/')  # Модель М
    # model.summary()

    name = SITE.post['name']

    # Загружаем изображение для анализа
    path = 'files/source/' + name + '.tif'
    img = cv2.imread(path)

    plt.figure(figsize=(6, 6))
    plt.imshow(img)
    plt.savefig('files/source/' + name + '.jpg')

    # Создаем пустой массив размером 25х512
    full_mask = np.zeros((5120, 5120))

    # Проходим по анализируемому изображению, вытаскивая участки размером 512х512
    for i in range(0, 5000, 512):
        print(f'Шаги обработки изображения: {i}')
        for j in range(0, 5000, 512):
            patch_img = img[i:i+512, j:j+512]
            patch = np.zeros((512, 512, 3))
            patch[:patch_img.shape[0], :patch_img.shape[1]] = patch_img
            
            # затем эти участки подаем в нейросеть
            pred = model.predict(np.expand_dims((patch / 127.5 -1), 0))
            
            # Заполняем соответствующие участки пустого массива предсказаниями нейросети,
            # Чтобы получить полную картину предсказания
            full_mask[i:i+512, j:j+512] = np.squeeze(pred)

    # Обрезаем лишнее и выводим на экран
    full_mask = full_mask[:5000, :5000]

    # Округление ответа модели по определенному порогу
    thresh = 0.5 # порог округления

    full_mask_round = full_mask.copy()
    full_mask_round[full_mask > thresh] = 1
    full_mask_round[full_mask < thresh] = 0
    plt.figure(figsize=(6, 6))
    plt.imshow(img)
    plt.imshow(full_mask_round, alpha=0.5)
    plt.savefig('files/result/' + name + '.jpg')

    # Cохранение предсказания в файл
    cv2.imwrite('files/result/' + name + '_mask.jpg', full_mask * 255)
    cv2.imwrite('files/result/' + name + '_mask_round.jpg', full_mask_round * 255)

    answer = {'answer': 'success', 'name': name}
    return {'ajax': json.dumps(answer)}


# Удаление элементов
def item_delete_ajax(SITE):
    print('PATH: /system/ajax.py -> item_delete_ajax')

    name = SITE.post['name']

    os.remove('files/source/' + name + '.jpg')
    os.remove('files/source/' + name + '.tif')
    os.remove('files/source/' + name + '.tfw')
    os.remove('files/result/' + name + '.jpg')
    os.remove('files/result/' + name + '_mask.jpg')
    os.remove('files/result/' + name + '_mask_round.jpg')
    os.remove('files/result/' + name + '.shp')
    os.remove('files/result/' + name + '.prj')
    os.remove('files/result/' + name + '.shx')
    os.remove('files/result/' + name + '.dbf')

    answer = {'answer': 'success'}
    return {'ajax': json.dumps(answer)}


# Переводим изображение в shapefile
def image_to_shapefile(SITE):
    print('PATH: /system/ajax.py -> image_to_shapefile')

    name = SITE.post['name']
    img_path_result = 'files/result/' + name + '_mask_round.jpg'

    img = cv2.imread(img_path_result) 
    t = 50
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(img_gray, t, 255, 0)
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Читаем метаданные из файла '.tfw'
    with open('files/source/' + name + '.tfw') as file:
        meta = [line.rstrip() for line in file]

    schema = {'geometry':'MultiLineString','properties':[('Name','str')]}
    shp = fiona.open('files/result/' + name + '.shp', mode='w', driver='ESRI Shapefile', schema = schema, crs = "EPSG:32637")

    for figure in contours:
        # Тут вместо 0 можно отсеять самые маленькие и незначительные фигуры, состоящие из 3-10 точек 
        if len(np.squeeze(figure).shape) > 1 and np.squeeze(figure).shape[0] > 0:
            figure = np.squeeze(figure)
            figure = find_point_on_map(figure, meta)
            rowDict = {
            'geometry' : {'type':'MultiLineString', 'coordinates': [figure]},
            'properties': {'Name' : None}
            }
            shp.write(rowDict)
    shp.close()


    answer = {'answer': 'success', 'name': name}
    return {'ajax': json.dumps(answer)}


# Функция конвертации пиксельных координат в географические исходя из метаданных обрабатываемого файла
def find_point_on_map(points, meta):
  Points = []
  A,C,D,B,E,F = float(meta[0]),float(meta[1]),float(meta[2]),float(meta[3]),float(meta[4]),float(meta[5])
  for x,y in points:
    Points.append(((A*x + C*x + E),(D*y + B*y + F)))
  return Points


# Оптимизатор для централизации градиента, ускоряющий процесс обучения
class GCAdam(tf.keras.optimizers.Adam):
    def get_gradients(self, loss, params):
        grads = []
        gradients = super().get_gradients()
        for grad in gradients:
            grad_len = len(grad.shape)
            if grad_len > 1:
                axis = list(range(grad_len - 1))
                grad -= tf.reduce_mean(grad, axis=axis, keep_dims=True)
            grads.append(grad)

        return grads