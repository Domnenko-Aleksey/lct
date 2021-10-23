document.addEventListener("DOMContentLoaded", function(event) {
  RECORD.init()
});


RECORD = {
	url:  '/send_file_ogg_ajax',  // Url, на котором python принимает ogg файл и отдаёт данные в формате JSON
	status: false,  // Признак записи.

	init(){
		console.log('--- INIT ---')
		try {
			RECORD.audio_context = new AudioContext;
			console.log('Аудио контекст подключен.');
			console.log('navigator.getUserMedia ' + (navigator.getUserMedia ? 'доступен.' : 'отсутствует!'));
		} catch (e) {
			alert('Веб-аудио не поддерживается браузером!');
		}

		navigator.getUserMedia({audio: true}, startUserMedia, function(e) {
			console.log('Нет аудиопотока: ' + e);
		});

		but_record = document.getElementById('record')
        but_record.onclick = RECORD.start_stop  
	},


	start_stop(){
		but_record = document.getElementById('record')

		// Меняем статус записи
		if (RECORD.status) {
			RECORD.status = false
			but_record.classList.remove('rec')
		    RECORD.stop();
		} else {
			RECORD.status = true  
			but_record.classList.add('rec')

		  	RECORD.start();

			// Отключаем через 1.5с
			setTimeout(function(){
				RECORD.status = false
				but_record.classList.remove('rec')
			    RECORD.stop();    
			}, 1500);
		}
	},


	start(stream) {
	var input = RECORD.audio_context.createMediaStreamSource(stream);
		console.log('Медиа поток создан.');

		recorder = new Recorder(input);
		console.log('Рекордер запущен.');
	}


  ajax(blob) {
    let form = new FormData()
      form.append('file', blob)
    let req = new XMLHttpRequest()
    req.open('post', RECORD.url, true);
    req.send(form)

    req.onreadystatechange = function(){
      if(req.readyState == 4 && req.status == 200){
        console.log(req.responseText);
        var data = JSON.parse(req.responseText)
        if (data.answer == 'success') {
          DAN.$('answer').innerHTML = data.content
        } else
          console.log('Ошибка' + req.responseText)
      }
    }   
  }
}
