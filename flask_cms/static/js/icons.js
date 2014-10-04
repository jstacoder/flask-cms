// function defs
function getIconLib(icon) {
    var classStr = $(icon).children().attr("class").split(" ")[0];
        switch(classStr) {
            case 'glyphicon':
                var rtn = 'Glyphicons';
                break;
             case 'el-icon':
                var rtn = 'Elusive-Icons';
                break;
             case 'icon':
                var rtn = 'Mfg-Labs';
                break;
             case 'octicon':
                var rtn = 'Octicons';
                break;
             case 'fa':
                var rtn = 'Font-Awesome';
                break;
             case 'ion':
                var rtn = 'Ionicons';
                break;
             case 'genericon':
                var rtn = 'Genericons';
                break;
             default:
                var rtn = null;
        }
    return rtn;
}

function displayIcon(elem) {
    var idx = $("dd").index($(elem));
    var lib = getIconLib(elem);
    $(".modal-title")
        .text(
                $(elem)
                .siblings()
                .eq(0)
                .text() + ' - ' + lib
        );
    $(".modal-body")
        .html(
          $(elem)
        .html());
    $("#myModal")
        .data("current_index",idx);
    if($("#myModal").css("display") == 'none'){
        $("#myModal")
            .modal();
    }
}
                
function toggleChevron(elem) {
    if(elem.hasClass("icon-chevron_up")){
        elem.removeClass("icon-chevron_up").addClass("icon-chevron_down");
    } else {
        if ($(".icon-chevron_up").length) {
            $(".icon-chevron_up").removeClass("icon-chevron_up").addClass("icon-chevron_down");
        }
        elem.removeClass("icon-chevron_down").addClass("icon-chevron_up");

    }
}


function addSpin(elem) {
    $(elem).addClass("fa-spin");
}

function removeSpin(elem) {
    $(elem).removeClass("fa-spin");
}

function checkSpin(elem){
    return $(elem).hasClass("fa-spin");
}

function toggleSpin(elem){
    if(!checkSpin(elem)){
        addSpin(elem);
    } else {
        removeSpin(elem);
    }
}

function toggleOpen(elem) {
    var e = $(elem);
    if (elem.hasClass("open")){        
        e.removeClass("open")
         .slideUp('slow');
    } else {
        if ($(".open").length) {
            $(".open").removeClass("open")
                      .slideUp('slow');
        }
        e.addClass("open")
         .slideDown('slow');
    }
}        
// Onload event handler
$(function(){                     
    $(".lib-name").on("click",function(){
        toggleChevron(
            $(".lib-name .icon")
                .eq($(".lib-name")
                .index($(this))
            )
        );
        toggleOpen(
            $(".lib-name + .icons")
                .eq($(".lib-name")
                .index($(this))
            )
        );
    });

    $(".spin-btn").on("click",function(){
        toggleSpin($(".modal-body > span"));
    });
                     
    $("dd").on("click",function(){                 
        displayIcon(this);
    });
    $(".modal-arrow").on("click",function(){
        var direction = $(this)
            .hasClass("pull-left") ? 'left' : 'right';
        var idx = $("#myModal")
            .data("current_index");                        
        var oldIdx = idx;
        if(direction == 'left'){
            idx--;
        }else{
            idx++;
        }
        displayIcon($("dd")
            .eq(idx)[0]);                        
        }
    );
});
