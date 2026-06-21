const API_BASE_URL = "http://127.0.0.1:8001";

async function login() {
    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value;
    const message = document.getElementById("message");

    message.textContent = "";

    if (!username || !password) {
        message.textContent = "Enter your username and password.";
        return;
    }

    try {
        const response = await fetch(
            `${API_BASE_URL}/auth/login`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    username,
                    password
                })
            }
        );

        if (!response.ok) {
            const error = await response.json().catch(() => null);
            message.textContent = error?.detail || "Login failed.";
            return;
        }

        const data = await response.json();
        localStorage.setItem("token", data.access_token);
        window.location.href = "notes.html";
    } catch {
        message.textContent = "Could not connect to the API.";
    }
}

async function register() {
    const username = document.getElementById("username").value.trim();
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;
    const message = document.getElementById("message");

    message.textContent = "";

    if (!username || !email || !password) {
        message.textContent = "Enter a username, email, and password.";
        return;
    }

    try {
        const response = await fetch(
            `${API_BASE_URL}/auth/register`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    username,
                    email,
                    password
                })
            }
        );

        if (!response.ok) {
            const error = await response.json().catch(() => null);
            message.textContent = error?.detail || "Registration failed.";
            return;
        }

        message.textContent = "Account created. You can log in now.";
    } catch {
        message.textContent = "Could not connect to the API.";
    }
}
