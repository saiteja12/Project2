var url = window.location.href


$(document).ready(function () {

});

logout = function () {
    var splitArr = url.split('/');
    splitArr[3] = "logout"
    $.ajax({
        url: splitArr.join('/'),
        type: 'get',
        dataType: 'json',
        success: function (data) {
            if (data.success == true) {
                window.location = '/';
            }
        }
    });
}
