
$(document).ready(function() {
	// Closing and Opening another modal for confirmation
	$(document).on("click", '#btnRemove', function(event){
		// Remove Event
		var atLeastOneIsChecked = $('input[name="remove_member"]:checked').length > 0;
		if (atLeastOneIsChecked==true) {
			$("#reactor").empty();
    		$('#RemoveMemberModal').modal('hide');
    		$('#RemoveConfirmationModal').modal('show');
    	}else{
    		$('#RemoveConfirmationModal').modal('hide');
 			$("#reactor").html('<label id="label_error"\
 			class="alert alert-block alert-danger lbl_margin">\
 			Please check at least one checkbox to remove!</label>');
 		}
	});

	// Catches when confimation modal is hidden
	$('#RemoveConfirmationModal').on('hidden.bs.modal', function () {
		// Throws error if nothing is checked
 			$('#RemoveMemberModal').modal('show');
 		
 			
	})
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
