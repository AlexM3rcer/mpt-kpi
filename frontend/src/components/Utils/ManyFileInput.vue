<template>
	<label for="files" ref="root" class="wrap input" :class="{dragging: dragging}">
		<div class="inner">
			<add-icon />
			<div class="description">
				для загрузки сертификатов перетащите<br />
				файлы или нажмите на область
			</div>
		</div>
		<div class="uploaded_certificates">
		</div>
	</label>
	<input
		id="files"
		type="file"
		style="display: none"
		multiple
		accept="image/png, image/gif, image/jpeg, application/pdf, application/vnd.openxmlformats-officedocument.wordprocessingml.document"
		@change="uploadFilesList($event.target.files)"
	/>
</template>

<script>
import axios from 'axios'
import AddIcon from '@/components/Icons/AddIcon.vue'

export default {
	emits: ['drop'],

	components: {
		AddIcon,
	},

	data() {
		return {
			files: [],
			dragging: false,
			dropArea: false,
			count: 0,
		}
	},

	watch: {
		dragging(val) {
			if (!this.dropArea) return
			if (val) {
				this.dropArea.classList.add('DragNDrop_area')
			} else {
				this.dropArea.classList.remove('DragNDrop_area')
			}
		},
	},

	mounted() {
		this.dropArea = this.$refs.root
		if (!this.dropArea) return

		this.dropArea = this.dropArea.parentElement
		this.dropArea.addEventListener('dragstart', this.dragstart, false)
		this.dropArea.addEventListener('dragenter', this.dragenter, false)
		this.dropArea.addEventListener('dragleave', this.dragleave, false)
		this.dropArea.addEventListener('dragover', this.dragover, false)
		this.dropArea.addEventListener('drop', this.drop, false)
	},

	methods: {
		dragenter(e) {
			let haveFiles = false

			if (e.dataTransfer.types) {
				for (let i = 0; i < e.dataTransfer.types.length; i++) {
					if (e.dataTransfer.types[i] === 'Files') {
						haveFiles = true
					}
				}
			}

			if (!haveFiles) return

			e.preventDefault()
			this.count++
			this.dragging = true
		},

		dragleave() {
			this.count--
			if (this.count === 0) {
				this.dragging = false
			}
		},

		dragstart(e) {
			console.log('dragstart')
			e.stopPropagation()
			this.count = 0
		},

		dragover(e) {
			e.preventDefault()
			e.stopPropagation()
		},

		drop(e) {
			e.preventDefault()
			e.stopPropagation()
			this.dragging = false
			this.count = 0

			const allowedTypes = ['image/jpeg', 'image/png', 'application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
    		const files = e.dataTransfer.files;
			const validFiles = [];

			for (let i = 0; i < files.length; i++) {
				if (allowedTypes.includes(files[i].type)) {
					validFiles.push(files[i]);
				} else {
					alert(`Файл "${files[i].name}" не поддерживается. Разрешены только файлы форматов JPG, PNG, PDF и DOCX.`);
				}
			}

			if (validFiles.length > 0) {
				this.uploadFilesList(validFiles);
			}
		},

		async uploadFile(file) {
			console.log('uploading file')
			console.log(file)

			const formData = new FormData()
			formData.append('file', file)

			const url = '/api/media/'
			return axios.post(url, formData)
		},

		uploadFilesList(files) {
			if (!files?.length) return
			files = Array.from(files)
			const inputContainer = document.querySelector('.inner')
			const imageContainer = document.querySelector('.uploaded_certificates')

			for (const file of files) {
				// const item = {
				// 	type: 'image',
				// 	isLoading: true,
				// 	media: {
				// 		src: URL.createObjectURL(file),
				// 		name: file.name,
				// 	},
				// }
				// this.files.push(item)

				this.uploadFile(file)
					.then((uploadFileInfo) => {
						console.log(uploadFileInfo)

						const imgElement = document.createElement('img')
						imgElement.classList.add('popup_file')
						imgElement.src = uploadFileInfo.data.url
						imgElement.alt = uploadFileInfo.data.original_name
						imgElement.style.maxWidth = '10em'
						imgElement.style.height = '8em'
						imgElement.style.padding = '1em'
						imgElement.style.borderRadius = '1em'

						const imgLabel = document.createElement('p')
						imgLabel.textContent = uploadFileInfo.data.original_name
						imgLabel.style.maxWidth = '7em'

						const imgBox = document.createElement('div')
						imgBox.style.display = 'flex'
						imgBox.style.padding = '0 0.5 0'
						imgBox.style.flexFlow = 'column nowrap'
						imgBox.style.width = '10em'
						imgBox.style.height = '10em'
						imgBox.style.whiteSpace = 'nowrap'
						imgBox.style.overflow = 'hidden'
						imgBox.style.textOverflow = 'ellipsis'
						imgBox.style.flexShrink = '0'
						imgBox.style.justifyContent = 'center'
						imgBox.style.alignItems = 'center'
						imgBox.appendChild(imgElement)
						imgBox.appendChild(imgLabel)

						imageContainer.appendChild(imgBox)

						inputContainer.style.display = 'none'

						this.files.push(uploadFileInfo.data)

						// item.isLoading = false

						this.$emit('files-sent', this.files);
					})
					.catch(() => {
						this.uploadError = true

						// item.isLoading = false
					})
				if (this.uploadError) return
			}
		},
	},
}
</script>

<style lang="sass" scoped>
.wrap {
 padding: 2rem 2rem 0.5rem;
 background-color: #CCDEF1;
 border: 2px dashed #6D747C;
}

.wrap.dragging {
 background-color: #CCDEF177;
}

.dragging {
 opacity: 1;
}

.inner {
 display: flex;
 align-items: center;
 justify-content: center;
 flex-direction: column;
 color: var(--white);
 gap: .8rem;
}

.description {
 color: #6D747C;
}

.uploaded_certificates {
	display: flex;
	justify-content: flex-start;
	overflow-y: hidden;
	overflow-x: auto;
}
</style>

<style lang="sass">

.DragNDrop_area * {
 pointer-events: none;
}
</style>
