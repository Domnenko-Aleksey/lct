def docs(SITE):
    print('/system/docs/docs.py')

    SITE.content = f'''
        <h1>Документы</h1>
        <a target="_blank" href="/files/pres.pdf">Презентация</a><br><br>
        <a target="_blank" href="/files/doc.pdf">Документация</a>
    '''
