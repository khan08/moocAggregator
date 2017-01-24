$(document).ready(function(){
     $("#search_input").keyup(function(){
        $('#courselist').empty();
        delay(function(){
                        console.log($('#search_input').val())
                        $.ajax({
                            async: true,
                            type:'GET',
                            url:"search/",
                            data:{
                                ajaxsearch: $('#search_input').val(),
                                page: 1,
                            },
                            success:function(result){
                                loadbutton_id = '#loadbutton_id';
                                //console.log(result)
                                $('#courselist').html(result);

                            }
                        })},500);
               });
     $("#loadbutton_id").click(function(){
                        page = parseInt($('#pagination-id').val());
                        //console.log(page);
                        page = page + 1;
                        $.ajax({
                            async: true,
                            type:'GET',
                            url:"search/",
                            data:{
                                ajaxsearch: $('#search_input').val(),
                                page : page,
                            },

                            success:function(result){
                                //console.log(result);
                                $('#pagination-id').val(page);
                                console.log($('#pagination-id').val())
                                $('#courselist').html(result);
                            }
                        })

     })

     })

var delay = (function(){
  var timer = 0;
  return function(callback, ms){
    clearTimeout (timer);
    timer = setTimeout(callback, ms);
  };
})();

function ajaxsearch(){
    

}