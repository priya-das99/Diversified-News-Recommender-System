document.addEventListener('DOMContentLoaded', function() {
    // Example: Add interactivity to the news items
    // const newsItems = document.querySelectorAll('.news-item');
    // newsItems.forEach(item => {
    //     item.addEventListener('click', function() {
    //         alert('News item clicked!');
    //     });
    // });

    // Example: Handle form submission dynamically
    const loginForm = document.querySelector('form');
    if (loginForm) {
        loginForm.addEventListener('submit', function(event) {
            event.preventDefault();
            const user_id = document.querySelector('#user_id').value;
            const password = document.querySelector('#password').value;
            // Perform AJAX request to submit the form
            fetch('/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ user_id, password })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    window.location.href = '/';
                } else {
                    alert('Invalid credentials');
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    }

    // Dark Mode Toggle Script
    const themeToggleBtn = document.getElementById('theme-toggle');
    const darkIcon = document.getElementById('theme-toggle-dark-icon');
    const lightIcon = document.getElementById('theme-toggle-light-icon');

    if (themeToggleBtn) { // Ensure the toggle button exists on the page
        // Initialize theme based on localStorage or system preference
        if (localStorage.getItem('color-theme') === 'dark' || 
            (!('color-theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
            document.documentElement.classList.add('dark');
            darkIcon.classList.remove('hidden');
        } else {
            lightIcon.classList.remove('hidden');
        }

        // Toggle theme on button click
        themeToggleBtn.addEventListener('click', () => {
            darkIcon.classList.toggle('hidden');
            lightIcon.classList.toggle('hidden');

            if (document.documentElement.classList.contains('dark')) {
                document.documentElement.classList.remove('dark');
                localStorage.setItem('color-theme', 'light');
            } else {
                document.documentElement.classList.add('dark');
                localStorage.setItem('color-theme', 'dark');
            }
        });
    }
});
