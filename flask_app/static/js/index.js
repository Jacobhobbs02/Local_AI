/* popUp function for ALL buttons */
function popOut(element) {
    element.classList.add('hidden');
    setTimeout(() => {
        element.remove();
    }, 500);
}

/* Show Password Button */
function togglePasswordVisibility(passwordFieldId, toggleButtonId) {
    const passwordField = document.getElementById(passwordFieldId);
    const togglePasswordButton = document.getElementById(toggleButtonId);
    const type = passwordField.getAttribute('type') === 'password' ? 'text' : 'password';
    
    passwordField.setAttribute('type', type);
    togglePasswordButton.src = type === 'password' 
        ? url('../images/show_button.png') 
        : url('../images/show_button.png');
}

/* Show Confirm Password button */
function toggleConfirmPasswordVisibility(passwordFieldId, toggleButtonId) {
    const confirmPasswordField = document.getElementById(passwordFieldId);
    const toggleConfirmPasswordButton = document.getElementById(toggleButtonId);
    const type = confirmPasswordField.getAttribute('type') === 'password' ? 'text' : 'password';
    
    confirmPasswordField.setAttribute('type', type);
    toggleConfirmPasswordButton.src = type === 'password' 
        ? url('../images/show_button.png') 
        : url('../images/show_button.png');
}