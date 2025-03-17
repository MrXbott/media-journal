
$(document).ready(function(){
    $(document).on('submit', '#comment', function(e){
        e.preventDefault();
        var formData = $(this).serialize();
        // console.log(formData);
        // console.log('submit comment pressed');
        $.ajax({
            type: 'POST',
            url: '/comment/',
            data: formData,
            success: function(json){
                console.log(json)
                if (json['status'] == 'ok'){
                    // console.log('comment saved');  
                    let comment_text = '<b>'+ json['created'] + ' ' + json['username'] +'</b> ' + json['comment'];
                    $('div#comments').append($('<div>').attr({'class': 'comment'}).html(comment_text));
                    $('textarea#id_body').val('');
                }
                
            },
            error: function(xhr, errmsg, err){
                console.log(xhr.status);
            }
        });
    });
});