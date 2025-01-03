document.addEventListener('DOMContentLoaded', function() { ///
    // Инициализация мини-приложения
    const telegram = window.Telegram.WebApp;

    if (telegram) {
        telegram.ready(); // Сообщаем Telegram, что WebApp готово
        console.log("Telegram WebApp инициализирован!");

        const initData = telegram.initDataUnsafe; // Получаем данные о пользователе

        // Отображаем имя пользователя на странице, если оно доступно
        const userName = initData.user?.first_name || "пользователь";
        const userId = initData.user?.id || "неизвестный ID";

    
    function validatePassword(password) {

        const errors = [];

        if (password.length < 8) {
            errors.push("Пароль должен быть не менее 8 символов");
        }

        if (!/^[A-Za-z0-9!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]+$/.test(password)) {
            errors.push("Пароль должен содержать только латинские буквы");
        }

        if (!/[A-Z]/.test(password)) {
            errors.push("Пароль должен содержать заглавные буквы");
        }

        if (!/[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(password)) {
            errors.push("Пароль должен содержать специальные символы");
        }

        return errors;
    }

    document.querySelectorAll('.password-toggle').forEach(toggle => {
        toggle.addEventListener('click', function() {
            const input = this.previousElementSibling;
            const type = input.getAttribute('type') === 'password' ? 'text' : 'password';
            input.setAttribute('type', type);
            this.textContent = type === 'password' ? 'visibility_off' : 'visibility';
        });
    });

    document.getElementById('loginForm').addEventListener('submit', function(event) {
        event.preventDefault(); // Всегда preventDefault, чтобы форма не отправлялась стандартным способом
    
        const emailInput = document.getElementById('a_email');
        const passwordInput = document.getElementById('a_password');
        const passwordError = document.getElementById('passwordError');
        
        // Валидация...
        const passwordValidationErrors = validatePassword(passwordInput.value);
        
        if (passwordValidationErrors.length > 0) {
            passwordError.innerHTML = passwordValidationErrors.join('<br>');
            return;
        }
    
        // Очистка ошибок
        passwordError.innerHTML = ''; 
        
        // Подготовка данных
        const formData = {
            user_id: window.Telegram.WebApp.initDataUnsafe.user?.id || "неизвестный ID",
            username: window.Telegram.WebApp.initDataUnsafe.user?.username || "undefined",
            email: emailInput.value,
            password: passwordInput.value,
            initData: window.Telegram.WebApp.initData || null
        };
    
        // Отправка запроса
        fetch("/authorization", {
            method: "POST",
            headers: { 
                "Content-Type": "application/json"
            },
            body: JSON.stringify(formData)
        })
        .then(response => {
            // Если ответ не OK - обработать ошибку
            if (!response.ok) {
                return response.json().then(errorData => {
                    throw new Error(errorData.message || 'Ошибка авторизации');
                });
            }
            // Если редирект - перейти по адресу
            return response.text(); // Используем text(), так как это HTML-страница
        })
        .then(responseText => {
            // Принудительная загрузка полученной страницы
            document.open();
            document.write(responseText);
            document.close();
        })
        .catch(error => {
            console.error("Ошибка:", error);
            passwordError.innerHTML = error.message;
        });
    });
}});