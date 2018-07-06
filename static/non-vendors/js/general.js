
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
        

        // Animations 
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

        $(document).on("click", '.title-card-class', function(){
            value = $(this).data('value');
            console.log(value);
            $(".add-card-reactor-"+value).hide();
            $("#card-add-form-column-"+value).show();
            $( "#add-card-reactor-"+value+" > input" ).focus();
        });

        $(document).on("click", '#close-add-card', function(){
            
             value = $(this).data('value');
            $("#card-add-form-column-"+value).hide();
            $(".add-card-reactor-"+value).show();
        });


        $(document).on("dblclick", '.existing-label', function(){
            id=$(this).data('value');
            $("#existing-label-"+id).hide();
            $("#existing-form-"+id).show();
            $( "#existing-form-"+id+" > input" ).focus();
        });

        $(document).on("click", '.existing-form', function(){
            id=$(this).data('value');
            $("#existing-form-"+id).hide();
            $("#existing-label-"+id).show();
        });




        // Reloading the board
        success_funciton = function(data){
            columns = JSON.parse(data.column);
            cards = JSON.parse(data.card)
            add_popped_url=$('#list-form').data('url');
            update_popped_url=$('.existing-form').data('url');
            archived_popped_url=$('#archive-form').data('url');
            add_card_popped_url=$('.toggle-card').data('url');
            $('.inner-wrap').empty();
            var a = 0;
            html = "";
            console.log(columns + " columns");
            console.log(cards + " cards");
            console.log(data + " data");
            while(a < columns.length){
                console.log('sulod');
                column_id = columns[a].pk;
                column_name = columns[a].fields.name
                html += '<div class="floatbox">' 
                         + '<div id="existing-label-'+column_id+'"' 
                       + ' class= "existing-reactor" data-value="'+column_id+'"> '
                       + ' <label data-value="'+column_id+'" '
                        + 'class="existing-label form-control title-column-class'
                        + ' non-editable-add-column" placeholder="Add List">'
                        + ' '+column_name+'</label> '
                       +'<form id="archive-form" action="'+archived_popped_url+'"'
                       +' data-url="'+archived_popped_url+'" data-value="'+column_id+'" novalidate="">'
                        +'<a id="archived-settings"  class="list-settings">'
                        +'<button class="link-style list-settings" type="submit">[X]</button></a>'
                        +'</form>'
                         + ' </div> '
                         + '   <form  id="existing-form-'+column_id+'" ' 
                         + '   class="existing-form" action='
                         + '   "'+update_popped_url+'" data-url="' +update_popped_url+'"'
                          + '  data-value="'+column_id+'"> '
                           + '     <input id="exist-list-'+column_id+'" class="form-control '
                           + '      title-column-class" data-value="'+column_id+'"'
                           + '      value="'+column_name+'">'
                           + '     <button name="AddColumn" type="submit" '
                           + '     class="btn btn-success btn-add-list">Update'
                           + '     </button> '
                            + '    <button id="close-add-list" type="button" '
                           + '      class="btn btn-secondary close-add-list"> '
                           + '      Cancel</button>  '
                          + '  </form>';
                             b = 0;
                             while(b < cards.length){
                                if (cards[b].fields.column == columns[a].pk){
                                    html+= '<div id="existing-card-'+column_id+'"'
                                      +' class="card-reactor" data-value="'+column_id+'">'
                                      + '           <center>'
                                      + '           <label data-value="'+column_id+'"'
                                      +' class=" form-control card-column-class'
                                      +' non-editable-add-card">'+cards[b].fields.name+'</label>'
                                      + '           </center>'
                                      + '           <form id="archive-form"'
                                      +' action=""'
                                      +' data-url=""'
                                      + ' data-value="'+column_id+'" novalidate="">'
                                      + '         </form>'
                                      + '       </div>';
                                }
                                b+=1;
                             }
                              html += '   <!-- Add Card -->'
                                      + '         <form  id="existing-form-'+column_id+'"'
                                      + ' class="existing-form"  data-value="'+column_id+'"'
                                      + ' action=""'
                                      + ' data-url="">'
                                      + ' <input id="exist-list-'+column_id+'"'
                                      + ' class="form-control title-column-class"'
                                      + 'data-value="'+column_id+'" value="'+column_name+'"> '
                                      + ' <button name="AddColumn" type="submit"'
                                      + 'class="btn btn-success btn-add-list">Update</button>' 
                                      + '<button id="close-add-list" type="button" class="btn'
                                      + 'btn-secondary close-add-list">Cancel</button>'  
                                      + '         </form>'
                                      + '       <div class="add-card-reactor-'+column_id+'">'
                                      + '         <label class="form-control title-card-class'
                                      +' non-editable-add-card" data-value="'+column_id+'"'
                                      +' placeholder="Add List">Add Card</label>'
                                      + '     </div>'
                                      + '     <form id="card-add-form-column-'+column_id+'"'
                                      + 'class="card-add-form-class toggle-card"'
                                      + 'action="'+add_card_popped_url+'"'
                                      + 'data-url="'+add_card_popped_url+'"' 
                                      + 'data-value="'+column_id+'">'
                                      + '         <input id="add-card-'+column_id+'"' 
                                      + 'class="form-control title-column-class" '
                                      +' placeholder="Enter Another Card Here"> '
                                      + ' <button name="AddColumn" type="submit"'
                                      + 'class="btn btn-success btn-add-card">Add</button>'
                                      + '<button id="close-add-card" data-value="'+column_id+'"'
                                      + 'type="button" class="btn btn-secondary close-add-card">'
                                      + 'Cancel</button>'
                                      + '     </form>'
                                      + ' </div>';
                               html+=' </div>';

               
                a+=1;
            }



            html += '<div class="floatbox">'
                  +'<div class="add-input-reactor">'
                      +'<label class="form-control title-column-class non-editable-add-column" placeholder="Add List">Add List</label>'
                  +'</div>'
                  +'<form id="list-form" action="'+add_popped_url+'" data-url="'+add_popped_url+'">'
                      +'<input id="add-list" class="form-control title-column-class" placeholder="Enter Another List Here"> '
                      +'<button name="AddColumn" type="submit" class="btn btn-success btn-add-list">Add</button> '
                      +'<button id="close-add-list" type="button" class="btn btn-secondary close-add-list">Cancel</button>'
                  +'</form>'
              +'</div>';
            $('.inner-wrap').html(html);
        }

        $(document).on('submit','#list-form', function(e){
            e.preventDefault()
            var title = $('#add-list').val()
            data = {
                title : title
            }
            var url = $(this).attr('action');
            $.post(url,data,success_funciton,'json'), function(err){

            };
        });

        $(document).on('submit','.existing-form', function(e){
            e.preventDefault()
            id=$(this).data('value');
            var title = $('#exist-list-' + id).val();

            console.log(title);
            data = {
                title : title,
                id : id
            }
            var url = $(this).attr('action');
            $.post(url,data,success_funciton,'json'), function(err){

            };
        });


        $(document).on('submit','#archive-form', function(e){
            console.log("aa");
            e.preventDefault()
            id=$(this).data('value');

            data = {
                id : id
            }
            var url = $(this).attr('action');
            $.post(url,data,success_funciton,'json'), function(err){

            };
        });


        $(document).on('submit','.card-add-form-class', function(e){
            console.log("hello");
            e.preventDefault()
            id=$(this).data('value');
            name = $("#add-card-"+id).val();
            data = {
                name : name,
                id : id
            }
            var url = $(this).attr('action');
            $.post(url,data,success_funciton,'json'), function(err){
                console.log('error');
            };
        });

        
});