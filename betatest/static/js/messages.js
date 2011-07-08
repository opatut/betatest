// message list selection

function formAllSelected(form) {
    return form.find("input.selection").length == form.find("input.selection:checked").length;
}

function selectAllCheck(form) {
    if(formAllSelected(form)) {
        form.find(".select_all").val("Unselect all");
    } else {
        form.find(".select_all").val("Select all");
    }
}

function toggleSelectAll(form) {
    new_v = !formAllSelected(form);
    form.find("input.selection").each(function() {
        $(this).attr("checked", new_v);
        toggleSelected($(this));
    });
}

function toggleSelected(input) {
    if(input.attr("checked")) {
        input.closest("li").addClass("selected");
    } else {
        input.closest("li").removeClass("selected");
    }
    selectAllCheck(input.closest("form"));
}

$(document).ready(function() {
    $("ul.message-list-ul li").click(function() {
        var $c = $(this).find("input.selection");
        $c.attr("checked", !$c.attr("checked"));
        toggleSelected($c);
    }).dblclick(function() {
        window.location.href = $(this).find("a.message_title").attr("href");
    });

    $("ul.message-list-ul li input.selection").click(function() {
        $(this).attr("checked", !$(this).attr("checked"));
        toggleSelected($(this));
    });

    $("ul.message-list-ul li input.selection").each(function() {
        toggleSelected($(this));
    });

    $(".select_all").click(function() {
        toggleSelectAll($(this).closest("form"));
    })

    $(".no-js-hide").css("visibility","visible");

    $('.user-autocomplete').autocomplete({
        serviceUrl:'/ajax/users/autocomplete',
        minChars: 1,
        delimiter: /\s*[^a-zA-Z0-9_-]+\s*/,
        maxHeight: 200,
        zIndex: 9999,
        noCache: false
    });
});
