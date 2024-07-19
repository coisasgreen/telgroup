document.getElementById('loginForm').addEventListener('submit', function(event) {
  event.preventDefault(); // Prevent form submission for now

  const password = document.getElementById('password').value;
  const notification = document.getElementById('notification');

  // Define the correct password
  const validPassword = "VIPCG-8092"; // Replace with your actual correct password

  // Define messages for different passwords (optional)
  const passwordMessages = {
    "VIPCG-8092": "Access Granted! Redirecionando...",
    "VIPCG-7352": "Tempo limite do código, contacte o seu administrador para ativar um novo código",
    "VIPCG-5931": "Seja bem-vindo ao Certeiros Green Privado, o group do Telegram será enviado para o seu e-mail dentro de alguns minutos",
    "VIPCG-4473": "CÓDIGO INCORRETO, Contacte o administrador para obter um código de ativação"
  };

  // Clear previous notification
  notification.textContent = '';

  if (password === validPassword) {
    notification.textContent = passwordMessages[validPassword];
    notification.style.color = "green";
    // Here you can redirect to the next page or perform any other action
    setTimeout(function() {
      window.location.href = "next.html"; // Replace with your actual next page URL
    }, 1000); // Redirect after 3 seconds (3000 milliseconds)
  } else if (passwordMessages[password]) {
    notification.textContent = passwordMessages[password];
    notification.style.color = "orange"; // Adjust color for other messages
  } else {
    notification.textContent = "Senha incorreta, tente novamente!";
    notification.style.color = "red";
  }
});
