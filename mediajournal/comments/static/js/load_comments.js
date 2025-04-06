var empty_page = false; 
var block_request = false;

function get_comments(page, object_id, object_type){
    console.log('getting comments');
    $.ajax({
        type: 'GET',
        url: '/comments/',
        data: {'page': page, 'id': object_id, 'type': object_type},
        success: function(data){
            console.log('success');
            if(data == '') {
                empty_page = true;
                $('.more-comments').addClass('hide');
            } 
            else {
                block_request = false;
                $('#comments-list').append(data); 
            }
        },
        error: function(xhr, errmsg, err){
            console.log(xhr.status);
        }
    });
}

$(document).ready(function(){
    var object_id = $('#comments').attr('data-id');
    var object_type = $('#comments').attr('data-type');
    console.log('id ', object_id, object_type);
    var page = 1;
    
    get_comments(page, object_id, object_type);

    $('.more-comments').on('click', function() {
        if (empty_page == false && block_request == false) {
            block_request = true;
            page += 1;
            get_comments(page, object_id, object_type);
        }
    });
});

