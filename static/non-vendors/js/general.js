
$(document).ready(function() {
	$('#sign_up_submit').on('click', function() {
	});

	if ($('div.error-box-index').length) {
		 $('#createBoardModal').modal('show');
	}

	if ($('div.error-box-boards').length) {
		 $('#EditBoardModal').modal('show');
	}

});
