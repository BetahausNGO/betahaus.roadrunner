
function handle_errors(form_elem, response) {
    console.log('handle errors with form: ', form_elem)
    $.each(response, function(a, b) {
        console.log(a,b)
    })
}

function reset_errors(form_elem) {
    console.log('reset errors on form: ', form_elem)
    form_elem.find('.form-group.has-error').each(function() {
        $(this).removeClass('has-error');
    })
}

$(document).ready(function () {
    //$('body').on('submit', '[data-inline-edit]', function(event) {
    $('[data-inline-edit]').on('submit', function(event) {
        event.preventDefault();
        var form = $(this);
        var url = form.attr('action');
        var request = arche.do_request(url, {data: form.serialize(), method: 'post'});
        request.done(function(response) {
            console.log(response);
            if (response['errors'] != null) {
                handle_errors(form, response['errors']);
            } else {
                reset_errors(form);
            }
        });
    });
});
