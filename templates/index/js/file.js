document.addEventListener("DOMContentLoaded", function(event) {
	audio_file()
});

function audio_file(){
    let file_input = DAN.$('file')
    let button = DAN.$('button_file')
    file_input.onchange = check_file
    button.onclick = ()=>{
        if(!check_file())
            return
        send_ajax()
    }
}

function check_file(){
    let file = DAN.$('file').files
    if (file[0].size > 7000000) {
        alert('Размер исходного файла слишком большой ( > 7 MB ). Мы тестируем принцип работы на слабой машине без графического процессора. Не мучайте наш компьютер, пожалуйста!')
        return false
    }

console.log(file[0].type)

    if (!(file[0].type == 'audio/wav' || file[0].type == 'audio/mpeg'|| file[0].type == 'audio/mp3')) {
        alert('Неверный формат файла. Должен быть файл формата "wav" или "mp3", продолжительностью от 2 секунд')
        return false
    }
    return true
}

function send_ajax(){
    console.log('SEND FILE AJAX')
    let file = DAN.$('file').files[0]
    let form = new FormData()
    form.append('file', file)
    DAN.$('answer_file').innerHTML = 'Загрузка ...'
    DAN.ajax('/send_file_ajax', form, function(data){
        DAN.$('answer_file').innerHTML = data.content
    })
}