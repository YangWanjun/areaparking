$(document).ready(function() {
    $(".card-action").hide();
    showHtml();
    hideId();
});

function showHtml() {
    var htmlNode = $("label:contains('メール本文')").next();
    var html = htmlNode.val();
    var div = $.parseHTML('<div contenteditable="true" style="padding: 15px 0px; color: gray;"></div>');
    $(div).html(html);
    htmlNode.replaceWith(div);
}

function hideId() {
    var idNode = $("label:contains('Id')").next();
    idNode.closest('div.row').hide();
}
