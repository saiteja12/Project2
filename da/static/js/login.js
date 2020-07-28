var path = location.hostname;

$(document).ready(function () {

    $("#username").val('');
    $("#password").val('');

    });
login = function () {
    $.ajax({
        url: 'login/',
        type: 'post',
        dataType: 'json',
        data: JSON.stringify({ 'username': $("#username").val(), 'password': $("#password").val() }),
        success: function (data) {
            if (data.success == true) {
                window.location='/home/';
            }
             else {
                alert("check Username/Password");
            }
        }
     });
}
