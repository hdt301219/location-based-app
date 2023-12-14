// jQuery
$(function() {

	// Switch to Forgot Password
	$('.forgotBtn').click(function() {
		$('#forgot').toggleClass('toggle');
	});
	
	// Switch to Register
	$('.registerBtn').click(function() {
		$('#register, #formContainer').toggleClass('toggle');
	});

});