
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

        // Animations
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
                $('#RemoveMemberModal').modal('show');
        })


        $(document).on("click", '#EditComment', function(){
                console.log("hi");
                card_id=$(this).data('value');
                console.log(card_id);
                $('#DivisionComment-'+card_id).addClass('display-none');
                $('#InputComment-'+card_id).removeClass('display-none');
                $('#EditComment').addClass('display-none');
                $('#DeleteComment').addClass('display-none');
                $("#card-save-button").removeClass('display-none');
                $("#card-cancel-button").removeClass('display-none');
        })

         $(document).on("click", '#card-cancel-button', function(){
                card_id=$(this).data('value');
                console.log(card_id);
                $('#DivisionComment-'+card_id).removeClass('display-none');
                $('#InputComment-'+card_id).addClass('display-none');
                $('#EditComment').removeClass('display-none');
                $('#DeleteComment').removeClass('display-none');
                $("#card-save-button").addClass('display-none');
                $("#card-cancel-button").addClass('display-none');
        })


        $('#DeleteCommentModal').on('hidden.bs.modal', function () {
                $('#CardModal').modal('show');
        })

        $('#CardMemberModal').on('hidden.bs.modal', function () {
                $('#CardModal').modal('show');
        })

        $('#ArchiveCardConfirmation').on('hidden.bs.modal', function () {
                $('#CardModal').modal('show');
        })

        $('#DueDateModal').on('hidden.bs.modal', function () {
                $('#CardModal').modal('show');
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
        

        
        // Adding a column animation
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
            console.log(value);
            $("#card-add-form-column-"+value).hide();
            $(".add-card-reactor-"+value).show();
        });

        // Existing Columns Animation
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

        // Decsription Animation
        $(document).on("dblclick", "#text-class-description", function(){
            if($('#text-class-description').prop('readonly')){

               $('#text-class-description').attr("readonly",false);
               $("#card-button-add-description").removeClass('display-none');
               $("#card-button-cancel-description").removeClass('display-none');
               $( "#hr-after-description" ).addClass( "mt-4" );
            }
        });
        $(document).on("click", "#card-button-cancel-description", function(){
          $('#text-class-description').attr("readonly",true);
          $("#card-button-add-description").addClass('display-none');
          $("#card-button-cancel-description").addClass('display-none');
          $( "#hr-after-description" ).removeClass( "mt-4" );
        });

        // Comment Animation
        $(document).on("click", "#text-comment-area", function(){
            $("#card-button-add-comment").removeClass('display-none');
            $("#card-button-cancel-comment").removeClass('display-none');
           
          });
        $(document).on("click", "#card-button-cancel-comment", function(){
          $("#card-button-add-comment").addClass('display-none');
          $("#card-button-cancel-comment").addClass('display-none');
        });

        // Animation for card title
        $(document).on("click", "#heading-card-title", function(){
          $("#heading-card-title").addClass('display-none');
          $("#input-card-title").removeClass('display-none');
          $("#input-card-title").focus();
        });

        $(document).on("blur", "#input-card-title", function(){
          $("#input-card-title").addClass('display-none');
          $("#heading-card-title").removeClass('display-none');
        });



        function formatDate(date) {
            var year = date.getFullYear(),
                month = date.getMonth() + 1, 
                day = date.getDate(),
                hour = date.getHours(),
                minute = date.getMinutes(),
                second = date.getSeconds(),
                hourFormatted = hour % 12 || 12, 
                minuteFormatted = minute < 10 ? "0" + minute : minute,
                morning = hour < 12 ? "am" : "pm";

            return month + "/" + day + "/" + year + " " + hourFormatted + ":" +
                    minuteFormatted + morning;
        }

        // Reloading the card
        reload_card = function(data){
            $(".class-details-reactor").empty();
            console.log(data);
            cards=JSON.parse(data.cards);
            comments=JSON.parse(data.comments);
            card_name = cards[0].fields.name;
            card_description = cards[0].fields.description;
            if (card_description==null){
              card_description="";
            }
            console.log(name);
            html = ""
            html += ' <div class="modal fade bd-example-modal-lg" id="CardModal" tabindex="-1" role="dialog" aria-labelledby="myLargeModalLabel" aria-hidden="true">'
                  +'<div class="modal-dialog modal-lg">'
                   +'    <div class="modal-content">'
                   +'       <div class="modal-header">'

                   +'         <h3 id="heading-card-title" class="modal-title card-class-title" id="exampleModalLabel"><strong>'+card_name+'</strong></h3>'
                  +'          <input id="input-card-title" class="form-control card-class-title display-none" value="'+card_name+'"> '
                   +'         <button type="button" class="close" data-dismiss="modal" aria-label="Close">'
                   +'           <span aria-hidden="true">&times;</span>'
                   +'         </button>'

                   +'       </div>'
                   +'       <div class="modal-body">'
                   +'          <div class="left-portion-of-header col-lg-9 col-md-9 col-sm-9">'
                   +'               <h5 class="modal-label-desc" id="exampleModalLabel">Card Description</h5>'

                   +'        </div>'
                    +'        <div class="right-portion-of-header col-lg-3 col-md-3 col-sm-3">'
                    +'              <h5 class="modal-label-manage" id="exampleModalLabel">Manage</h5>'
                    +'       </div>'
                    +'         <div class="left-portion-of-modal col-lg-9 col-md-9 col-sm-9">'

                    +'            <textarea readonly id="text-class-description" class="textarea class-description" placeholder="Card Description">'+card_description+'</textarea>'

                     +'           <button name="" id="card-button-add-description"class="btn btn-secondary card-button-add-description mt-1 float-right display-none">Save</button>'
                    +'            <button name="" id="card-button-cancel-description"class="btn btn-secondary card-button-add-description mt-1 float-right display-none">Cancel</button>'
                    +'          </div>'

                     +'         <div class="right-portion-of-modal col-lg-3 col-md-3 col-sm-3">'
                     +'             <button data-toggle="modal" data-target="#CardMemberModal"  name="MessageBoxModalAlert" class="btn btn-secondary card-button-invite mt-1" data-dismiss="modal">Members</button>'
                     +'             <button data-toggle="modal" data-target="#DueDateModal" name="MessageBoxModalAlert" class="btn btn-secondary card-button-due-date mt-1" data-dismiss="modal">Due Date</button>'
                     +'             <button  data-toggle="modal" data-target="#ArchiveCardConfirmation"  name="MessageBoxModalAlert" class="btn btn-secondary card-button-due-date mt-1" data-dismiss="modal">Archive</button>'

                     +'         </div>'
                      +'        <!-- Bottom Part -->'
                     +'         <div id="hr-after-description"class="left-portion-of-header col-lg-12 col-md-12 col-sm-12">'
                     +'           <hr class="hr">'
                     +'       </div>'
                     +'       <div class="left-portion-of-header col-lg-9 col-md-9 col-sm-9">'
                     +'             <h5 class="modal-card-add-comment" id="exampleModalLabel">Add Comment</h5>'
                     +'             <textarea id="text-comment-area" class="textarea" placeholder="Write a comment"></textarea>'
                      +'            <button id="card-button-add-comment" name="" class="btn btn-secondary card-button-add-comment mt-1 float-right display-none">Save</button>'
                     +'              <button id="card-button-cancel-comment" name="" class="btn btn-secondary card-button-add-comment mt-1 float-right display-none">Cancel</button>'

                     +'      </div>';
                     if(comments){
                            html += '      <!-- Comments -->'
                         +'      <div class="left-portion-of-header col-lg-12 col-md-12 col-sm-12">'
                         +'           <hr class="hr">'
                         +'       </div>'
                          +'      <div class="left-portion-of-header col-lg-9 col-md-9 col-sm-9">'
                          +'            <h5 class="modal-card-add-comment" id="exampleModalLabel">Comments</h5>'
                          +'     </div>';
                     }
                    
                      index = 0;
                      while(index < comments.length){
                            date_commented = new Date(comments[index].fields.date_commented);
                            date_commented = formatDate(date_commented);
                            html +='      <!-- To Loop -->'
                            +'       <div class="left-portion-of-header col-lg-12 col-md-12 col-sm-12">'
                            +'            <hr class="hr">'
                             +'       </div>'
                             +'         <div class="left-portion-of-header col-lg-9 col-md-9 col-sm-9">'

                             +'             <p class="card-comment-user" id="exampleModalLabel"><strong>'+comments[index].fields.user+'</strong> ('+date_commented+')</p>'
                             +'             '
                             +'             <div  id="DivisionComment-'+comments[index].pk+'" class="card-comments" name="" novalidate="">'+comments[index].fields.comment+'</div>'
                             +'             <textarea id="InputComment-'+comments[index].pk+'" class="textarea card-comments display-none">'+comments[index].fields.comment+'</textarea>'

                             +'             <button data-value="'+comments[index].pk+'" id="EditComment" class="float-left additional-option-comment link-style btn btn-warning">Edit</button>'
                             +'             <button data-value="'+comments[index].pk+'" data-toggle="modal" data-target="#DeleteCommentModal" id="DeleteComment" class="float-left additional-option-comment link-style btn btn-danger" data-dismiss="modal">Delete</button>'
                             +'           <button data-value="'+comments[index].pk+'" name="" id="card-save-button" class="btn btn-secondary card-button-add-description mt-1 float-right display-none">Save</button>'
                             +'           <button data-value="'+comments[index].pk+'" name="" id="card-cancel-button"class="btn btn-secondary card-button-add-description mr-2 mt-1 float-right display-none">Cancel</button>'
                             +'         </div>'
                             +'      '
                             +'               '
                              +'      <!-- Too Loop? -->';
             
                            index+=1;
                      }
                      html+=' </div>'
                            +'    </div>'
                            +'  </div>';
             $(".class-details-reactor").html(html);
             $("#CardModal").modal('show');
        }

        // Reloading the board
        reload_inner_wrapper = function(data){
            columns = JSON.parse(data.column);
            cards = JSON.parse(data.card);
            add_popped_url=$('#list-form').data('url');
            archived_popped_url = $('#hidden-column-archive-values').val();
            update_popped_url = $('#hidden-column-update-values').val();
            add_card_popped_url = $('#hidden-card-add-values').val();
            $('.inner-wrap').empty();
            var a = 0;
            html = "";            while(a < columns.length){
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
                                      +' class="card-reactor" data-toggle="modal" data-target="#CardModal"'
                                      +' data-value="'+column_id+'">'
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


        // Ajax Calls
        $(document).on('submit','#list-form', function(e){
            e.preventDefault()
            var title = $('#add-list').val()
            data = {
                title : title
            }
            var url = $(this).attr('action');
             console.log(url);
            $.post(url,data,reload_inner_wrapper,'json'), function(err){

            };
        });


        $(document).on("click", '.card-reactor', function(){
            // Loading card values to modal
            card_id = $(this).data('card_id');
            data = {
              card_id : card_id
            }
             var url = $(this).data('action');
             $.get(url,data,reload_card,'json'), function(err){

            };
        });

        $(document).on('submit','.existing-form', function(e){
            e.preventDefault()
            id=$(this).data('value');
            var title = $('#exist-list-' + id).val();
            data = {
                title : title,
                id : id
            }
            var url = $(this).attr('action');

            console.log(url);
            if (url == undefined){
                url = $('#hidden-column-update-values').val();
            }
            $.post(url,data,reload_inner_wrapper,'json'), function(err){

            };
        });

        $(document).on("input", "#input-card-title", function(){
          
            $.post(url,data,reload_inner_wrapper,'json'), function(err){

            };
        });

        $(document).on('submit','#archive-form', function(e){
            e.preventDefault()
            id=$(this).data('value');

            data = {
                id : id
            }
            var url = $(this).attr('action');

            console.log(url);
            if (url == undefined){
                url = $('#hidden-column-archive-values').val();
            }
            $.post(url,data,reload_inner_wrapper,'json'), function(err){

            };
        });


        $(document).on('submit','.card-add-form-class', function(e){
            console.log("hello");
            e.preventDefault()
            id=$(this).data('value');
            console.log($(this).attr('action'));
            name = $("#add-card-"+id).val();
            data = {
                name : name,
                id : id
            }
            var url = $('.card-add-form-class').attr('action');
            if (url == undefined){
                url = $('#hidden-card-add-values').val();
                console.log(url);
            }
                
            $.post(url,data,reload_inner_wrapper,'json'), function(err){
                console.log('error');
            };
        });

        
});