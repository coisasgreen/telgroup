document.getElementById('loginBtn').addEventListener('click', function() {
    const password = document.getElementById('password').value;
    const notification = document.getElementById('notification');

    // Define the passwords and their corresponding messages
    const validPassword = "VIPCG-8092"; // Change this to the actual correct password
    const passwords = {
        "VIPCG-7352": "Tempo limite do código, contacte o seu administrador para ativar um novo código",
        "VIPCG-5931": "Seja bem-vindo ao Certeiros Green Privado, o group do Telegram será enviado para o seu e-mail dentro de alguns minutos",
        "VIPCG-4473": "CÓDIGO INCORRETO, Contacte o administrador para obter um código de ativação"
    };

    // Clear previous notification
    notification.textContent = '';

    if (password === validPassword) {
        notification.textContent = "Access Granted!";
        notification.style.color = "green";
    } else if (passwords[password]) {
        notification.textContent = passwords[password];
        notification.style.color = "red";
    } else {
        notification.textContent = "Wrong Password!";
        notification.style.color = "red";
    }
});
