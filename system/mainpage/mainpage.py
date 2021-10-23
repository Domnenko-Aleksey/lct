def mainpage(SITE):
    print('/system/mainpage/mainpage.py')

    SITE.addHeadFile('/lib/DAN/DAN.css')
    SITE.addHeadFile('/lib/DAN/DAN.js')
    SITE.addHeadFile('/templates/system/css/mainpage.css')
    SITE.addHeadFile('/templates/system/js/process.js')

    SITE.content = f'''
        <h1>Загрузить файлы</h1>
        <div class="dan_flex_row_start mainpage_input_container">
            <div class="mainpage_desc_input">Формат ".tif",<br>размер 5000 х 5000 пикс.</div>
            <div><input id="mainpage_tif_file" type="file"></div>
        </div>
        <div class="dan_flex_row_start mainpage_input_container">
            <div class="mainpage_desc_input">Формат ".tfw"</div>
            <div><input id="mainpage_tfw_file" type="file"></div>
        </div>
        <div class="mainpage_pt_20"><input id="mainpage_submit" class="dan_button_green" type="button" value="Отправить"></div>
        <div id="mainpage_download"></div>
        <div class="mainpage_out dan_flex_row">
            <div id="mainpage_source"></div>
            <div id="mainpage_result"></div>
        </div>
    '''
