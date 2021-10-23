import time
import sys
import base64
from cryptography import fernet
import jinja2
import aiohttp_jinja2
from aiohttp import web
from aiohttp_session import setup, get_session, session_middleware
from aiohttp_session.cookie_storage import EncryptedCookieStorage
# import pymysql
# import pymysql.cursors
sys.path.append('classes')
sys.path.append('system')
sys.path.append('page')
from Site import Site
from page import page
from system import system
from auth import auth



@aiohttp_jinja2.template('index/index.html')
async def index_r(request):
    # Основной режим вывода содержимого
    print('===== INDEX =====')

    SITE = site(request)

    session = await get_session(request)
    SITE.post = await request.post()

    # r = page.router(SITE)
    r = auth.auth(SITE)

    # Обработка редиректа
    if r and 'redirect' in r:
        return web.HTTPFound(r['redirect'])

    # Обработка ajax
    if r and 'ajax' in r:
        return web.HTTPOk(text=r['ajax'])

    return {'AUTH': SITE.auth, 'content': SITE.content, 'head': SITE.getHead(), 'test_1': 'TEST 1', 'test_2': 'TEST 2'}



async def ws(request):
    # Веб-сокеты
    pass



@aiohttp_jinja2.template('system/main.html')
async def system_r(request):
    # Админка
    print('===== SYSTEM =====')
    SITE = site(request)

    SITE.post = await request.post()  # Ждём получение файлов методом POST
    SITE.session = await get_session(request)

    SITE.auth = 1 if 'auth' in SITE.session else 0  # Статус авторизации - 1, если есть сессия

    # Авторизация на сайте
    if (SITE.auth == 0):
        r = auth.auth(SITE)
        # Обработка редиректа
        if r and 'redirect' in r:
            return web.HTTPFound(r['redirect'])
        return {'AUTH': SITE.auth, 'content': SITE.content, 'head': SITE.getHead()}

    r = system.router(SITE)

    # Обработка редиректа
    if r and 'redirect' in r:
        return web.HTTPFound(r['redirect'])
    
    # Обработка ajax
    if r and 'ajax' in r:
        return web.HTTPOk(text=r['ajax'])

    return {'AUTH': SITE.auth, 'content': SITE.content, 'head': SITE.getHead()}



def site(request):
    '''
    con = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        db='dan_py',
        charset='utf8mb4',
        autocommit=True,
        cursorclass=pymysql.cursors.DictCursor
    )
    '''
    SITE = Site()
    # SITE.db = con.cursor()

    # path = request.match_info.get('url', '')
    path = request.path
    SITE.path = path
    SITE.p = path[1:].split('/')
    i = len(SITE.p)
    while i < 7:
        SITE.p.append('')
        i += 1
    SITE.request = request
    return SITE



app = web.Application(client_max_size=1024**100)

# Установка сессий
fernet_key = fernet.Fernet.generate_key()
secret_key = base64.urlsafe_b64decode(fernet_key)
setup(app, EncryptedCookieStorage(secret_key))

aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))
app.add_routes([web.static('/lib', 'lib'),
                web.static('/templates', 'templates'),
                web.static('/files', 'files'),
                web.get('/ws', ws),  # Веб-сокеты
                web.get('/system{url:.*}', system_r),  # Админка
                web.post('/system{url:.*}', system_r),  # Админка
                web.get('/{url:.*}', index_r),
                web.post('/{url:.*}', index_r)])

if __name__ == '__main__':
    web.run_app(app, port=9999)










