$(document).ready(function () {

	function component_table_dropdown(param_obj,) {
		/**
		 * generate status dropdown for the specified column
		 * 
		 * @param {Object} param_obj
		 * @param {Object} param_obj.options_param - {
		 * 		<status_codename> : {
		 * 			value: <value>,
		 * 			display: <value>,
		 * 			etc.
		 * 		},
		 * }
		 * 
		 */
		
		let {
			data = 'default',
			statuses_obj = 'default',
			options_param = 'default',
			stage_update_url = 'default',
			stage_id = 'default',
			stage_name = 'default',
		} = param_obj;

		if (data == '-') {
			return `
			<div class="text-center">
				${data}
			</div>
			`;
		}

		// options in select
		let options_dropdown = ''
		for (const key in statuses_obj) {
			if (Object.hasOwnProperty.call(statuses_obj, key)) {
				let status = statuses_obj[key];
				status.status = status.status.toLowerCase();

				op_key = status.codename

				if (!options_param.hasOwnProperty(status.codename)) {
					options_param[status.codename] = {}
				}
				
				let out_status = status.status.charAt(0).toUpperCase() + status.status.slice(1)
				let selected = data.toLowerCase() === status.status ? 'selected':'';
				let value = options_param[status.codename].hasOwnProperty('value') ? options_param[status.codename].value : '';
				let display = !options_param[status.codename].hasOwnProperty('display') ? '' : options_param[status.codename].display === true ? '' : 'd-none';
				
				// let out_status = status.status.charAt(0).toUpperCase() + status.status.slice(1)
				// let selected = data.toLowerCase() === status.status.toLowerCase() ? 'selected':'';
				// let value = status.status.toLowerCase() == proceed_label.toLowerCase() ? 1 : status.status.toLowerCase() == reject_label.toLowerCase() ? 0 : '';
				// let display = status.status.toLowerCase() == none_label.toLowerCase() ? 'd-none' : '';

				option = `<option ${selected} class="${display}" value="${value}">${out_status}</option>`;
				
				options_dropdown += option;
			}
		}

		// return select
		return `
			<select name="proceed" id="" class="table-dropdown form-select" data-${stage_name}="${stage_id}" data-update-url="${stage_update_url}" data-stage-name="${stage_name}">
				${options_dropdown}
			</select>
		`;
	}

	const uploadResumeModal = new bootstrap.Modal('#uploadResumeModal');

	uploadResumeModal.toggle()

	var table = $("#table-candidates").DataTable({
		orderCellsTop: true,
		fixedHeader: true,
		responsive: true,
		autoWidth: true,
		dom: 
			"<'row mb-2'<'col-sm-12 col-md-4'l><'col-sm-12 col-md-8'<'d-flex justify-content-end'<'me-4'B>f>>>" +
        	"<'row'<'col-sm-12'tr>>" +
        	"<'row'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7'p>>",
		buttons: {
			buttons: [
				// upload and parse resume button
				{
					text: 'Upload resume',
					action: function ( e, dt, node, config ) {
						uploadResumeModal.toggle()
					},
					className: 'btn-sm btn-success btn-theme me-2',
				},
				// parse resume button
				{
					text: 'Parse new resume',
					action: function ( e, dt, node, config ) {
						alert( 'Button activated' );
					},
					className: 'btn-sm btn-success btn-theme',
				},
			],

			dom: {
				container: {
					className: ''
				}
			}
			
		},
		serverSide: true,
		processing: true,
		ajax: {
			url: "/browse",
			headers: {
				Accept: "application/json",
			},
		},
		columns: [
			{ data: "name", width:"15%" ,},
			{ data: "date", },
			{ data: "source_" ,width:"10%",},
			// gpt status column
			{ 
				data: "gpt_status_", 
				width:"13%",
				render:function (data,type) {  
					let bg_color = data.toLowerCase() == 'recommended' ? 'text-bg-success' : 'text-bg-danger'
					return `
					<div class="text-center">
						<span class="badge rounded-pill fw-semibold text-capitalize ${bg_color}">
							${data}
						</span>
					</div>
					`;
				},
			},
			// initialscreening status column
			{ 
				data: "initialscreening_status", 
				width:"13%",
				render:function (data,type,row) {
					
					return component_table_dropdown({
						data : data,
						statuses_obj : statuses_initscreening,
						options_param : {
							'initscreening:selected': {
								value: 1,
							},
							'initscreening:not selected': {
								value: 0,
							},
							'initscreening:pending': {
								display: false
							},
						},
						stage_update_url : initscreening_update_url,
						stage_id : row.initialscreening_id,
						stage_name : 'initial_screening',
					})
						
					// return data in badge design
					let bg_color = data.toLowerCase() == 'yet to select' ? 'text-bg-warning' : 'selected' ? 'text-bg-success' : 'text-bg-danger'
					
					return `
					<div class="text-center">
						<span class="badge rounded-pill fw-semibold text-capitalize text-white ${bg_color}">
							${data}
						</span>
					</div>
					`;
				},
			},
			// prescreening status column
			{ 
				data: "prescreening_status",
				width:"13%",
				render:function (data,type,row) {
					
					return component_table_dropdown({
						data : data,
						row : row,
						statuses_obj : statuses_prescreening,
						options_param : {
							'prescreening:pending': {
								display: false,
							},
							'prescreening:not proceed': {
								value: 0,
							},
							'prescreening:proceed': {
								value: 1,
							},
							'prescreening:send instruction': {
								value: 2,
							},
							'prescreening:pending submission': {
								value: 3,
							},
							'prescreening:assessment submitted': {
								value: 4,
							},
						},
						stage_update_url : prescreening_update_url,
						stage_id : row.prescreening_id,
						stage_name : 'prescreening',
					})


					// return data in badge design
					let bg_color = data.toLowerCase() == 'pending' ? 'text-bg-warning' : '-' ? null : 'proceed' ? 'text-bg-success' : 'text-bg-danger'
					
					if (bg_color === null) {
						return `
						<div class="text-center">
							${data}
						</div>
						`;
					}
					else {
						return `
						<div class="text-center">
							<span class="badge rounded-pill fw-semibold text-capitalize text-white ${bg_color}">
								${data}
							</span>
						</div>
						`;
					}
				},
			},
			// cbi status column
			{ 
				data: "cbi_status",
				width:"13%",
				render:function (data,type,row) {
					
					return component_table_dropdown({
						data : data,
						statuses_obj : statuses_cbi,
						options_param : {
							'cbi:not proceed': {
								value: 0,
							},
							'cbi:proceed': {
								value: 1,
							},
							'cbi:pending schedule': {
								// display: false
								value: 2,
							},
							'cbi:pending interview': {
								// display: false
								value: 3,
							},
							'cbi:pending result': {
								// display: false
								value: 4,
							},
						},
						stage_update_url : cbi_update_url,
						stage_id : row.cbi_id,
						stage_name : 'cbi',
					})
					
					// return data in badge design
					let bg_color = data.toLowerCase() == 'pending interview' || data.toLowerCase() == 'pending result'  ? 'text-bg-warning' : '-' ? null : 'proceed' ? 'text-bg-success' : 'text-bg-danger'
					
					if (bg_color === null) {
						return `
						<div class="text-center">
							${data}
						</div>
						`;
					}
					else {
						return `
						<div class="text-center">
							<span class="badge rounded-pill fw-semibold text-capitalize text-white ${bg_color}">
								${data}
							</span>
						</div>
						`;
					}
				},
			},
			{ 
				data: "overall_status_", 
				width:"15%",
			},
		],

		initComplete: function () {

		}, //end initComplete

		drawCallback: function () {  
			const api = this.api();

			// Filtering column
			$(".table-filter-wrapper", api.table().header()).each(function (i) {

				var column = api.column(i);
				var input = $(this).find("input[type='text']");
				input
					.on("keypress", function (e) {
						
						if(e.which === 13) {
							if (column.search() !== this.value) {
								// console.log(`Filter= ${this.value}`);
								column.search(this.value).draw();
							}
						}
					})
					
				
				var select = $(this).find("select");
				select
					.on("change", function () {
						if (column.search() !== this.value) {
							// console.log(`Filter= ${this.value}`);
							column.search(this.value).draw();
						}
					});

				var date = $(this).find("input[type='date']");
				date
					.on("change", function () {
						// console.log(`Filter= ${this.value}`);
						column.search(this.value).draw();
					});
				
			});

			// Linkable row
			$('tr',api.table().body()).each(function (row_i,element) { 

				$(this)
				.on('click', function() {
	
					window.location.href = api.row(row_i).data()['href'];
	
				})
				.css('cursor','pointer');
	
			});

			// table dropdown
			$('.table-dropdown',api.table().body()).each(function (row_i,element) {

				$(element).on('click', function (e) {  
					e.stopPropagation();
				});

				$(element).on('change', function (e) {
					update_url = e.target.dataset.updateUrl

					const data = {
						proceed:this.value,
						[e.target.dataset.stageName]:e.target.dataset[e.target.dataset.stageName]
					}

					$.ajax({
						type: "POST",
						url: update_url,
						data: data,
						headers: {
							'Accept': 'application/json'
						},
						success: function (response) {
							console.log(response)
							api.draw();
						},
						error: function (a,b,c) {  
							console.log(a.responseJSON);
							api.draw();

						}
					});

				})
	
			});

		}


	});
	

	const uploadResumeFileInput = $('#upload-resumes-input');
	const uploadResumeFileWrapper = $('#upload-resumes-wrapper');

	const uploadResumeFileInputObj = {
		fileInputObj: uploadResumeFileInput,
		add_files: function (fileList) {
			var files = Array.from(this.fileInputObj.prop('files'))
			var new_files = Array.from(fileList)
			files = files.concat(new_files)
			return this.assign_files(files)
		},
		remove_files: function (fileIndex) {
			var files = Array.from(this.fileInputObj.prop('files'))
			files.splice(fileIndex, 1)
			return this.assign_files(files)
		},
		assign_files: function (files) {  
			dt = new DataTransfer()
			
			files.forEach(file => {
				dt.items.add(file)
			});

			this.fileInputObj.prop('files',dt.files)

			return dt.files
		},
		get_files_array: function () {  
			return Array.from(this.fileInputObj.prop('files'))
		}

	}

	const displayFiles = (files) => {  

		let default_view = $('#upload-resumes-alert')
		// console.log(default_view.hasClass('d-none'))
		const fileItemWrapper = $('#upload-resumes-item-wrapper')

		// reset wrapper
		fileItemWrapper.empty()

		if (files.length > 0){

			if (!default_view.hasClass('d-none')) {
				default_view.addClass('d-none');
			}

			$.each(files, (index, file) => {
				fileItemWrapper.append(
					`
					<div class="upload-resumes-item d-flex align-items-center gap-1" style="width:calc(600px/4)">
						<div class="file-name-ellipsis">${file.name}</div>
						<button class="upload-resumes-item-delete btn btn-sm" data-file-index="${index}"><i class="fa-solid fa-trash"></i></button>
					</div>
					`
				);
			})

			// initialize delete file button 
			$('.upload-resumes-item button.upload-resumes-item-delete').each(function (index, element) {
				$(element).on('click',(event) => {
					console.log('delete file '+this.dataset.fileIndex)
					
					displayFiles(uploadResumeFileInputObj.remove_files(this.dataset.fileIndex))

				})
			});

		} else {
			
			if (default_view.hasClass('d-none')) {
				default_view.removeClass('d-none');
			}
		}

	}

	var tempFiles = null
	uploadResumeFileInput.on('click', function () {  
		tempFiles = Array.from(uploadResumeFileInput.prop('files'))
		console.log(tempFiles)
	})

	uploadResumeFileInput.on('change',function (event) {
		// console.log($(this).prop('files'))
		let files = Array.from($(this).prop('files'))
		if (tempFiles) {
			files = tempFiles.concat(files)
			tempFiles=null
		}
		displayFiles(uploadResumeFileInputObj.assign_files(files))
	})

	uploadResumeFileWrapper.on('dragenter dragover dragleave drop', function (event) {
		event.preventDefault()
	});

	uploadResumeFileWrapper.on('drop', function (event){
		// console.log(event.originalEvent.dataTransfer.files)
		const files = event.originalEvent.dataTransfer.files
		
		displayFiles(uploadResumeFileInputObj.add_files(files))
		
	})


});
