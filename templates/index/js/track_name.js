document.addEventListener("DOMContentLoaded", function(event) {
	track_name()
});

function track_name(){
    let button = DAN.$('button_name')
    button.onclick = () => {
        console.log('SEND name AJAX')
        let form = new FormData()
        let name = DAN.$('track_name').value
        form.append('track_name', name)
        DAN.$('answer_name').innerHTML = 'Загрузка ...'
        DAN.ajax('/send_track_name_ajax', form, function(data){
            DAN.$('answer_name').innerHTML = data.content
        })
    }
}




