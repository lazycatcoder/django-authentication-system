document.addEventListener('DOMContentLoaded', function() {
    var usernameInput = document.getElementById('user-signup');
    var passwordInput = document.getElementById('password1');
  
    usernameInput.value = '';
    passwordInput.value = '';
  });
  

document.addEventListener('DOMContentLoaded', function() {
var usernameInput = document.getElementById('user-signup');
var passwordInput = document.getElementById('password1');

if (usernameInput && passwordInput) {
    usernameInput.value = '';
    passwordInput.value = '';

    usernameInput.setAttribute('value', '');
    passwordInput.setAttribute('value', '');
}
});
 
    
$(document).ready(function() {
    $('#tab-1').on('click', function() {
        window.history.pushState({}, '', '/auth/login/');
    });

    $('#tab-2').on('click', function() {
        window.history.pushState({}, '', '/auth/signup/');
    });
});