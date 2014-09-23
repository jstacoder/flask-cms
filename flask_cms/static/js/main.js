var $ = jQuery;
$(document).ready(function($) {
    $(document).ready(function(){
        var c = $("<div>").addClass('content_block')
        .appendTo($("body"));
    
        $("a").click(function(e){
            e.preventDefault();
        });
        $(".content_block").click(function(){
            var ID = $(this).attr("id");
            var txt = $("."+ID).text();
            alert(txt);
        });
    });
});
add_grid = function(){
    $(".box:not(.sidebar)").css(
        "border","solid 2px black"
    );
    $(".box:not(.sidebar)").css(
        "min-height","145px"
    );
    $(".content-column").css(
        "height","580px"
    );
    $(".sidebar").css(
            "border","0"
    );
    $(".content").css(
            "height","auto"
    );
    $(".footer .box").css(
            "min-height","90px"
    );
}
