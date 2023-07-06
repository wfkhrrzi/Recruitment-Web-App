$(document).ready(function () {
	
	$("#cbi-schedule-table").DataTable({
		orderCellsTop: true,
		// fixedHeader: true,
		responsive: true,
		autoWidth: true,
		// serverSide: true,
		// processing: true,
		// ajax: {
		// 	url: "/browse",
		// 	headers: {
		// 		Accept: "application/json",
		// 	},
		// },
		columns: [
			{ data: "interview_time", width:"10%" },
			{ data: "asessors", width:"40%"},
			{ data: "rsvp_status", width:"10%"},
			{ data: "schedule_status", width:"10%"},
			{ data: "remarks", width:"30%"},
		],

		initComplete: function () {
			// Filtering column
			var api = this.api();

			
		}, //end initComplete

		drawCallback: function () {  
			var api = this.api();


		}


	});
});
