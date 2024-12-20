// Handles login functionality and event listeners
document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');

    loginForm.addEventListener('submit', function (event) {
        event.preventDefault();

        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;

        fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`
        })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    alert(data.message);
                } else {
                    alert(data.message);
                }
            })
            .catch(error => {
                alert('Error: ' + error.message);
            });
    });

    // Forgot Password functionality
    document.querySelector('a').addEventListener('click', function (event) {
        event.preventDefault();
        alert('Forgot Password functionality not implemented yet.');
    });
});
