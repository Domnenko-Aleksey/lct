document.addEventListener("DOMContentLoaded", ()=>{
	RESULT.init()
});

RESULT = {
    init(){
        // Фотогалерея на отдельную строку
        let tr = document.getElementsByClassName('result_tr')
        for (let i = 0; i < tr.length; i++) {
            DAN.show('result_prev', tr[i].id) 
        }

        let del = document.getElementsByClassName('result_delete_svg')
        for (let i = 0; i < del.length; i++) {
            del[i].onclick = RESULT.del
        }
    },

    del(){
        let svg = this
        let name = svg.dataset.name
        let tr = svg.parentNode.parentNode
        tr.remove()

        var form = new FormData()
		form.append('name', name)
        DAN.ajax('/system/item_delete_ajax', form, (data) => {
            console.log('Файлы удалены')
		})
    }
}