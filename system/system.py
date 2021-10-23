from aiohttp import web
from system.mainpage import mainpage
from system.docs import docs
from system.result import result
from system.delete import delete
from system.ajax import ajax

def router(SITE):
    print('PATH: /system/system.py')

    # Вызов функций по ключу
    functions = {
        '': mainpage.mainpage,
        'docs': docs.docs,
        'result': result.result,
        'delete': delete.delete,
        'image_upload_ajax': ajax.image_upload_ajax,
        'image_processing_ajax': ajax.image_processing_ajax,
        'image_to_shapefile': ajax.image_to_shapefile,
        'item_delete_ajax': ajax.item_delete_ajax
    }

    if (SITE.p[1] not in functions):
        # Если функция не существует - 404
        raise web.HTTPNotFound()

    # Вызов функции
    return functions[SITE.p[1]](SITE)
