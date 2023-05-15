$(document).ready(function () {

	// get the form element and attach a submit event listener
	const eval_forms = $('#initialscreening-del-eval-form,#initialscreening-eval-form');	

	$(eval_forms).each(function (index, element) {
		// element == this
		
		element.addEventListener("submit", (e) => {
			e.preventDefault(); // prevent default form submission behavior
	
			const submitBtnValue = e.submitter.value; // get submit button value
			
			const formData = new FormData(e.target);
			
			data={}

			if (e.target.id == "initialscreening-eval-form") {
				data = {
					proceed: submitBtnValue,
					users: [],
					initial_screening: e.target.dataset.initialScreeningId,
				};
		
				for (const [key, value] of formData.entries() ) {
					data["users"].push(value);
				}
			}
			else {
				data = {initial_screening_eval:submitBtnValue}
			}
	
			// send the form data to the server using AJAX request
			$.ajax(
				{
					type:"POST",
					url: e.target.action,
					data:data,
					success: function(res) 
					{
						// add wrapper if not available
						var leads_none = res['none'];
						var leads_true = res['true'];
						var leads_false = res['false'];
						var eval_lead_wrapper = $("#eval-leads-wrapper")
						
						if (leads_true.length>0) {
							if (document.getElementById('eval-leads-true-wrapper') == null) {
								eval_lead_wrapper.prepend('<div id="eval-leads-true-wrapper" class="flex-fill me-2"></div>')
							}
						} else {
							if (document.getElementById('eval-leads-true-wrapper')) {
								$('#eval-leads-true-wrapper').remove()
							}
						}
						
						if (leads_false.length>0) {
							if (document.getElementById('eval-leads-false-wrapper') == null) {
								eval_lead_wrapper.append('<div id="eval-leads-false-wrapper" class="flex-fill"></div>')
							}
						} else {
							if (document.getElementById('eval-leads-false-wrapper')) {
								$('#eval-leads-false-wrapper').remove()

							}
						}


						// reset items
						for (const key in res) {
							// delete all items
							$(`#eval-leads-${key}-wrapper`).empty()
							for (const lead_html in res[key]) {
								// recreate items
								$(`#eval-leads-${key}-wrapper`).append(res[key][lead_html])
							}
						};

						// reset wrapper class
						var container_pending = document.getElementById("leads-pending-container");
						var container_evaluated = document.getElementById("leads-evaluated-container");
						container_pending.className="";
						container_evaluated.className="";
						
							// pending container
						if (leads_none.length > 0) {
							if (leads_true.length > 0 && leads_false.length > 0) {
								container_pending.className = 'col-5';
							}
							else if (leads_true.length > 0 || leads_false.length > 0) {
								container_pending.className = 'col-8';
							} else {
								container_pending.className = 'col-12';
							}
							
						}
						else {
							container_pending.className = 'd-none';
						}

							// evaluated container
						if (leads_none.length > 0) {
							if (leads_true.length > 0 && leads_false.length > 0) {
								container_evaluated.className = 'col-7';
							}
							else if (leads_true.length > 0 || leads_false.length > 0) {
								container_evaluated.className = 'col-4';
							} else {
								container_evaluated.className = 'd-none';
							}
							
						}
						else {
							container_evaluated.className = 'col-12';
						}

					},
					error: function (a,b,c) {  
						console.log(a.responseJSON)
					}
	
				});
	
		});
		
	});

	// update on remarks hidden input and selection status (Final Decision)
	var remarks_el = $('#initialscreening-remark')
	var selection_el = $('#final-status-editing select')
	
	var orig_selection_val = selection_el.val()
	var orig_remarks_val = remarks_el.val()
	// console.log(orig_selection_val)
	// console.log(orig_remarks_val)
	
	function show_update_btn(show) {  
		let btn_wrapper = $('#final-decision-update-wrapper')
		btn_wrapper.removeClass('d-none')
	
		if (show == false){
			btn_wrapper.addClass('d-none')
		}
	}	
	
	remarks_el.on('keyup', function () {
		$('input[name="remarks"]').val(this.value)

		// show update button if value changes
		if (this.value != orig_remarks_val || selection_el.val() != orig_selection_val) {
			show_update_btn(true)
		}
		else {
			show_update_btn(false)
		}
	});

	selection_el.on('change', function () {
		// show update button if value changes
		if (this.value != orig_selection_val || remarks_el.val() != orig_remarks_val) {
			show_update_btn(true)
		}
		else {
			show_update_btn(false)
		}

	});


	// $('#final-decision-form').on('submit', function (e) {
		
	// 	e.preventDefault()

	// 	var formData = new FormData(e.target)
	// 	for (const [key, value] of formData.entries() ) {
	// 		console.log(key+": "+value);
	// 	}
	
	
	// });


});
