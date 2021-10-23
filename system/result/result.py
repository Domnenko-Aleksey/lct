import os

def result(SITE):
    print('PATH: /system/result/result.py')

    SITE.addHeadFile('/lib/DAN/DAN.css')
    SITE.addHeadFile('/lib/DAN/DAN.js')
    SITE.addHeadFile('/templates/system/css/result.css')
    SITE.addHeadFile('/templates/system/js/result.js')

    tr_html = ''
    dir = 'files/result'
    files_list = os.listdir(dir)
    print('files_list:', files_list)
    num = 1
    for file_img in files_list:
        if file_img.endswith('_mask.jpg'):  # Получаем только готовые изображения с маской
            name = file_img.split('.')[0].replace('_mask', '')
            source_prev = '/files/source/' + name + '.jpg'  # Превью из исходников
            result_prev = '/files/result/' + name + '.jpg'  # Превью из результата
            result_mask = '/files/result/' + name + '_mask.jpg'  # Результат - маска           
            result_mask_round = '/files/result/' + name + '_mask_round.jpg'  # Результат - маска с округлением
            result_shp = '/files/result/' + name + '.shp'  # Shp

            tr_html += '<tr id="result_tr_' + name + '" class="result_tr">'
            tr_html +=      '<td>' + str(num) + '</td>'
            tr_html +=      '<td>' + name + '</td>'
            tr_html +=      '<td><img class="result_prev" src="' + source_prev + '"></td>'
            tr_html +=      '<td><img class="result_prev" src="' + result_prev + '"></td>'
            tr_html +=      '<td>'
            tr_html +=          '<a target="_blank" href="' + result_mask + '">'
            tr_html +=              '<svg class="result_svg"><use xlink:href="/templates/system/images/sprite.svg#map_6"></use></svg>'
            tr_html +=          '</a>'
            tr_html +=          '<img class="result_prev result_display_none" src="' + result_mask + '">'
            tr_html +=      '</td>'
            tr_html +=      '<td>'
            tr_html +=          '<a target="_blank" href="' + result_mask_round + '">'
            tr_html +=              '<svg class="result_svg"><use xlink:href="/templates/system/images/sprite.svg#map_6"></use></svg>'
            tr_html +=          '</a>'
            tr_html +=          '<img class="result_prev result_display_none" src="' + result_mask_round + '">'
            tr_html +=      '</td>'
            tr_html +=      '<td>'
            tr_html +=          '<a target="_blank" href="' + result_shp + '">'
            tr_html +=              '<svg class="result_svg"><use xlink:href="/templates/system/images/sprite.svg#map_10"></use></svg>'
            tr_html +=          '</a>'
            tr_html +=      '</td>'
            tr_html +=      '<td class="text_align_center"><svg class="result_svg result_delete_svg" data-name="' + name + '"><use xlink:href="/templates/system/images/sprite.svg#delete"></use></svg></td>'
            tr_html += '</tr>'
            num += 1

    SITE.content = f'''
        <h1>Результат</h1>
        <table class="admin_table dan_even_odd">
            <tr>
                <th style="width:50px">№</th>
                <th style="width:100px">Наименов.</th>
                <th style="width:100px">Прев. исх.</th>
                <th style="width:100px">Прев. рез.</th>
                <th style="width:50px">Рез.</th>
                <th style="width:50px">Рез_о.</th>
                <th>Shapefile</th>
                <th style="width:50px">Удал.</th>
            </tr>
            {tr_html}
        </table>
    '''
