/*Based on: http://djangosnippets.org/snippets/1053/*/

$(function() {
    $('div.inline-group').sortable({
        /*containment: 'parent',
        zindex: 10, */
        items: 'div.inline-related',
        handle: 'h3:first',
        update: function() {
            $(this).find('div.inline-related').each(function(i) {
                if ($(this).find('input[id$=name]').val()) {
                    $(this).find('input[id$=order]').val(i+1);
                }
            });
        }
    });
    $('div.inline-related h3').css('cursor', 'move');
    i/*$('div.inline-related').find('input[id$=order]').parent('div').hide();*/
});
   
