
$(document).ready(function() {

        // using jQuery
        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }

        var csrftoken = getCookie('csrftoken');
        

        function csrfSafeMethod(method) {
            // these HTTP methods do not require CSRF protection
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        }
        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });

        $(document).on("click", '#btnRemove', function(){
            // Sequence of prompting and error of removing members
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
        
        $(document).on("click", '.add-input-reactor', function(){
            $(".add-input-reactor").hide();
            $("#list-form").show();
            $( "#list-form > input" ).focus();
        });

        $(document).on("click", '.close-add-list', function(){
            $("#list-form").hide();
            $(".add-input-reactor").show();
        });

        $(document).on("blur", '#list-form > input', function(){
            // Losing focus on text input
            if (!$(this).val().length) {
                $("#list-form").hide();
                $(".add-input-reactor").show();
            }
        });

        $(document).on("dblclick", '.existing-label', function(){
            id=$(this).data('value');
            $("#existing-label-"+id).hide();
            $("#existing-form-"+id).show();
            $( "#existing-form-"+id+" > input" ).focus();
        });

        $(document).on("dblclick", '.existing-form', function(){
            id=$(this).data('value');
            $("#existing-form-"+id).hide();
            $("#existing-label-"+id).show();
        });

        $(document).on("blur", '.existing-form > input', function(){
            // Losing focus on text input
            if ($(this).val().length) {
                id=$(this).data('value');
                console.log('HIDE');
                $("#existing-form-"+id).hide();
                $("#existing-label-"+id).show();
            }
        });


        
});