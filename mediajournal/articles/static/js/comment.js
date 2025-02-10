
$(document).ready(function(){
    $(document).on('submit', '#comment', function(e){
        e.preventDefault();

        console.log('submit comment pressed');
        console.log($('#id_text').val(), $('#article_id').val());
        $.ajax({
            type: 'POST',
            url: '/comment/',
            data: {
                text: $('#id_text').val(),
                article_id: $('#article_id').val(),
                csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
                action: 'post'
            },
            success: function(json){
                console.log(json)
                if (json['status'] == 'ok'){
                    console.log('comment saved');  
                    console.log($('#comments div.comment:last'))  ;
                    let comment = $('#comments div.comment:last').clone();
                    comment.empty();
                    comment.append('<b>'+ json['created'] + ' ' + json['username'] +'</b> ' + json['body']);
                    console.log(comment);
                    $(comment).insertAfter( $('#comments div.comment:last') );
                    // text = $('#id_text').val();
                    // $('<div id="NextElement">' + text + '</div>').insertAfter( $('#comments div.comment:last') );
                }
                
            },
            error: function(xhr, errmsg, err){
                console.log(xhr.status);
            }
        });
    });
});