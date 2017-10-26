function EB() {}

EB.prototype.getCookie = function(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
};

EB.prototype.csrfSafeMethod = function(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
};

EB.prototype.ajax_request = function(url, method, params, success, failure, always) {
    var self = this;
    var csrftoken = self.getCookie('csrftoken');

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!self.csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $.ajax({
        type: method,
        url: url,
        data: params,
        dataType: "json"
    }).done(function(result) {
        success(result);
    }).fail(function(result) {
        failure(result);
    }).always(function(result) {
        always(result);
    });
};

EB.prototype.reflection_form_errors = function(form_obj, errors) {
    // 既存のエラーを消す
    $("div.errors", form_obj).remove();
    $.each(errors, function(name, messages) {
        div_error = $.parseHTML('<div class="errors"></div>');
        $.each(messages, function(i, msg) {
            $(div_error).append('<small class="error">' + msg + '</small>');
        });
        $("#id_" + name, form_obj).after(div_error);
    });
}

var eb = new EB();