var interval = undefined;
$(document).ready(function () {
    interval = setInterval(getNext, 2000); // milliseconds
    $('#next').on('click', getNext);
    $('#prev').on('click', getPrev);
});

function getNext() {
  $('#title0').html(course_name)
}

function getPrev() {
    var $curr = $('.courses').show();
        $next = ($curr.prev().length) ? $curr.prev() : $('.courses').last();
    transition($curr, $next);
}

function transition($curr, $next) {
    clearInterval(interval);

    $next.css('z-index', 2).fadeIn('slow', function () {
        $curr.hide().css('z-index', 0);
        $next.css('z-index', 1);
    });
}