function iframes() {
    $('[data-iframe]').click(function(e) {
        e.preventDefault();
        $('iframe' + $(this).data('iframe')).prop('src', $(this).prop('href'));
        return false;
    });
}

function markdowns() {
    $('.markdown:not(.marked)').each(function() {
        $(this).html(marked($(this).text()));
        $(this).addClass('marked');
    });
}

function openImages() {
    $('[data-open-image]').click(function(e) {
        e.preventDefault();
        var full_image = $('#full-image');
        var main = $('main');
        var nav = $('.bottom-right-buttons');
        var onClick = function(e) {
            e.preventDefault();
            full_image.hide();
            main.show();
            nav.show();
            return false;
        };
        full_image.find('img').prop('src', $(this).prop('href'));
        full_image.find('img').unbind('click');
        full_image.find('img').click(onClick);
        full_image.find('#full-image-close-button').unbind('click');
        full_image.find('#full-image-close-button').click(onClick);
        nav.hide();
        main.hide();
        full_image.show();
        return false;
    });
}

function openTexts() {
    $('[data-open-text]').click(function(e) {
        e.preventDefault();
        var button = $(this);
        var full_text = $('#full-text');
        var main = $('main');
        var nav = $('.bottom-right-buttons');
        var onClick = function(e) {
            e.preventDefault();
            full_text.hide();
            main.show();
            nav.show();
            return false;
        };
        full_text.find('p').text(button.find('.content').text());
        if (button.data('open-text-markdown')) {
            full_text.find('p').addClass('markdown');
            markdowns();
        }
        full_text.find('#full-text-close-button').unbind('click');
        full_text.find('#full-text-close-button').click(onClick);
        nav.hide();
        main.hide();
        full_text.show();
        return false;
    });
}

function infiniteScroll() {
    var win = $(window);
	  win.scroll(function() {
		    if ($(document).height() - win.height() == win.scrollTop()) {
			      $('.loading').show();
			      $.ajax({
                data: {
                    ajax: true,
                    page: $('[data-next-page]').data('next-page'),
                },
				        dataType: 'html',
				        success: function(html) {
                    console.log(html);
                    $('[data-next-page]').replaceWith(html);
				        }
			      });
		    }
	  });
}

$(document).ready(function() {
    iframes();
    markdowns();
    openImages();
    openTexts();
    infiniteScroll();
});
