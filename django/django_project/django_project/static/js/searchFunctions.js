$(document).ready(function(){
    $("#search_input").autocomplete({
        source: "search/",
        minLength: 1,
        theme: "square",
        select: function( event, ui ) {
            window.location.href = "?query="+ui.item.value;
        }
    });
    $("#search_input").keypress(function(e){
        if(e.keyCode==13){
            $('#search_btn').click();
            }
    });

    $(".page_number").click(function(){
        page = parseInt($('#pagination-id').val());
        if (this.id == 2){
            page = page + 1;
        }
        else if (this.id == 0){
            page = page - 1;
        }
        else{
            page = parseInt($(this).text());
        }
        window.location.href = "?query="+GetURLParameter("query")+"&page="+page;
     })

     $("#search_btn").click(function(){
        window.location.href = "?query="+$("#search_input").val();
    });
});

function GetURLParameter(sParam){
    var sPageURL = window.location.search.substring(1);
    var sURLVariables = sPageURL.split('&');
    for (var i = 0; i < sURLVariables.length; i++){
        var sParameterName = sURLVariables[i].split('=');
        if (sParameterName[0] == sParam){
           return sParameterName[1];
        }
    }
    return '';
}