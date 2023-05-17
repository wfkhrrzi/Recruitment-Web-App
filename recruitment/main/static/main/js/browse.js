$(document).ready(function () {
	
	console.log(statuses_initscreening)

	function component_table_dropdown(param_obj,) {
		/**
		 * generate status dropdown for the specified column
		 * 
		 * @param {Object} param_obj
		 * @param {Object} param_obj.options_param - {
		 * 		<label_lowercase> : {
		 * 			value: <value>,
		 * 			display: <value>,
		 * 		},
		 * }
		 * 
		 */
		
		let {
			data = 'default_',
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

				if (!options_param.hasOwnProperty(status.status)) {
					options_param[status.status] = {}
				}
				
				let out_status = status.status.charAt(0).toUpperCase() + status.status.slice(1)
				let selected = data.toLowerCase() === status.status.toLowerCase() ? 'selected':'';
				let value = options_param[status.status].hasOwnProperty('value') ? options_param[status.status].value : '';
				let display = !options_param[status.status].hasOwnProperty('display') ? '' : options_param[status.status].display === true ? '' : 'd-none';
				
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


	$("#table-candidates").DataTable({
		orderCellsTop: true,
		fixedHeader: true,
		responsive: true,
		autoWidth: true,
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
			{ data: "source_name" ,width:"10%",},
			// gpt status column
			{ 
				data: "gpt_status_name", 
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
							'selected': {
								value: 1,
							},
							'not selected': {
								value: 0,
							},
							'yet to select': {
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
						statuses_obj : statuses_prescreening,
						options_param : {
							'proceed': {
								value: 1,
							},
							'not proceed': {
								value: 0,
							},
							'pending': {
								display: false
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
							'proceed': {
								value: 1,
							},
							'not proceed': {
								value: 0,
							},
							'pending interview': {
								// display: false
								value: 2,
							},
							'pending result': {
								// display: false
								value: 3,
							},
						},
						stage_update_url : '#',
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
				data: "overall_status_name", 
				width:"15%",
			},
		],

		initComplete: function () {

		}, //end initComplete

		drawCallback: function () {  
			const api = this.api();

			// Filtering column
			$(".filter", api.table().header()).each(function (i) {

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

					console.log(data)

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

});
