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
						// console.log("leads_none: "+leads_none.length);
						// console.log("leads_true: "+leads_true.length);
						// console.log("leads_false: "+leads_false.length);
						var eval_lead_wrapper = $("#eval-leads-wrapper")
						// console.log(document.getElementById('#eval-leads-true-wrapper'));
						
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
						// console.log(container_pending);
						// console.log(container_evaluated);
						container_pending.className="";
						container_evaluated.className="";
						
						// console.log(container_pending);
						// console.log(container_evaluated);

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

	


});
