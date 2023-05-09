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
						// reset items
						
						for (const key in res) {
							// delete all items
							$(`#eval-leads-${key}-wrapper`).empty()
							for (const lead_html in res[key]) {
								// recreate items
								$(`#eval-leads-${key}-wrapper`).append(res[key][lead_html])
							}
						}
	
					},
					error: function (a,b,c) {  
						console.log(a.responseJSON)
					}
	
				});
	
		});
		
	});


});
