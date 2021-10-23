document.addEventListener("DOMContentLoaded", function(event) {
  RECORD.init()
});


RECORD = {
  url:  '/send_record_file_ajax',  // Url, на котором python принимает ogg файл и отдаёт данные в формате JSON
  status: false,  // Признак записи.

  init(){
    console.log('--- INIT ---')

      if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
          console.log('getUserMedia supported.');
          navigator.mediaDevices.getUserMedia ({ audio: true })

          // Success callback
          .then(function(stream) {
              console.log('Медиаустройства работают')

              /*
              var options = {
                mimeType: 'audio/webm;codecs=opus'
              }
              RECORD.mediaRecorder = new MediaRecorder(stream, options);
              */

              RECORD.mediaRecorder = new MediaRecorder(stream);

              // По мере записи нам нужно собирать аудиоданные. 
              // Мы регистрируем обработчик событий, чтобы сделать это, используя RECORD.mediaRecorder.ondataavailable:
              let chunks = [];

              RECORD.mediaRecorder.ondataavailable = function(e) {
                  chunks.push(e.data);
              }

              but_record = document.getElementById('record')
              but_record.onclick = RECORD.start_stop

              // Когда запись остановлена, stateсвойство возвращает значение «неактивно», и запускается событие остановки. 
              // Мы регистрируем для этого обработчик событий RECORD.mediaRecorder.onstopи завершаем там наш blob из всех полученных кусков:
              RECORD.mediaRecorder.onstop = function(e) {
                  console.log('Запись остановлена');
                  console.log('Mime-тип:', RECORD.mediaRecorder.mimeType)

                  // После этого мы создаем объединенный Blob из записанных звуковых фрагментов 
                  // const blob = new Blob(chunks, { 'type' : 'audio/ogg; codecs=opus' });
                  const blob = new Blob(chunks, { 'type' : 'audio/wav' });

                  // Отправляем на сервер
                  RECORD.ajax(blob)

                  // Очищаем массив кусков
                  chunks = [];
              }
          })

          .catch(function(err) {
              console.log('Ошибка подключения к getUserMedia: ' + err);
          });
      } else {
          console.log('getUserMedia не поддерживается браузером!');
      }
  },


  start_stop(){
      but_record = document.getElementById('record')

    // Меняем статус записи
      if (RECORD.status) {
        RECORD.status = false
      but_record.classList.remove('rec')
            RECORD.mediaRecorder.stop();
      } else {
        RECORD.status = true  
      but_record.classList.add('rec')

          RECORD.mediaRecorder.start();

        // Отключаем через 3.с
        setTimeout(function(){
            RECORD.status = false
          but_record.classList.remove('rec')
                RECORD.mediaRecorder.stop();    
        }, 3000);
      }
  },


  ajax(blob) {
    let form = new FormData()
    form.append('file', blob)
    let req = new XMLHttpRequest()
    req.open('post', RECORD.url, true);
    req.send(form)
    DAN.$('answer').innerHTML = 'Обработка'

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