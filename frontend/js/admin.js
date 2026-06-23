const API_URL = "https://scientific-api-1ufm.onrender.com";

window.onload = loadUsers;

async function apiFetch(path, options = {}) {
    const token = localStorage.getItem("token");

    if (!token) {
        window.location.href = "login.html";
        return null;
    }

    const response = await fetch(
        `${API_URL}${path}`,
        {
            ...options,
            headers: {
                ...(options.headers || {}),
                Authorization: `Bearer ${token}`
            }
        }
    );

    if (response.status === 401) {
        localStorage.removeItem("token");
        window.location.href = "login.html";
        return null;
    }

    return response;
}

function setMessage(text) {
    document.getElementById("message").textContent = text;
}

async function loadUsers() {
    const table = document.getElementById("users");
    table.innerHTML = "<tr><td colspan=\"6\">Loading users...</td></tr>";

    try {
        const response = await apiFetch("/admin/users");

        if (!response) {
            return;
        }

        if (response.status === 403) {
            setMessage("Admin access required.");
            table.innerHTML = "";
            return;
        }

        if (!response.ok) {
            setMessage("Could not load users.");
            table.innerHTML = "";
            return;
        }

        const users = await response.json();
        table.innerHTML = "";

        users.forEach(user => {
            table.appendChild(renderUserRow(user));
        });
    } catch {
        setMessage("Could not connect to the API.");
        table.innerHTML = "";
    }
}

function renderUserRow(user) {
    const row = document.createElement("tr");

    row.innerHTML = `
        <td>${user.id}</td>
        <td>
            <input id="username-${user.id}" value="">
        </td>
        <td>
            <input id="email-${user.id}" value="">
        </td>
        <td class="center-cell">
            <input id="admin-${user.id}" type="checkbox">
        </td>
        <td>${user.note_count}</td>
        <td>
            <div class="button-row">
                <button onclick="saveUser(${user.id})">
                    Save
                </button>
                <button class="danger" onclick="deleteUser(${user.id})">
                    Delete
                </button>
            </div>
        </td>
    `;

    row.querySelector(`#username-${user.id}`).value = user.username;
    row.querySelector(`#email-${user.id}`).value = user.email;
    row.querySelector(`#admin-${user.id}`).checked = user.is_admin;

    return row;
}

async function saveUser(id) {
    setMessage("");

    const username = document.getElementById(`username-${id}`).value.trim();
    const email = document.getElementById(`email-${id}`).value.trim();
    const isAdmin = document.getElementById(`admin-${id}`).checked;

    const response = await apiFetch(
        `/admin/users/${id}`,
        {
            method: "PUT",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                username,
                email,
                is_admin: isAdmin
            })
        }
    );

    if (!response) {
        return;
    }

    if (!response.ok) {
        const error = await response.json().catch(() => null);
        setMessage(error?.detail || "Could not save user.");
        return;
    }

    setMessage("User saved.");
    loadUsers();
}

async function deleteUser(id) {
    setMessage("");

    const response = await apiFetch(
        `/admin/users/${id}`,
        {
            method: "DELETE"
        }
    );

    if (!response) {
        return;
    }

    if (!response.ok) {
        const error = await response.json().catch(() => null);
        setMessage(error?.detail || "Could not delete user.");
        return;
    }

    setMessage("User deleted.");
    loadUsers();
}

function logout() {
    localStorage.removeItem("token");
    window.location.href = "login.html";
}
