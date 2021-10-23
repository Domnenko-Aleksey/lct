document.addEventListener("DOMContentLoaded", ()=>{
	PROCESS.init()
});

const PROCESS = {
	init() {
		DAN.$('mainpage_submit').onclick = PROCESS.files_upload
		DAN.$('mainpage_tif_file').oninput = () => PROCESS.image_check('tif')
		DAN.$('mainpage_tfw_file').oninput = () => PROCESS.image_check('tfw')
	},


	// Добавить изображение
	files_upload(e){
		console.log('FILES UPLOAD')

		if (!PROCESS.image_check('tif') || !PROCESS.image_check('tfw'))
			return
		
		let input_tif_file = DAN.$('mainpage_tif_file')
		let tif_file = input_tif_file.files[0]

		let input_tfw_file = DAN.$('mainpage_tfw_file')
		let tfw_file = input_tfw_file.files[0]

		console.log(tif_file.name, ' --- ', tfw_file.name)
		// Проверка того, что имена (до расширения) у файлов одинаковые
		if (tif_file.name.split('.')[0].toLowerCase() != tfw_file.name.split('.')[0].toLowerCase()) {
			alert('Не совпадают имена файлов: ' + tif_file.name + ' и ' + tfw_file.name)
			return
		}

		var form = new FormData()
		form.append('tif_file', tif_file)
		form.append('tfw_file', tfw_file)
		DAN.modal.spinner()

		DAN.ajax('/system/image_upload_ajax', form, (data) => {
			DAN.modal.add('Файлы с именем <b>' + data.name + '</b> загружены. <br><br>Приступаем к обработке файла. Подождите 1-2 минуты.')
			PROCESS.image_processing(data.name)
		})
	},


	// Проверка типа и размера файла
	image_check(type){
		let files = ''
		if (type == 'tif') {
			if (DAN.$('mainpage_tif_file').files.length == 0) {
				alert('Не выбран файл tif')
				return false				
			}

			files = DAN.$('mainpage_tif_file').files

			if (files[0].size > 100000000) {
				alert('Размер исходного изображения слишком большой')
				return false
			}
	
			if (files[0].type != 'image/tiff') {
				alert('Неверный формат файла, должен быть tif')
				return false
			}
		} else if (type == 'tfw') {
			if (DAN.$('mainpage_tfw_file').files.length == 0) {
				alert('Не выбран файл tfw')
				return false				
			}
			let file_name = DAN.$('mainpage_tfw_file').files[0].name

			if (file_name.split('.')[1].toLowerCase() != 'tfw') {
				alert('Неверный формат файла, должен быть tfw')
				return false
			}
		} else {
			return false
		}

		return true
	},


	// Обработка файла
	image_processing(name){
		var form = new FormData()
		form.append('name', name)
		DAN.ajax('/system/image_processing_ajax', form, (data) => {
			links = '<div id="mainpage_download_links">' +
						'<a target="_blank" href="/files/result/' + data.name + '_mask.jpg">Результат 5000 х 5000 px</a><br>' +
						'<a target="_blank" href="/files/result/' + data.name + '_mask_round.jpg">Результат "round"</a><br>' +
					'</div>'
			DAN.$('mainpage_download').innerHTML = links
			DAN.$('mainpage_source').innerHTML = '<img src="/files/source/' + data.name + '.jpg" alt-"">'
			DAN.$('mainpage_result').innerHTML = '<img src="/files/result/' + data.name + '.jpg" alt-"">'
			DAN.modal.update('Шаг 3. Создание shape файла.')
		
			PROCESS.shapefile_processing(data.name)
		})
	},


	// Создание shapefile
	shapefile_processing(name){
		var form = new FormData()
		form.append('name', name)
		DAN.ajax('/system/image_to_shapefile', form, (data) => {
			let link = '<a target="_blank" href="/files/result/' + data.name + '.shp">Shapefile</a><br>' 
			DAN.$('mainpage_download_links').innerHTML += link

			DAN.modal.del()
		})
	}
}