import os

def delete(SITE):
    print('PATH: /system/delete/dlete.py')

    dir_list = ['files/result', 'files/source']
    f = 0  # Счётчик файлов
    for dir in dir_list:  # Папки второго уровня
      files_list = os.listdir(dir)
      for file in files_list:
        f += 1
        # if file.lower().endswith(file_type):  # Если это файл с нужным нам расширением
        path = dir + '/' + file
        os.remove(path)

    SITE.content = f'''
        <h1>Все файлы ({f}шт.) удалены</h1>
    '''
