def system(SITE):
    print('SYSTEM')
    SITE.addHeadFile('/lib/DAN/DAN.css')
    SITE.addHeadFile('/lib/DAN/DAN.js')
    SITE.addHeadFile('/templates/page/js/templates.js')
    SITE.addHeadFile('/templates/page/js/file.js')
    SITE.addHeadFile('/templates/page/js/track_name.js')

    # SITE.addHeadFile('/templates/page/js/record.js')
    # SITE.addHeadFile('/templates/page/js/record.js')



    SITE.content = '''
        <div class="flex_row">
            <div>
                <div id="switcher">
                    <input checked="checked" data-id="container_switcher_1" id="switcher_1" name="switcher" type="radio"><label for="switcher_1"><svg class="switcher_ico"><use xlink:href="/templates/page/svg/sprite.svg#download"></use></svg></label> 
                    <input data-id="container_switcher_2" id="switcher_2" name="switcher" type="radio"><label for="switcher_2"><svg class="switcher_ico"><use xlink:href="/templates/page/svg/sprite.svg#link"></use></svg></label> 
                    <input data-id="container_switcher_3" id="switcher_3" name="switcher" type="radio"><label for="switcher_3"><svg class="switcher_ico"><use xlink:href="/templates/page/svg/sprite.svg#search"></use></svg></label>
                </div>
                
                <div id="container_switcher_1" class="container_switcher">     
                    <div id="record" style="display:none;">
                        <div>REC.</div>
                    </div>
                    <div class="flex_row flex_center">
                        <label for="file">Поиск по файлу</label>
                        <input id="file" type="file">
                    </div>
                    <div class="flex_row">
                        <input id="button_file" class="button_custom" type="button" value="Отправить">
                    </div>
                    <div id="answer_file"></div>
                </div>
                
                
                <div id="container_switcher_2" class="container_switcher">     
                    <div class="flex_row flex_center">
                        <label for="url">Поиск по ссылке</label>
                        <input type="url" id="url" placeholder="В процессе разработки" pattern="https://.*" size="30" required>
                    </div>
                    <div class="flex_row">
                        <input id="button" class="button_custom" type="button" value="Отправить">
                    </div>
                    <div id="answer_link"></div> 
                </div>

                <div id="container_switcher_3" class="container_switcher">  
                    <div class="flex_row flex_center">
                        <label for="search">Поиск по названию композиции</label>
                        <input type="search" id="track_name" name="q" placeholder="Введите название композиции" > 
                    </div>          
                    <div class="flex_row">
                        <input id="button_name" class="button_custom" type="button" value="Отправить">
                    </div>
                    <div id="answer_name"></div>
                </div>
            </div>
        </div>
    <video id="bg_video" class="bg_video" preload="auto" autoplay="" loop="loop" muted="">
    <source src="/templates/page/files/bg.mp4" type="video/mp4">
    </video>

    <div class="bg_image"></div>

    <div class="company_name"><div>СОЮЗ</div></div>
    '''
