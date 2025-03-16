$(document).ready(function () {
    $('#add_image').on('click', function () {
        let total_forms = $('#id_images-TOTAL_FORMS').val();
        let image_form = $('#empty_form').clone();
        let image_form_id = 'image-' + total_forms;
        $('#images_formset').append($('<div>').attr({'id': image_form_id}).append(image_form.html().replace(/__prefix__/g, total_forms)));
        $('#id_images-TOTAL_FORMS').val(parseInt(total_forms) + 1);
    });
});