$(document).ready(function () {
    $('#add_image').on('click', function () {
        let total_forms = $('#id_images-TOTAL_FORMS').val();
        let image_form = $('#empty_form').clone();
        image_form.removeAttr('id').removeAttr('class');
        $('#images_formset').append(image_form.html().replace(/__prefix__/g, total_forms));
        $('#id_images-TOTAL_FORMS').val(parseInt(total_forms) + 1);
    });
});