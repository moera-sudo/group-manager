document.addEventListener('DOMContentLoaded', function() { /// 
        // Password validation function
        function validatePassword(password) {
        const errors = [];

        if (password.length < 8) {
            errors.push("Пароль должен быть не менее 8 символов");
        }

        // Проверка на латинские буквы
        if (!/^[A-Za-z0-9!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]+$/.test(password)) {
            errors.push("Пароль должен содержать только латинские буквы");
        }

        // Проверка на наличие заглавных букв
        if (!/[A-Z]/.test(password)) {
            errors.push("Пароль должен содержать заглавные буквы");
        }

        // Проверка на наличие специальных символов
        if (!/[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(password)) {
            errors.push("Пароль должен содержать специальные символы");
        }

        return errors;
        }

        // Username validation function
        function validateUsername(username) {
        if (username.length < 5 || username.length > 41) {
            return "Имя пользователя должно быть от 5 до 40 символов";
        }
        return "";
        }

        // Password toggle visibility
        document.querySelectorAll('.password-toggle').forEach(toggle => {
        toggle.addEventListener('click', function() {
            const input = this.previousElementSibling;
            const type = input.getAttribute('type') === 'password' ? 'text' : 'password';
            input.setAttribute('type', type);
            this.textContent = type === 'password' ? 'visibility_off' : 'visibility';
        });
        });

        // Form submission validation
        document.getElementById('registrationForm').addEventListener('submit', function(event) {
        const passwordInput = document.getElementById('r_password');
        const confirmPasswordInput = document.getElementById('r_confirm_password');
        const nameInput = document.getElementById('r_fullname');
        const passwordError = document.getElementById('passwordError');
        const nameError = document.getElementById('nameError');

        const passwordValidationErrors = validatePassword(passwordInput.value);
        const nameValidationError = validateUsername(nameInput.value);

        if (passwordInput.value !== confirmPasswordInput.value) {
            passwordError.innerHTML = "Пароли не совпадают";
            event.preventDefault();
        } else if (passwordValidationErrors.length > 0) {
            passwordError.innerHTML = passwordValidationErrors.join('<br>');
            event.preventDefault();
        } else {
            passwordError.innerHTML = '';
        }

        if (nameValidationError) {
            nameError.innerHTML = nameValidationError;
            event.preventDefault();
        } else {
            nameError.innerHTML = '';
        }
        });
});