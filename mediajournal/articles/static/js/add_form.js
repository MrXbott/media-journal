$(document).ready(function () {
    $('#add_image').on('click', function () {
        let total_forms = $('#id_images-TOTAL_FORMS').val();
        let image_form = $('#image_empty_form').clone();
        let image_form_id = 'image-' + total_forms;
        $('#images_formset').append($('<div>').attr({'id': image_form_id}).append(image_form.html().replace(/__prefix__/g, total_forms)));
        $('#id_images-TOTAL_FORMS').val(parseInt(total_forms) + 1);
    });

    $('#add_section').on('click', function(){
        let btn = this;
        console.log('btn clicked');
        let total_forms = parseInt($('#id_sections-TOTAL_FORMS').val());
        let max_forms = $('#id_sections-MAX_NUM_FORMS').val();
        let section_form = $('#section_empty_form').clone();
        let section_form_id = 'section-' + total_forms;
        
        // $(section_form).find('input[type="button"]').attr({'data-id': section_form_id});

        // console.log(del_btn_id);
        if (total_forms < max_forms) {
            $('#sections_formset').append($('<div>').attr({'class': 'section-container'}).append(section_form.html().replace(/__prefix__/g, total_forms)));
            total_forms = total_forms + 1;
            $('#id_sections-TOTAL_FORMS').val(total_forms);
        };
        if (total_forms == max_forms) {
            $(btn).addClass('disabled');
        }
    });

    $(document).on('click', '#sections_formset input[type="button"]', function(){
        console.log('del btn clicked');
        let del_btn = this;
        // let section_id = $(this).attr('data-id');
        let total_forms = parseInt($('#id_sections-TOTAL_FORMS').val());
        // console.log(section_id);
        // $('div#' + section_id).remove();
        
        console.log($(del_btn).closest('div.section-container'));
        // let section_div = $(del_btn).closest('div.section-container');
        $(del_btn).closest('div.section-container').remove();
        $('#id_sections-TOTAL_FORMS').val(total_forms - 1);
    });
});