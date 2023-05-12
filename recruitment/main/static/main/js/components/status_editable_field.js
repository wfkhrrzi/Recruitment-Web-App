$(document).ready(function () {
    
    // status interaction
	
	$('.status-field-edited button').on('click',function (e) {  
		// console.log($(this).parent())
		$(this).parent().addClass('d-none');
		$(this).parent().next().removeClass('d-none');
	})
	
	$('.status-field-editing button.status-field-editing-submit').on('click',function (e) {  
		console.log(this)
		// $(this).parent().addClass('d-none');
		// $(this).parent().prev().removeClass('d-none');
	})
	
	$('.status-field-editing button.status-field-editing-cancel').on('click',function (e) {  
        e.preventDefault();

        parent = $(this).parent().parent().parent().parent();
		parent.addClass('d-none');
		parent.prev().removeClass('d-none');
	})


    $(".status-field-select").on('change', function () {
        $(this).removeClass('bg-secondary bg-success bg-danger')
        
        // console.log(this)
        console.log($(this).val())

        let val = $(this).val()

        if (val == ""){
            $(this).addClass('bg-secondary')
        }
        else if (Boolean(Number(val))) {
            $(this).addClass('text-white bg-success')
        } else {
            $(this).addClass('text-white bg-danger')
        }

    });


});