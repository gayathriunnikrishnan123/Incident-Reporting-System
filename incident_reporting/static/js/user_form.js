
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('userCreationForm');


    const password = document.getElementById('id_password');
    const confirmPassword = document.getElementById('id_confirm_password');
    const confirmError = document.getElementById('confirm-password-error');

    function validatePasswordMatch() {
        if (confirmPassword.value && password.value !== confirmPassword.value) {
            confirmError.textContent = 'Passwords do not match';
            confirmPassword.style.borderColor = '#e53e3e';
        } else {
            confirmError.textContent = '';
            confirmPassword.style.borderColor = '#e2e8f0';
        }
    }

    if (password && confirmPassword) {
        password.addEventListener('input', validatePasswordMatch);
        confirmPassword.addEventListener('input', validatePasswordMatch);
    }

    // Form submission handling
    form.addEventListener('submit', function(e) {
        // Clear previous errors
        const clientErrors = document.querySelectorAll('.error-message:empty');
        clientErrors.forEach(error => {
            error.textContent = '';
        });


        let isValid = true;
        const requiredFields = [
            { id: 'id_email', name: 'email' },
            { id: 'id_fullname', name: 'fullname' },
            { id: 'id_phone', name: 'phone' },
            { id: 'id_password', name: 'password' },
            { id: 'id_confirm_password', name: 'confirm_password' }
        ];
        
        requiredFields.forEach(field => {
            const fieldElement = document.getElementById(field.id);
            if (fieldElement && !fieldElement.value.trim()) {
                fieldElement.style.borderColor = '#e53e3e';
                isValid = false;
            } else if (fieldElement) {
                fieldElement.style.borderColor = '#e2e8f0';
            }
        });

        // Email validation
        const emailField = document.getElementById('id_email');
        const emailError = document.getElementById('emailval-error');
        if (emailField && emailField.value) {
            const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailPattern.test(emailField.value)) {
                emailField.style.borderColor = '#e53e3e';
                emailError.textContent = 'Email not valid'
                isValid = false;
            }
        }

        // Password match validation
        if (password && confirmPassword && password.value !== confirmPassword.value) {
            confirmError.textContent = 'Passwords do not match';
            confirmPassword.style.borderColor = '#e53e3e';
            isValid = false;
        }

        // If not all vaid stop submiting
        if (!isValid) {
            e.preventDefault();
            return false;
        }

        // Show loading state
        const submitBtn = document.querySelector('.submit-btn');
        const originalText = submitBtn.textContent;
        submitBtn.textContent = 'Creating Account...';
        submitBtn.disabled = true;

        // Re-enable button so that we can shetup something like fallback
        setTimeout(() => {
            if (submitBtn.textContent === 'Creating Account...') {
                submitBtn.textContent = originalText;
                submitBtn.disabled = false;
            }
        }, 10000);
    });

    // Phone number formatting
    const phoneField = document.getElementById('id_phone');
    if (phoneField) {
        phoneField.addEventListener('input', function(e) {
            // Remove all non-digits
            let value = e.target.value.replace(/\D/g, '');
            
            // only 10 needed
            if (value.length > 10) {
                value = value.slice(0, 10);
            }
            
            e.target.value = value;
        });
    }

    // Form field error handling
    const formFields = document.querySelectorAll('input, select');
    formFields.forEach(field => {
        field.addEventListener('blur', function() {
            // Reset border color when field loses focus and has value
            if (this.value.trim() && this.style.borderColor === 'rgb(229, 62, 62)') {
                this.style.borderColor = '#e2e8f0';
            }
        });

        field.addEventListener('focus', function() {
            // Reset border color when field gets focus
            if (this.style.borderColor === 'rgb(229, 62, 62)') {
                this.style.borderColor = '#667eea';
            }
        });
    });

    // Handle form errors from Django
    const errorFields = document.querySelectorAll('.error-message');
    errorFields.forEach(errorElement => {
        if (errorElement.textContent.trim()) {
            
            const formGroup = errorElement.closest('.form-group');
            if (formGroup) {
                const inputField = formGroup.querySelector('input, select');
                if (inputField) {
                    inputField.style.borderColor = '#e53e3e';
                }
            }
        }
    });
});