const API_URL = "https://scientific-api-1ufm.onrender.com";
const operations = [
    {
        id: "summary",
        label: "Summary",
        path: "/stats/summary"
    },
    {
        id: "mean",
        label: "Mean",
        path: "/stats/mean"
    },
    {
        id: "std",
        label: "Standard Deviation",
        path: "/stats/std"
    },
    {
        id: "variance",
        label: "Variance",
        path: "/stats/variance"
    },
    {
        id: "max",
        label: "Maximum",
        path: "/stats/max"
    },
    {
        id: "min",
        label: "Minimum",
        path: "/stats/min"
    }
];

window.onload = () => {
    renderOperations();
    selectOperation("summary");
};

function renderOperations() {
    const container = document.getElementById("operations");

    operations.forEach(operation => {
        const label = document.createElement("label");
        label.className = "operation-option";

        label.innerHTML = `
            <input
                type="radio"
                name="operation"
                value="${operation.id}"
                onchange="selectOperation('${operation.id}')"
            >
            <span>${operation.label}</span>
        `;

        container.appendChild(label);
    });
}

function selectOperation(id) {
    const input = document.querySelector(`input[value="${id}"]`);

    input.checked = true;
    setStatus("");
}

function getOperation() {
    const selected = document.querySelector("input[name='operation']:checked");
    return operations.find(operation => operation.id === selected.value);
}

function parseVector() {
    let value;

    try {
        value = JSON.parse(document.getElementById("vector").value);
    } catch {
        throw new Error("Vector must be valid JSON.");
    }

    if (!Array.isArray(value) || value.length === 0) {
        throw new Error("Vector must be a non-empty array.");
    }

    if (!value.every(item => typeof item === "number" && Number.isFinite(item))) {
        throw new Error("Vector values must all be numbers.");
    }

    return value;
}

async function runOperation() {
    const operation = getOperation();
    const output = document.getElementById("result");

    setStatus("");
    output.textContent = "Running...";

    let payload;

    try {
        payload = {
            vector: parseVector()
        };
    } catch (error) {
        setStatus(error.message, true);
        output.textContent = "Fix the input and try again.";
        return;
    }

    try {
        const response = await fetch(
            `${API_URL}${operation.path}`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(payload)
            }
        );

        const data = await response.json();

        if (!response.ok) {
            setStatus(formatApiError(data), true);
            output.textContent = JSON.stringify(data, null, 2);
            return;
        }

        setStatus("Operation completed.", false);
        output.textContent = JSON.stringify(data, null, 2);
    } catch {
        setStatus("Could not connect to the API.", true);
        output.textContent = "Start FastAPI on http://127.0.0.1:8001 and try again.";
    }
}

function formatApiError(data) {
    if (typeof data.detail === "string") {
        return data.detail;
    }

    return "The API rejected the request.";
}

function setStatus(message, isError = false) {
    const status = document.getElementById("status");
    status.textContent = message;
    status.className = isError ? "status-error" : "status-ok";
}

function loadExample() {
    document.getElementById("vector").value = "[1, 2, 3, 4, 5]";
    document.getElementById("result").textContent = "Choose an operation and run it.";
    setStatus("");
}

function clearForm() {
    document.getElementById("vector").value = "";
    document.getElementById("result").textContent = "";
    setStatus("");
}
