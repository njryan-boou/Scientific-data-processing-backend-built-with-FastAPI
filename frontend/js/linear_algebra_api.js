const API_URL = "https://scientific-api-1ufm.onrender.com";

const operations = [
    {
        id: "determinant",
        label: "Determinant",
        path: "/linalg/determinant",
        kind: "single"
    },
    {
        id: "inverse",
        label: "Inverse",
        path: "/linalg/inverse",
        kind: "single"
    },
    {
        id: "transpose",
        label: "Transpose",
        path: "/linalg/transpose",
        kind: "single"
    },
    {
        id: "trace",
        label: "Trace",
        path: "/linalg/trace",
        kind: "single"
    },
    {
        id: "eigenvalues",
        label: "Eigenvalues",
        path: "/linalg/eigenvalues",
        kind: "single"
    },
    {
        id: "eigenvectors",
        label: "Eigenvectors",
        path: "/linalg/eigenvectors",
        kind: "single"
    },
    {
        id: "matrix-addition",
        label: "Add Matrices",
        path: "/linalg/matrix-addition",
        kind: "double"
    },
    {
        id: "matrix-subtraction",
        label: "Subtract Matrices",
        path: "/linalg/matrix-subtraction",
        kind: "double"
    },
    {
        id: "matrix-multiplication",
        label: "Multiply Matrices",
        path: "/linalg/matrix-multiplication",
        kind: "double"
    },
    {
        id: "scalar-multiply",
        label: "Scalar Multiply",
        path: "/linalg/scalar-multiply",
        kind: "scalar"
    },
    {
        id: "scalar-divide",
        label: "Scalar Divide",
        path: "/linalg/scalar-divide",
        kind: "scalar"
    },
    {
        id: "lu-decomposition",
        label: "LU Decomposition",
        path: "/linalg/lu-decomposition",
        kind: "single"
    },
    {
        id: "qr-decomposition",
        label: "QR Decomposition",
        path: "/linalg/qr-decomposition",
        kind: "single"
    },
    {
        id: "svd-decomposition",
        label: "SVD Decomposition",
        path: "/linalg/svd-decomposition",
        kind: "single"
    }
];

window.onload = () => {
    renderOperations();
    selectOperation("determinant");
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

function getOperation() {
    const selected = document.querySelector("input[name='operation']:checked");
    return operations.find(operation => operation.id === selected.value);
}

function selectOperation(id) {
    const input = document.querySelector(`input[value="${id}"]`);
    const operation = operations.find(item => item.id === id);

    input.checked = true;
    document.getElementById("matrix-b-wrap").style.display =
        operation.kind === "double" ? "block" : "none";
    document.getElementById("scalar-wrap").style.display =
        operation.kind === "scalar" ? "grid" : "none";
    setStatus("");
}

function parseMatrix(id) {
    let value;

    try {
        value = JSON.parse(document.getElementById(id).value);
    } catch {
        throw new Error(`${id === "matrix-a" ? "Matrix A" : "Matrix B"} must be valid JSON.`);
    }

    if (!Array.isArray(value) || value.length === 0) {
        throw new Error("Matrix must be a non-empty array of rows.");
    }

    if (!value.every(row => Array.isArray(row) && row.length > 0)) {
        throw new Error("Each matrix row must be a non-empty array.");
    }

    const width = value[0].length;

    if (!value.every(row => row.length === width)) {
        throw new Error("Matrix rows must all have the same length.");
    }

    return value;
}

function buildPayload(operation) {
    const matrixA = parseMatrix("matrix-a");

    if (operation.kind === "double") {
        return {
            matrix_a: matrixA,
            matrix_b: parseMatrix("matrix-b")
        };
    }

    if (operation.kind === "scalar") {
        const scalar = Number(document.getElementById("scalar").value);

        if (!Number.isFinite(scalar)) {
            throw new Error("Scalar must be a number.");
        }

        return {
            matrix: matrixA,
            scalar
        };
    }

    return {
        matrix: matrixA
    };
}

async function runOperation() {
    const operation = getOperation();
    const output = document.getElementById("result");

    setStatus("");
    setResultMessage(output, "Running...");

    let payload;

    try {
        payload = buildPayload(operation);
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
            setStatus(getApiErrorMessage(data, "Could not run this operation."), true);
            renderApiError(output, data);
            return;
        }

        setStatus("Operation completed.", false);
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
    document.getElementById("matrix-a").value = "[[1, 2], [3, 4]]";
    document.getElementById("matrix-b").value = "[[5, 6], [7, 8]]";
    document.getElementById("scalar").value = "2";
    setResultMessage(document.getElementById("result"), "Choose an operation and run it.");
    setStatus("");
}

function clearForm() {
    document.getElementById("matrix-a").value = "";
    document.getElementById("matrix-b").value = "";
    document.getElementById("scalar").value = "";
    setResultMessage(document.getElementById("result"), "");
    setStatus("");
}
