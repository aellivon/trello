
$(document).ready(function() {
	$('#sign_up_submit').on('click', function() {
	});

	if ($('div.error-box-index').length) {
		 $('#createBoardModal').modal('show');
	}

	if ($('div.error-box-boards').length) {
		 $('#EditBoardModal').modal('show');
	}

	if ($('div.error-box-member-invite').length) {
		 $('#AddMemberModal').modal('show');
	}

	if ($('#MessageBoxModalAlert').length) {
		 $('#MessageBoxModalAlert').modal('show');
	}

	

});
