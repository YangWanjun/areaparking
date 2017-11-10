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

EB.prototype.isNumeric = function(num) {
    return !isNaN(num);
}

EB.prototype.toNumComma = function(num) {
    int_comma = (num + "").replace(/(\d)(?=(\d{3})+(?!\d))/g, '$1,');
    return int_comma;
}

EB.prototype.popup_anchor = function() {
    $('a.popup').on('click', function() {
        var href = $(this).attr('href');
        window.open(href, "", "width=750, height=500");
        return false;
    });
}

EB.prototype.reset_whiteboard_row = function(tr, idx) {
    var self = this;
    tr = $(tr)
    var row1 = tr.clone();
    var row2 = tr.clone();
    var row3 = tr.clone();
    row1.html("");
    row2.html("");
    row3.html("");
    row1.css("border-bottom-style", "dotted");
    row2.css("border-bottom-style", "dotted");
    if (idx % 2 == 0) {
        row1.css("background-color", "#f2f2f2");
        row2.css("background-color", "#f2f2f2");
        row3.css("background-color", "#f2f2f2");
    }
    bk_no                           = tr.children().eq(0);
    parking_lot                     = tr.children().eq(1);
    parking_position                = tr.children().eq(2);
    contract_status                 = tr.children().eq(3);
    is_existed_contractor_allowed   = tr.children().eq(4);
    is_new_contractor_allowed       = tr.children().eq(5);
    free_end_date                   = tr.children().eq(6);
    time_limit_id                   = tr.children().eq(7);
    address                         = tr.children().eq(8);
    tanto_name                      = tr.children().eq(9);
    price_recruitment               = tr.children().eq(10);
    price_recruitment_no_tax        = tr.children().eq(11);
    price_homepage                  = tr.children().eq(12);
    price_homepage_no_tax           = tr.children().eq(13);
    price_handbill                  = tr.children().eq(14);
    price_handbill_no_tax           = tr.children().eq(15);
    length                          = tr.children().eq(16);
    width                           = tr.children().eq(17);
    height                          = tr.children().eq(18);
    weight                          = tr.children().eq(19);
    tyre_width                      = tr.children().eq(20);
    tyre_width_ap                   = tr.children().eq(21);
    min_height                      = tr.children().eq(22);
    min_height_ap                   = tr.children().eq(23);
    f_value                         = tr.children().eq(24);
    r_value                         = tr.children().eq(25);
    position_comment                = tr.children().eq(26);

    bk_no.attr("rowspan", 3);
    parking_lot.attr("colspan", 5);
    address.attr("colspan", 4);
    address.css("padding-left", "5px");

    row1.append(bk_no);
    row1.append(parking_lot);
    row1.append(parking_position);
    row1.append(contract_status);
    if (contract_status.text() === "空き") {
        contract_status.html('<span class="new badge left green" data-badge-caption="空き" style="margin-left: 0px;"></span>');
    } else if (contract_status.text() === "手続中") {
        contract_status.html('<span class="new badge left deep-orange" data-badge-caption="手続中" style="margin-left: 0px;"></span>');
    } else {
        contract_status.html('<span class="new badge left grey" data-badge-caption="なし" style="margin-left: 0px;"></span>');
    }
    row1.append(is_existed_contractor_allowed);
    row1.append(is_new_contractor_allowed);
    row1.append(free_end_date);
    row1.append(time_limit_id);
    $('td', row1).each(function() {
        $(this).css('display', '');
    });

    row2.append(address);
    row2.append(tanto_name);
    row2.append(price_recruitment);
    row2.append(price_recruitment_no_tax);
    row2.append(price_homepage);
    row2.append(price_homepage_no_tax);
    row2.append(price_handbill);
    if (price_handbill_no_tax.html() == "") {
        price_handbill_no_tax.html("&nbsp");
    }
    row2.append(price_handbill_no_tax);
    $('td', row2).each(function() {
        $(this).css('display', '');
    });

    row3.append(length);
    row3.append(width);
    row3.append(height);
    row3.append(weight);
    row3.append(tyre_width);
    row3.append(tyre_width_ap);
    row3.append(min_height);
    row3.append(min_height_ap);
    row3.append(f_value);
    row3.append(r_value);
    // 車室の備考
    if (position_comment.html() == "") {
        position_comment.html("&nbsp;");
    } else {
        if (position_comment.text().length > 5) {
            text = position_comment.text();
            position_comment.addClass("tooltipped");
            position_comment.attr("data-position", "top");
            position_comment.attr("data-delay", "50");
            position_comment.attr("data-tooltip", text);
            position_comment.text(text.substring(0, 4) + "...");
        }
    }
    row3.append(position_comment);
    $('td', row3).each(function() {
        $(this).css('display', '');
        if (self.isNumeric($(this).text())) {
            $(this).css('text-align', 'right');
            $(this).text(self.toNumComma($(this).text()));
        }
    });

    return [row1, row2, row3];
}

var eb = new EB();