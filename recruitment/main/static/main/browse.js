$(document).ready(function () {
	
	$('#table-candidates thead tr:eq(0)').prepend('<th>Id</th>');
	$('#table-candidates thead tr:eq(1)').prepend('<th class="filter"></th>');

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
			{ data: "id", visible:false},
			{ data: "name", width:"15%" },
			{ data: "date", },
			{ data: "source_name" ,width:"10%"},
			{ data: "gpt_status_name", width:"13%"},
			{ data: "initialscreening_status" ,width:"13%"},
			{ data: "prescreening_status" ,width:"13%"},
			{ data: "cbi_status",width:"13%"},
			{ data: "overall_status_name" ,width:"15%"},
		],

		initComplete: function () {
			// Filtering column
			var api = this.api();

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
				
				// console.log(row_i)
				// console.log(api.row(row_i).data()['id'])
				// console.log(this)

				$(this).on('click', function() {
	
					var id = api.row(row_i).data()['id'];
					
					// Construct the URL to navigate to
					var url = '/browse/' + id;
	
					console.log(url)
					
					// Navigate to the URL
					window.location.href = url;
				});

			});
			


		}, //end initComplete
	});
});
