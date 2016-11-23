$(document).ready(function() {
    $('[data-iframe]').click(function(e) {
	e.preventDefault();
	$('iframe' + $(this).data('iframe')).prop('src', $(this).prop('href'));
	return false;
    });
    $('.markdown').each(function() {
	$(this).html(marked($(this).text()));
    });
    $('[data-open-image]').click(function(e) {
	e.preventDefault();
	var full_image = $('#full-image');
	var main = $('main');
	var onClick = function(e) {
	    e.preventDefault();
	    full_image.hide();
	    full_image.hide();
	    main.show();
	    return false;
	};
	full_image.find('img').prop('src', $(this).prop('href'));
	full_image.find('img').unbind('click');
	full_image.find('img').click(onClick);
	full_image.find('#full-image-close-button').unbind('click');
	full_image.find('#full-image-close-button').click(onClick);
	main.hide();
	full_image.show();
	return false;
    });
});
