const API_URL = "https://scientific-api-1ufm.onrender.com";

const operations = [
    {
        id: "euler",
        label: "Euler Method",
        path: "/ode/euler"
    },
    {
        id: "runge-kutta-4",
        label: "Runge-Kutta 4",
        path: "/ode/runge-kutta-4"
    }
];

window.onload = () => {
    renderOperations();
    selectOperation("euler");
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

function readNumber(id, label) {
    const value = Number(document.getElementById(id).value);

    if (!Number.isFinite(value)) {
        throw new Error(`${label} must be a number.`);
    }

    return value;
}

function buildPayload() {
    const steps = Number(document.getElementById("steps").value);
    const stepSize = readNumber("step-size", "Step size");

    if (!Number.isInteger(steps) || steps <= 0) {
        throw new Error("Steps must be a positive integer.");
    }

    if (stepSize <= 0) {
        throw new Error("Step size must be positive.");
    }

    return {
        y0: readNumber("y0", "Initial value y0"),
        t0: readNumber("t0", "Initial time t0"),
        step_size: stepSize,
        steps
    };
}

async function runOperation() {
    const operation = getOperation();
    const output = document.getElementById("result");

    setStatus("");
    setResultMessage(output, "Running...");

    let payload;

    try {
        payload = buildPayload();
    } catch (error) {
        setStatus(error.message, true);
        setResultMessage(output, "Fix the input and try again.");
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
            setStatus(getApiErrorMessage(data, "Could not run this solver."), true);
            renderApiError(output, data);
            return;
        }

        setStatus("Solver completed.", false);
        renderApiResult(output, data);
    } catch {
        setStatus("Could not connect to the API.", true);
        setResultMessage(output, "Start FastAPI on http://127.0.0.1:8001 and try again.");
    }
}

function setStatus(message, isError = false) {
    const status = document.getElementById("status");
    status.textContent = message;
    status.className = isError ? "status-error" : "status-ok";
}

function loadExample() {
    document.getElementById("y0").value = "1";
    document.getElementById("t0").value = "0";
    document.getElementById("step-size").value = "0.5";
    document.getElementById("steps").value = "5";
    setResultMessage(document.getElementById("result"), "Choose a method and run it.");
    setStatus("");
}

function clearForm() {
    document.getElementById("y0").value = "";
    document.getElementById("t0").value = "";
    document.getElementById("step-size").value = "";
    document.getElementById("steps").value = "";
    setResultMessage(document.getElementById("result"), "");
    setStatus("");
}
