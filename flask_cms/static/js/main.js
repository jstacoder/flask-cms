var $ = require('jquery');
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
