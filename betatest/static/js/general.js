// general js

$(document).ready(function() {
    $("*[title]").tooltip({
        showURL: false,
        track: false,
        tagName: "title",
        fade: true,
        delay: 500,
        left: 15,
        top: 5
    });

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
