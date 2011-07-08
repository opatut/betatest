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
});
