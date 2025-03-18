var empty_page = false; 
var block_request = false;

function get_comments(page, article_id){
    console.log('getting comments');
    $.ajax({
        type: 'GET',
        url: '/comments/',
        data: {'page': page, 'article_id': article_id},
        success: function(data){
            if(data == '') {
                empty_page = true;
                $('.more').addClass('hide');
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
    var article_id = $('input#id_article').val();
    var page = 1;
    
    get_comments(page=page, article_id=article_id);

    $('.more').on('click', function() {
        if (empty_page == false && block_request == false) {
            block_request = true;
            page += 1;
            get_comments(page, article_id);
        }
    });
});

