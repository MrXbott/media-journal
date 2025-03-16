function validateImage(input){
    image = input.files[0];
    var allowed_extensions = new Array('jpg','jpeg', 'png');
    var file_extension = image.name.split('.').pop().toLowerCase(); 

    let parent_div = $(input).parent().parent();
    let message_div = $(parent_div).children('div.image-message')[0];

    if (!allowed_extensions.includes(file_extension)) {
        $(message_div).text('Allowed formats: jpg, jpeg, png');
        $(input).val('');
        return false;
    }
    if (image.size > 102400) {
        $(message_div).text('Image size must be less 100kb');
        $(input).val('');
        return false;
    }
    return true;
};

$(document).ready(function () {
    // $('#add_image').on('click', function () {
    //     let total_forms = $('#id_images-TOTAL_FORMS').val();
    //     let image_form = $('#empty_form').clone();
    //     let image_form_id = 'image-' + total_forms;
    //     $('#images_formset').append($('<div>').attr({'id': image_form_id}).append(image_form.html().replace(/__prefix__/g, total_forms)));
    //     $('#id_images-TOTAL_FORMS').val(parseInt(total_forms) + 1);
    // });


    $(document).on('change', 'input[id^="id_images-"]', function(){
        // e.stopPropagation();
        let parent_div = $(this).parent().parent();
        let message_div = $(parent_div).children('div.image-message')[0];
        $(message_div).text('');
        if (validateImage(this)) {
            $(this).parent().append($('<img>').attr({'src': URL.createObjectURL(this.files[0]), 'class': 'uploading-image'}));
            $(this).addClass('hide');
        };
        
    });

});