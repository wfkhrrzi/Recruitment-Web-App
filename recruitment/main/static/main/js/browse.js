$(document).ready(function () {

	function sleepAfterModalHide() {
		return new Promise(resolve => setTimeout(resolve, 1000));
	}

	function uploadSuccess(callback) {
		if(isUploadSuccess){
			callback();

			isUploadSuccess = false;
		}
	}

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
	const parseNewResumeModal = new bootstrap.Modal('#parseNewResumeModal');
	const openResumeModal = new bootstrap.Modal('#openResumeModal');


	function table_child_row(data) {

		let res = null
		$.ajax({
			type: "get",
			url: get_details_url+`?candidate_id=${data.id}`,
			async:false,
			success: function (response) {
				console.log(response)
				res = response
			}
		});

		let remarks = res['remarks']
		let details = res['details']
		
		let remarks_obj={
			initial_screening:{
				form_action:initscreening_update_url,
				id:data.initialscreening_id,
				label:'Initial Screening',
				cur_remarks:remarks.initialscreening_remarks,
			},
			// prescreening:{
			// 	form_action:prescreening_update_url,
			// 	id:data.prescreening_id,
			// 	label:'Pre-assessment',
			// },
			cbi:{
				form_action:cbi_update_url,
				id:data.cbi_id,
				label:'CBI Assessment',
				cur_remarks:remarks.cbi_remarks,
			},
			// overall:{
			// 	form_action:'#',
			// 	id:null,
			// 	label:'Overall',
			// },
		}

		let rootWrapper = $('<div>').addClass('d-flex justify-content-start gap-4');
		let remarksWrapper = $('<div class="flex-fill px-2">')
		$(remarksWrapper).append('<div class="mb-2 align-self-center fw-medium">Remarks</div>');
		$(remarksWrapper).append('<div></div>').find('div').addClass('d-flex justify-content-start gap-2');
		
		for (const key in remarks_obj) {
			if (Object.hasOwnProperty.call(remarks_obj, key)) {
				const stage = remarks_obj[key];
				
				// if (stage.id) {
					$(`
						<div class="flex-fill" >
							<label for="${key}-remarks" class="form-label">${stage.label}</label>
							<textarea ${stage.id ? '' : 'disabled'} data-form-action="${stage.form_action}" data-stage="${key}" data-stage-id=${stage.id} class="form-control table-remarks" rows="3" style="font-size:inherit;" placeholder="Optional. Make sure to save the remarks">${stage.cur_remarks === '-' ? '': stage.cur_remarks}</textarea>
						</div>
					`)
						.appendTo(remarksWrapper.find('div:eq(1)'))
				// }
			}
		}
		
		let sourceWrapper = $('<div class="px-2">')
		$(sourceWrapper).append('<div class="mb-2 align-self-center fw-medium">Source</div>');
		$(sourceWrapper).append(`<div>${details['source_']}</div>`)
		
		let nationalityWrapper = $('<div class="px-2">')
		$(nationalityWrapper).append('<div class="mb-2 align-self-center fw-medium">Nationality</div>');
		$(nationalityWrapper).append(`<div>${details['nationality_']}</div>`)
		
		rootWrapper.append(sourceWrapper)
		rootWrapper.append(nationalityWrapper)
		rootWrapper.append(remarksWrapper)
		
		return rootWrapper.prop('outerHTML')
		
	}

	const gpt_status_badge = (data) => {
		if(!data){
			return '-'
		}
		let bg_color = data.toLowerCase() == 'recommended' ? 'text-bg-success' : 'text-bg-danger'
		return `
		<div class="text-center">
			<span class="badge rounded-pill fw-semibold text-capitalize ${bg_color}">
				${data}
			</span>
		</div>
		`;
	}

	// gpt_status initialized to 'recommended'
	// $('.table-filter-wrapper select[name="gpt_status"]').val('gpt_status:recommended');

	const init_gpt_score = 80

	var table = $("#table-candidates").DataTable({
		orderCellsTop: true,
		fixedHeader: true,
		responsive: true,
		autoWidth: true,
		dom: 
			// "<'row mb-2'<'col-sm-12 col-md-4'l><'col-sm-12 col-md-8'<'d-flex justify-content-end'<B><'ms-4'f>>>>" + // search bar is 'f'
			"<'row mb-2 align-items-center'<'col-sm-12 col-md-4'l><'col-sm-12 col-md-8'<'d-flex justify-content-end align-items-center'<B><'#gpt-score-thre'><'#sourceFilter'>>>>" + 
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
						// alert( 'Button activated' );
						// window.open("https://ptsg-5edhnebulaap02-generic-resume-parser.azurewebsites.net/", "_blank")
						parseNewResumeModal.toggle()
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
		searchCols: [
			null,
			null,
			null,
			null,
			// { "search": "gpt_status:recommended" },
			null,
			null,
			null,
			null,
			null,
			null,
			{ "search": init_gpt_score },

		],
		order: [[1, 'asc']],
		columns: [
			{
				className: 'dt-control',
                orderable: false,
                data: null,
                defaultContent: '',
			},
			{ data: "name", width:"15%", render: function (data,type,row) {
				out = $(`
					<div>
						<div class='d-flex gap-2 align-items-center'>
							<div>${data}</div>
						</div>
					</div>
				`);

				if (row.new_applicant) {
					out.find('div.d-flex').append(`
						<span class="badge text-bg-secondary rounded-pill fw-semibold">NEW</span>
					`)
				}

				return out.html();
			}},
			{ data: "date", },
			{ data: "category_" ,width:"10%",},
			// gpt status column
			{ 
				data: "gpt_status_", 
				width:"13%",
				render:function (data,type) {  
					return gpt_status_badge(data)
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
				data: "gpt_status_", 
				width:"15%",
				render: function (data) {  
					return gpt_status_badge(data);
				}
			},
			{
				name:"source",
				data: "source_",
				visible: false,
			},
			{
				name:"gpt_score",
				data: "gpt_score",
				visible: false,
			},
		],

		initComplete: function () {
			const api = this.api();

			// source filter
			let options = '<option value="">Source</option>'
			for (const source of sources) {
				options += `<option value="${source.id}">${source.source}</option>`
			}

			$("#sourceFilter").addClass('ms-3').append(`
				<select name="source" id="" class="table-filter form-select">
					${options}
				</select>
			`).on('change',function (event) {  
				// console.log(event.target.value)
				api.column('source:name').search(event.target.value).draw()
			});

			$('#gpt-score-thre').addClass('ms-3').append(`
				<label class="fw-medium" style="font-size:0.8rem;margin:0;">GPT Threshold: <span id="gpt-score-thre-value" >${init_gpt_score}</span>%</label>
				<input type="range" class="form-range" value="${init_gpt_score}">
			`)
			.find('input[type="range"]').on('input change',function () {  
				$(this).attr('value',this.value);
				$('#gpt-score-thre-value').html(this.value);
			}).on('change',function () {  
				// api call to filter table based on gpt score
				console.log('threshold value:',this.value)
				api.column('gpt_score:name').search(this.value).draw()		
			})

		}, //end initComplete

		drawCallback: function () {  
			const api = this.api();

			// Filtering column
			$(".table-filter-wrapper", api.table().header()).each(function (i) {
				// console.log(api.column(i));
				// console.log(api.column($(this).index()));
				var column = api.column($(this).index());
				var input = $(this).find("input[type='text']");
				input
					.on("keypress", function (e) {
						if(e.which === 13) {
							console.log('******** run input **********')
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
						console.log('******** run date **********')
						column.search(this.value).draw();
					});
				
			});

			// Linkable row / Open respective resume when clicking a candidate item 
			$('tr',api.table().body()).each(function (row_i,element) {

				let data = api.table().row(this).data()

				$(this)
				.on('click', function() {
	
					// window.location.href = api.row(row_i).data()['href'];
					
					console.log(data.id)
					$.ajax({
						url: get_open_resume_url+data.id,  // Replace with the URL to your Django view
						type: 'GET',
						xhrFields: {
							responseType: 'blob'
						},
						// responseType: 'arraybuffer',  // Use 'arraybuffer' to handle binary data
						// dataType: 'blob',  // Use 'blob' data type to handle binary data
						success: function(data) {

							var fileUrl = URL.createObjectURL(data);
				
							// // Set the iframe source to display the PDF
							$(openResumeModal._element).find('iframe').attr('src', fileUrl);

							openResumeModal.toggle()

						},
						error: function(xhr, status, error) {
							console.error('Error retrieving PDF:', error);
						}
					});
	
				})
				.css('cursor','pointer');
	
			});

			// table dropdown
			$('.table-dropdown',api.table().body()).each(function (row_i,element) {

				$(element).on('click', function (e) {  
					e.stopPropagation();
				});				

				$(element).on('change', function (e) {

					const update_url = e.target.dataset.updateUrl

					const data = {
						proceed:this.value,
						[e.target.dataset.stageName]:e.target.dataset[e.target.dataset.stageName]
					}

					// initialize ajax update
					const update_ajax = function () {
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
					}

					let subsequent_stage_exist = false

					// check if subsequent stages exist
					$('.table-dropdown',$(this).parent().parent()).each(function (index, element) {
						
						let next_dropdown_index = $(element).parent().index()
						let current_dropdown_index = $(e.target).parent().index()

						// current dropdown contains subsequent stages
						if (next_dropdown_index > current_dropdown_index) {	
							subsequent_stage_exist = true
						}
						
					});

					// executes update
					if (subsequent_stage_exist) {
						// prompt user to confirm selection
						Swal.fire({
							title: 'Are you sure?',
							text: "Rejecting the candidate on ealier stages will terminate the subsequent stages",
							icon: 'warning',
							showCancelButton: true,
							confirmButtonColor: '#3085d6',
							cancelButtonColor: '#d33',
							confirmButtonText: 'Yes, I proceed',
							cancelButtonText: 'CANCEL',
						}).then((result) => {
							console.log(result)
							if (result.isConfirmed) {
								// update executed
								update_ajax();
							} else {
								// revert current dropdown change
								api.draw()
							}
						});
					} else {
						// executes update regardless
						update_ajax();
					}
					

				})
	
			});


			// Add event listener for opening and closing child rows (remarks)
			$('td.dt-control',api.table().body()).on('click', function (e) {
				e.stopPropagation()

				// current row
				const tr = $(this).closest('tr');
				const tr_index = $(tr).index()
				const row = api.table().row(tr);
		 
				if (row.child.isShown()) {
					// This row is already open - close it
					row.child.hide();
					tr.removeClass('shown');
				} else {
					// Open this row
					row.child(table_child_row(row.data())).show();
					tr.addClass('shown');

					// change event to save edited remarks
					$('.table-remarks',row.child()).each(function (index,element) {  
						// console.log(this)
						$(this).on('change',function (e) { 

							let dataset = e.target.dataset
							data = {
								remarks: $(this).val(),
								[dataset.stage] : dataset.stageId
							}

							$.ajax({
								type: "post",
								url: dataset.formAction,
								data: data,
								headers: {
									Accept: "application/json",
								},
								success: function (response) {
									console.log(response)
								},
								error: function(a,b,c) {
									console.log(Error(a))
								}
							});
							
						})
					})
				}
				
				// close other opened rows
				const tbody = $(this).closest('tbody')
				
				$(tbody).children().each(function (index,element) {  
					const row = api.table().row(this)
					if (index !== tr_index & row.child.isShown()) {
						console.log(`row ${index} has dt-hasChild`)
						row.child.hide();
						$(this).removeClass('shown');
					}
				});


			});			

		}


	});

	// trigger fullscreen modal
	$(openResumeModal._element).find('.modal-header').find('button:eq(0)').on('click',function () {  
		$(openResumeModal._element).find('.modal-dialog').toggleClass('modal-fullscreen')
	})
	
	$(openResumeModal._element).on('hide.bs.modal',function () {  
		$(openResumeModal._element).find('.modal-dialog').removeClass('modal-fullscreen')
	})



		
	/* ------------------- UPLOAD FILE ------------------------- */
	const uploadResumeForm = $('#upload-resume-form')
	const uploadResumeFileInput = $('input[type="file"]',uploadResumeForm);
	const uploadResumeContent = $('#upload-resumes-content');
	const uploadResumeWrapper = $('#upload-resumes-wrapper');
	const uploadResumeFileItemWrapper = $('#upload-resumes-item-wrapper');
	const uploadResumeClear = $('#upload-resume-clear',uploadResumeForm);
	const uploadParseResumeTrigger = $('#upload-and-parse-resume',uploadResumeForm);
	const uploadResumeSubmit = $('#upload-resume-submit',uploadResumeForm);
	const uploadResumeDefaultView = $('#upload-resumes-alert');
	var isUploadSuccess = false;

	console.log(uploadResumeForm.get(0))

	// object to manipulate input[type='file']
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
		remove_all: function () {
			var files = Array()
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

	// re-render upload-resumes-item-wrapper on every func call
	const displayFiles = (dt_files) => {  

		// reset wrapper
		uploadResumeFileItemWrapper.empty()

		if (dt_files.length > 0){

			if (!uploadResumeDefaultView.hasClass('d-none')) {
				uploadResumeDefaultView.addClass('d-none');
			}

			if (uploadResumeClear.hasClass('d-none')) {
				uploadResumeClear.removeClass('d-none');
			}

			uploadResumeSubmit.prop('disabled',false)
			uploadParseSubmit.prop('disabled',false)


			$.each(dt_files, (index, file) => {
				uploadResumeFileItemWrapper.append(
					`
					<div class="upload-resumes-item py-1 px-2 d-flex align-items-center gap-1 rounded" style="max-width:500px;">
						<div class="file-name-ellipsis">${file.name}</div>
						<button class="upload-resumes-item-delete btn btn-sm" data-file-index="${index}"
						style="
							--bs-btn-hover-color: var(--bs-danger);
							--bs-btn-active-color: var(--bs-white);
  							--bs-btn-active-bg: var(--bs-btn-hover-color);
						"
						>
							<i class="fa-solid fa-trash"></i>
						</button>
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
			
			if (uploadResumeDefaultView.hasClass('d-none')) {
				uploadResumeDefaultView.removeClass('d-none');
			}
			
			if (!uploadResumeClear.hasClass('d-none')) {
				uploadResumeClear.addClass('d-none');
			}

			uploadResumeSubmit.prop('disabled',true)
			uploadParseSubmit.prop('disabled',true)
		}

	}

	var tempFiles = null
	uploadResumeFileInput.on('click', function () {  // temporarily store current selected files in tempFiles, then unload them in "change" event
		tempFiles = Array.from(uploadResumeFileInput.prop('files'))
	})

	uploadResumeFileInput.on('change',function (event) {
		let files = Array.from($(this).prop('files'))
		if (tempFiles) {
			files = tempFiles.concat(files)
			tempFiles=null
		}
		displayFiles(uploadResumeFileInputObj.assign_files(files))
	})

	uploadResumeWrapper.on('dragenter dragover dragleave drop', function (event) {
		event.preventDefault()
	});

	uploadResumeWrapper.on('dragenter dragover', function (event) {
		$(this).addClass('upload-file-card-highlight')
	});

	uploadResumeWrapper.on('dragleave', function (event) {
		// Check if the related target is not a child element of the drop target
		if (!$(this).is(event.relatedTarget) && !$(this).has(event.relatedTarget).length) {
			// Remove the class
			$(this).removeClass('upload-file-card-highlight');
		}

	});

	uploadResumeWrapper.on('drop', function (event){
		$(this).removeClass('upload-file-card-highlight')
		const files = event.originalEvent.dataTransfer.files
		displayFiles(uploadResumeFileInputObj.add_files(files))
		
	})

	// constructor func for progress bar (implementation)
	function ProgressBar (progress_value=null,progress_text=null) {

		progress_value = progress_value ? progress_value : 0
		
		let progressBar = $('<div>', {
			class: 'progress',
			role: 'progressbar',
			style: 'height: 20px'
		});
		
		let progressBarInner = $('<div>', {
			class: 'progress-bar progress-bar-striped bg-success progress-bar-animated',
			style: `width: ${progress_value}%`,
			text: `${progress_text ? progress_text : progress_value}%`
		});

		progressBar.append(progressBarInner)

		this.component= progressBar;

		this.set_value= function (value) {  
			this.component.find('.progress-bar').css('width',`${value}%`);
			this.component.find('.progress-bar').text(`${value}%`);
		}
		
		this.set_text= function (value) {  
			this.component.find('.progress-bar').text(`${value}`);
		}
		
		this.get_component= function () {  
			return this.component
		}

		this.get_component_html= function () {  
			return this.component.prop('outerHTML');
		}

		this.reset = function () {  
			this.set_value(0)
		}

		this.hide = function () {  
			this.component.remove()
		}

		this.reset_hide = function () {  
			this.reset()
			this.hide()
		}
	}

	var progress_bar = new ProgressBar() // progress bar obj instance --> actual element

	// when clicked "upload" button
	const executeUploadResume = function () {  
		const formData = new FormData(uploadResumeForm.get(0))
		
		var files_count = 0

		for (const [key, file] of formData.entries()) {
			if (file.name) { // workaround for an element appearing with empty name
				files_count++;
			}
		}

		if (files_count > 0) {

			let ajaxUpload = $.ajax({
				type: "post",
				url: uploadResumeForm.prop('action'),
				data: formData,
				headers:{
					'Accept':'application/json'
				},
				contentType: false,
				processData: false,
				// actions before ajax start
				beforeSend: function () {
					uploadResumeFileItemWrapper.empty()
					uploadResumeContent.append(progress_bar.get_component())
					uploadResumeSubmit.prop('disabled',true)
					uploadResumeClear.prop('disabled',true)
				},
				// actions after ajax completes
				success: function (response) {
					isUploadSuccess = true;

					uploadResumeFileItemWrapper.empty()
					uploadResumeFileItemWrapper.html(`
					<div class="text-success">
						<div class="fa-stack fa-xl mb-3">
							<i class="fa-regular fa-circle fa-stack-2x" style=" margin:0;"></i>
							<i class="fa-solid fa-check fa-stack-1x fa-lg" style=" margin:0;"></i>
						</div>
						<div class="fw-medium">Files are successfully uploaded</div>
					</div>
					`)
					uploadResumeSubmit.prop('disabled',true)
					uploadResumeClear.prop('disabled',false).addClass('d-none')
					uploadResumeFileInputObj.remove_all()
					progress_bar.reset_hide()

				},
				error: function (a,b,c) {  
					console.log(a.responseJSON)
				},
				// actions during ajax execution
				xhr: function () {  
					var xhr = new window.XMLHttpRequest();

					xhr.upload.addEventListener("progress", function(evt) {
						if (evt.lengthComputable) {
							var percentComplete = evt.loaded / evt.total;
							percentComplete = parseInt(percentComplete * 100);
							console.log(percentComplete);
							
							progress_bar.set_value(percentComplete)

						}
					}, false);

					xhr.upload.onload = function () {
						setTimeout(() => {progress_bar.set_text('Uploading the files into the database')},2000)
					}

					return xhr;
				}
			});

			return new Promise(function (resolve,reject) {  
				ajaxUpload.done(function (response) {  
					resolve(response)
				})
			})


		} else {
			return Error('no files are selected')
		}

	}

	uploadResumeForm.on('submit',function (e) {  
		e.preventDefault()
		console.log('upload submitted');

		let source_input = $('#upload-resumes-source-hidden').val();

		if (source_input == ""){
			console.log('source is NULL');
			uploadResumeContainer.find('.card-body')
			.prepend(
				displayUploadErrorAlert('Select the <b>source</b> of the resume(s)!')
			);

			setTimeout(() => {
				clearUploadErrorAlert();
				console.log('Deleted upload error messages');
			}, 5000);

			return
		}

		else {
			clearUploadErrorAlert();
		}

		console.log('run upload');

		// executeUploadResume();

	})

	const displayUploadErrorAlert = function (message) {  
		let component = $(`
		<div class="alert alert-danger alert-dismissible fade show upload-resumes-error-alert" role="alert" style="
			font-size:0.8rem;
			--bs-alert-padding-x: 0.5rem;
			--bs-alert-padding-y: 0.5rem;
		">
			<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close" style="
				padding: 0.7rem 1rem;
			"></button>
		</div>
		`)

		component.prepend(message)

		return component.prop('outerHTML')
	}

	const clearUploadErrorAlert = function () {  
		$('.upload-resumes-error-alert').remove()
	}

	// when clicked "clear all" button
	uploadResumeClear.on('click',function (e) {  
		e.preventDefault()
		// console.log('clear all clicked')
		displayFiles(uploadResumeFileInputObj.remove_all())

		console.log(uploadResumeFileInput.prop('files'))
		
		uploadResumeSubmit.prop('disabled',true)

	})


	$(uploadResumeModal._element).on('hide.bs.modal', event => {
		(
			async () => {
				await sleepAfterModalHide()
				
				// reset uploadResumeFileItemWrapper
				uploadSuccess(function () {  
					uploadResumeFileItemWrapper.empty();
					uploadResumeDefaultView.removeClass('d-none');
				});

			}
		)();

	})

	// update source hidden input for every change in upload modal's source input
	$("#upload-resumes-source-select").on('change',function (event) {  
		$('#upload-resumes-source-hidden').val(event.target.value)
	})

	// ---------------------------- PARSE NEW RESUME ---------------------------------------
	const parseNewResumesInputs = $('.parse-resumes-input');
	const parseNewResumesForm = $('#parse-resumes-config-form');
	const parseNewResumesList = $('#parse-resumes-list');
	const parseNewResumesSubmit = $('#parse-resumes-submit');
	const jobRoleInput = $('#parse-resumes-jobRole');
	const jobDescInput = $('#parse-resumes-jobDesc');
	const skillsInput = $('#parse-resumes-skills');
	const parserUpdateCheckbox = $('#parse-config-update-checkbox')

	// parseNewResumeModal.toggle()

	// return resumes to parse alert + ajax
	function resumesToParseAlert() {
		parseNewResumesList.empty();

		return $.ajax({
			type: "get",
			url: get_raw_resumes_url,
			success: function (response) {
				// generate resume items
				data = response.data
				// data = []
				
				if (data.length > 0) {

					parseNewResumesList.append(
						`<div class="alert alert-success mb-0">
							<i class="fa-sharp fa-solid fa-circle-check fa-lg me-2"></i>
							There are a total of <strong>${response.count}</strong> resumes to be parsed
						</div>`
					);
					parseNewResumesSubmit.prop('disabled',false);

				} else {
					
					parseNewResumesList.append(
						`<div class="alert alert-danger mb-0">
							<i class="fa-solid fa-triangle-exclamation fa-lg me-2"></i>
							No resumes are to be parsed
						</div>`
					);
					parseNewResumesSubmit.prop('disabled',true);

				}
			},
			error: function (a,b,c) {  
				console.log(a)
			}
		});
	}

	// fetch parser config details
	function readParserConfig() {
		$.ajax({
			type: "get",
			url: read_parserConfig_url,
			success: function (response) {
				jobRoleInput.val(response['job_title'])
				jobDescInput.val(response['job_description'])
			}
		});
	}

	// fetch parser config details
	function updateParserConfig() {
		if (parserUpdateCheckbox.prop('disabled') == false && parserUpdateCheckbox.prop('checked') == true) {
			
			// console.log('parser config start updating...')
			$.ajax({
				type: "post",
				url: update_parserConfig_url,
				data:{
					job_title:jobRoleInput.val(),
					job_description:jobDescInput.val(),
				},
				success: function (response) {
					console.log('parser config updated.')
					// jobRoleInput.val(response['job_title'])
					// jobDescInput.val(response['job_description'])
				}
			});

		}
	}


	$(parseNewResumeModal._element).on('show.bs.modal', event => {
		// display active parsing tasks
		resumesToParseAlert();

	})

	$(parseNewResumeModal._element).on('hide.bs.modal', event => {
		(
			async () => {
				await sleepAfterModalHide()
				
				// clear all resumes
				parseNewResumesList.children().remove()
		
				// reset uploadResumeFileItemWrapper
				uploadSuccess(function () {  
					uploadResumeFileItemWrapper.empty();
					uploadResumeDefaultView.removeClass('d-none');
				})
		
				// remove upload container
				undoUploadParse();
			}
		)();
	})
	
	function disable_parse_inputs(bool=true) {
		parseNewResumesInputs.each(function (index, element) {
			// element == this
			$(this).prop('disabled',bool)
	
			// jobRoleInput.val(jobRole);
			// jobDescInput.val(jobDesc);
			readParserConfig();
			parserUpdateCheckbox.prop('disabled',bool)
	
		});		
	}

	disable_parse_inputs();

	$('#parse-resumes-default-checkbox').on('change', function () {
		if (this.checked) {
			parseNewResumesInputs.prop('disabled',true)
			// parseNewResumesForm.addClass('d-none')
			// jobRoleInput.val(jobRole);
			// jobDescInput.val(jobDesc);
			readParserConfig();
			parserUpdateCheckbox.prop('disabled',true)

		} else {
			parseNewResumesInputs.prop('disabled',false)
			parserUpdateCheckbox.prop('disabled',false)
			// parseNewResumesForm.removeClass('d-none')

		}

	});

	// submit parse resume
	const executeParseResume = function () {  
		disable_parse_inputs(false);

		const formData = new FormData(parseNewResumesForm[0])

		let data = {}


		for (const [key,value] of formData.entries()) {
			data[key] = value
			// console.log(`${key}: ${value}`)
		}

		console.log(data)

		disable_parse_inputs();

		let ajaxParse = $.ajax({
			type: "post",
			url: get_parse_resumes_url,
			data: data,
			headers: {
				Accept: "application/json",
			},
			success: function (response) {
				console.log(response)
				resumesToParseAlert();
			},
			error: function(a,b,c) {
				console.log(Error(a))
			}
		});

		
		// return new Promise(function (resolve,reject) {  
		// 	ajaxParse.done(function (response) {  
		// 		resolve(response)
		// 	})
		// })

		// parseNewResumeModal.toggle()

	}

	parseNewResumesSubmit.on('click', function () {
		console.log('parse resumes trigger')
		executeParseResume();		
		updateParserConfig();
	});

	// ---------------------- PARSE RESUMES NOTIFICATION ----------------------------------
	
	const bgTasksAlert = $('.background-tasks-alert');

	// initialize event source for parse resume 
	// var es = new ReconnectingEventSource('/notification/parser');

	// es.addEventListener('message', function (e) {
	// 	res = JSON.parse(e.data);
	// 	console.log(res);

	// 	active_task.add_task(res['task'])
		
	// }, false);

	// es.addEventListener('stream-reset', function (e) {
	// }, false);

	// initialize websocket for parse resume 
	var socket = new WebSocket('ws://localhost:8000/notification/parser');
	
	socket.onmessage = function (e) {  
		res = JSON.parse(e.data);
		res['lst_task'] = JSON.parse(res['lst_task'])
		// console.log(res);
		
		bgTasksAlert.children().remove()
		
		if (res['lst_task']) {
			bgTasksAlert.removeClass('d-none');
			let alert_string = '';
			
			const tasks = res['lst_task']
			console.log(tasks)

			alert_string += `<strong class="me-2">${tasks.user.alias}</strong>  is currently parsing  <strong class="ms-2">${tasks.resumes_info.length} resumes</strong>\n`

			bgTasksAlert.append(
				`<div class="alert alert-warning mb-0">
					<div class="d-flex align-items-center">
						<div class="me-3 spinner-border spinner-border-sm" role="status" style="">
							<span class="visually-hidden">Loading...</span>
						</div>
						${alert_string}
						</div>
				</div>`
			);
		}
		else {
			bgTasksAlert.addClass('d-none')
		}
	}

	socket.onopen = function () {  
		setInterval(
			function () {  
				socket.send('ping')
			},
			2000
		)
	}

	
	// ---------------------- Upload and Parse Resumes ----------------------------------

	const uploadParseResumeContainer = $('#upload-and-parse-resumes-container');
	const uploadResumeContainer = $('#upload-resumes-container');
	const uploadParseSubmit = $(`
		<button id="upload-parse-resumes-submit" type="button" class="btn btn-sm btn-success btn-theme" disabled>Upload & Parse Resumes</button>
	`)

	var uploadParseResumeBool = false;
	
	const triggerUploadParse = function () {
		
		uploadParseResumeContainer.addClass('py-3')
		uploadParseResumeContainer.append(`
		<div class="fw-medium mb-3" style="font-size:0.9rem">Upload Resumes</div>
		`)
		uploadResumeWrapper.appendTo(uploadParseResumeContainer);
		
		uploadParseResumeTrigger.addClass('d-none')
		uploadResumeSubmit.addClass('d-none')

		uploadParseResumeBool = true;

		// change modal appearance
		$(parseNewResumeModal._element).find('.modal-header h1').text('Upload and Parse')
		
		parseNewResumesSubmit.replaceWith(uploadParseSubmit);

		// submit upload parse resumes
		uploadParseSubmit.on('click', function () {  
			let execUpload = executeUploadResume();
			console.log(execUpload)
			if (execUpload instanceof Promise) {

				execUpload.then(function(response) {
					console.log(response);
					executeParseResume();
					// let execParse = executeParseResume();

					// execParse.then(function (response) {  
					// 	console.log(response);
					// 	resumesToParseAlert();
					// })

				}).catch(function(error) {

					console.error(error);

				});

			} else {
				// Object is not a promise
				console.log(execUpload);
			}
		
		});
		
	}
	
	const undoUploadParse = function () {  
		console.log(uploadParseResumeBool)
		if (uploadParseResumeBool) {
			uploadResumeWrapper.appendTo(uploadResumeContainer);
			uploadParseResumeContainer.removeClass('py-3');
			uploadParseResumeContainer.empty();
	
			uploadParseResumeTrigger.removeClass('d-none');
			uploadResumeSubmit.removeClass('d-none')


			uploadParseResumeBool = false

			// change modal appearance
			$(parseNewResumeModal._element).find('.modal-header h1').text('Parse Resumes')
			uploadParseSubmit.replaceWith(parseNewResumesSubmit);

		}
	}


	// when clicked "upload and parse" button
	uploadParseResumeTrigger.on('click',function (e) {  
		e.preventDefault()
		console.log('upload and parse');

		triggerUploadParse();
		updateParserConfig();
	});

	
});
