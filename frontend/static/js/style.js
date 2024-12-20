// Handles the UI rendering and styling
function renderUI() {
    const root = document.getElementById("root");

    root.innerHTML = `
        <div class="flex flex-col items-center justify-center min-h-screen bg-gradient-to-r from-purple-500 to-pink-500">
            <h1 class="text-white text-5xl font-bold mb-4 shadow-lg" id="title">TaaZaa Khabar</h1>
            <h2 class="text-white text-3xl mb-2 shadow-md">Log In to Your Account</h2>
            <form id="loginForm" class="w-full max-w-sm">
                <div class="bg-white p-4 rounded-lg shadow-lg mb-4 transition-transform transform hover:scale-105">
                    <label for="username" class="block text-sm font-medium text-zinc-700">Username</label>
                    <input type="text" id="username" name="username" class="mt-1 block w-full px-3 py-2 border border-zinc-300 rounded-md shadow-sm focus:outline-none focus:ring focus:ring-blue-500 focus:border-blue-500 sm:text-sm" placeholder="Enter your username" required>
                </div>
                <div class="bg-white p-4 rounded-lg shadow-lg mb-4 transition-transform transform hover:scale-105">
                    <label for="password" class="block text-sm font-medium text-zinc-700">Password</label>
                    <input type="password" id="password" name="password" class="mt-1 block w-full px-3 py-2 border border-zinc-300 rounded-md shadow-sm focus:outline-none focus:ring focus:ring-blue-500 focus:border-blue-500 sm:text-sm" placeholder="Enter your password" required>
                </div>
                <button type="submit" class="bg-blue-600 text-white px-4 py-2 rounded-lg shadow-lg hover:bg-blue-500 transition w-full">Log In</button>
            </form>
            <a href="#" class="mt-6 text-white underline hover:text-blue-300">Forgot Password?</a>
        </div>
    `;

    // Animation for the title
    const title = document.getElementById('title');
    const titleText = title.innerText;
    title.innerText = '';
    title.style.whiteSpace = 'nowrap';
    for (let i = 0; i < titleText.length; i++) {
        setTimeout(() => {
            title.innerText += titleText[i];
        }, i * 200);
    }
}

renderUI();
