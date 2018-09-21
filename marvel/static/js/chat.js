
$('#msg_f').on('submit',function(event) {
	event.preventDefault();

	$.ajax({
		url : '/login/post/',
		type: 'POST',
		data: {recv : $('#rev').val() ,msgbox : $('#msgbox').val() },
		success : function(json){
			$('#msgbox').val('');
			$('#msg_b').append('<div class="msg_right"><p class="msg">'+json.msg+'</p></div>');

		}
	}).done(function (){
		document.location.reload(); 
	});
});

$("#msg_b").scrollTop($('#msg_b').height())
// using jQuery
// function getCookie(name) {
//     var cookieValue = null;
//     if (document.cookie && document.cookie !== '') {
//         var cookies = document.cookie.split(';');
//         for (var i = 0; i < cookies.length; i++) {
//             var cookie = jQuery.trim(cookies[i]);
//             // Does this cookie string begin with the name we want?
//             if (cookie.substring(0, name.length + 1) === (name + '=')) {
//                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                 break;
//             }
//         }
//     }
//     return cookieValue;
// }
// var csrftoken = getCookie('csrftoken');

// function csrfSafeMethod(method) {
//     // these HTTP methods do not require CSRF protection
//     return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
// }
// $.ajaxSetup({
//     beforeSend: function(xhr, settings) {
//         if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
//             xhr.setRequestHeader("X-CSRFToken", csrftoken);
//         }
//     }
// });