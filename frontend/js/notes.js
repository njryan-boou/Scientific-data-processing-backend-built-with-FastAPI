const API_BASE_URL = "http://127.0.0.1:8001";

window.onload = initializeNotesPage;

async function initializeNotesPage() {
    await loadCurrentUser();
    await loadNotes();
}

async function apiFetch(path, options = {}) {
    const token = localStorage.getItem("token");

    if (!token) {
        window.location.href = "login.html";
        return null;
    }

    const response = await fetch(
        `${API_BASE_URL}${path}`,
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

async function loadCurrentUser() {
    const response = await apiFetch("/auth/me");

    if (!response || !response.ok) {
        return;
    }

    const user = await response.json();
    const adminLink = document.getElementById("admin-link");

    if (adminLink && user.is_admin) {
        adminLink.classList.remove("hidden");
    }
}

async function loadNotes() {
    const container = document.getElementById("notes");
    container.innerHTML = "Loading notes...";

    try {
        const response = await apiFetch("/notes/");

        if (!response) {
            return;
        }

        if (!response.ok) {
            container.innerHTML = "Could not load notes.";
            return;
        }

        const notes = await response.json();
        container.innerHTML = "";

        if (notes.length === 0) {
            container.innerHTML = "<p>No notes yet.</p>";
            return;
        }

        notes.forEach(note => {
            const noteElement = document.createElement("div");
            noteElement.className = "note";

            const title = document.createElement("h3");
            title.textContent = note.title;

            const content = document.createElement("p");
            content.textContent = note.content;

            const deleteButton = document.createElement("button");
            deleteButton.className = "delete-btn";
            deleteButton.textContent = "Delete";
            deleteButton.onclick = () => deleteNote(note.id);

            noteElement.append(title, content, deleteButton);
            container.appendChild(noteElement);
        });
    } catch {
        container.innerHTML = "Could not connect to the API.";
    }
}

async function createNote() {
    const titleInput = document.getElementById("title");
    const contentInput = document.getElementById("content");
    const title = titleInput.value.trim();
    const content = contentInput.value.trim();

    if (!title || !content) {
        return;
    }

    const response = await apiFetch(
        "/notes/",
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                title,
                content
            })
        }
    );

    if (!response || !response.ok) {
        return;
    }

    titleInput.value = "";
    contentInput.value = "";
    loadNotes();
}

async function deleteNote(id) {
    const response = await apiFetch(
        `/notes/${id}`,
        {
            method: "DELETE"
        }
    );

    if (!response || !response.ok) {
        return;
    }

    loadNotes();
}

function logout() {
    localStorage.removeItem("token");
    window.location.href = "login.html";
}
