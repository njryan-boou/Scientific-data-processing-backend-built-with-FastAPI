function setResultMessage(output, message) {
    output.classList.remove("output-formatted", "output-error");
    output.textContent = message;
}

function renderApiResult(output, data) {
    output.replaceChildren();
    output.classList.add("output-formatted");
    output.classList.remove("output-error");

    if (isOdeResult(data)) {
        output.appendChild(renderOdeTable(data));
        return;
    }

    if (isPlainObject(data)) {
        const grid = document.createElement("div");
        grid.className = "result-grid";

        Object.entries(data).forEach(([key, value]) => {
            grid.appendChild(renderResultEntry(formatLabel(key), value));
        });

        output.appendChild(grid);
        return;
    }

    output.appendChild(renderValue(data));
}

function renderApiError(output, data) {
    output.replaceChildren();
    output.classList.add("output-formatted", "output-error");

    const detail = isPlainObject(data) ? data.detail : data;
    output.appendChild(renderErrorDetail(detail));
}

function renderResultEntry(label, value) {
    const section = document.createElement("section");
    section.className = "result-entry";

    const heading = document.createElement("h3");
    heading.textContent = label;
    section.appendChild(heading);
    section.appendChild(renderValue(value));

    return section;
}

function renderValue(value) {
    if (isMatrix(value)) {
        return renderMatrix(value);
    }

    if (Array.isArray(value)) {
        return renderVector(value);
    }

    if (isPlainObject(value)) {
        const list = document.createElement("dl");
        list.className = "result-list";

        Object.entries(value).forEach(([key, item]) => {
            const term = document.createElement("dt");
            term.textContent = formatLabel(key);

            const description = document.createElement("dd");
            description.appendChild(renderValue(item));

            list.append(term, description);
        });

        return list;
    }

    const metric = document.createElement("div");
    metric.className = "result-metric";
    metric.textContent = formatValue(value);
    return metric;
}

function renderMatrix(matrix) {
    const wrap = document.createElement("div");
    wrap.className = "result-table-wrap";

    const table = document.createElement("table");
    table.className = "result-matrix";

    matrix.forEach(row => {
        const tr = document.createElement("tr");

        row.forEach(value => {
            const td = document.createElement("td");
            td.textContent = formatValue(value);
            tr.appendChild(td);
        });

        table.appendChild(tr);
    });

    wrap.appendChild(table);
    return wrap;
}

function renderVector(vector) {
    const list = document.createElement("div");
    list.className = "result-vector";

    vector.forEach(value => {
        const item = document.createElement("span");
        item.className = "result-chip";
        item.textContent = formatValue(value);
        list.appendChild(item);
    });

    return list;
}

function renderOdeTable(data) {
    const wrap = document.createElement("div");
    wrap.className = "result-table-wrap";

    const table = document.createElement("table");
    table.className = "result-series";

    const header = document.createElement("tr");
    ["Step", "t", "y"].forEach(label => {
        const th = document.createElement("th");
        th.textContent = label;
        header.appendChild(th);
    });
    table.appendChild(header);

    data.t.forEach((time, index) => {
        const row = document.createElement("tr");
        [index, time, data.y[index]].forEach(value => {
            const cell = document.createElement("td");
            cell.textContent = formatValue(value);
            row.appendChild(cell);
        });
        table.appendChild(row);
    });

    wrap.appendChild(table);
    return wrap;
}

function renderErrorDetail(detail) {
    if (Array.isArray(detail)) {
        const list = document.createElement("ul");
        list.className = "result-error-list";

        detail.forEach(item => {
            const listItem = document.createElement("li");

            if (isPlainObject(item)) {
                const location = Array.isArray(item.loc) ? item.loc.join(" > ") : "";
                listItem.textContent = location
                    ? `${location}: ${item.msg || JSON.stringify(item)}`
                    : item.msg || JSON.stringify(item);
            } else {
                listItem.textContent = String(item);
            }

            list.appendChild(listItem);
        });

        return list;
    }

    const message = document.createElement("p");
    message.className = "result-error-message";
    message.textContent = typeof detail === "string"
        ? detail
        : JSON.stringify(detail, null, 2);
    return message;
}

function isOdeResult(data) {
    return isPlainObject(data)
        && Array.isArray(data.t)
        && Array.isArray(data.y)
        && data.t.length === data.y.length;
}

function isMatrix(value) {
    return Array.isArray(value)
        && value.length > 0
        && value.every(row => Array.isArray(row));
}

function isPlainObject(value) {
    return value !== null && typeof value === "object" && !Array.isArray(value);
}

function formatLabel(key) {
    const labels = {
        P: "Permutation Matrix",
        L: "Lower Matrix",
        U: "Upper Matrix",
        Q: "Orthogonal Matrix",
        R: "Upper Matrix",
        S: "Singular Values",
        Vt: "V Transpose",
        std: "Standard Deviation",
        t: "Time Points",
        y: "Solution Values"
    };

    return labels[key] || key
        .replace(/_/g, " ")
        .replace(/\b\w/g, letter => letter.toUpperCase());
}

function formatValue(value) {
    if (typeof value === "number") {
        return Number.isInteger(value) ? String(value) : value.toFixed(4);
    }

    if (isPlainObject(value) && "real" in value && "imag" in value) {
        const real = formatValue(value.real);
        const imag = formatValue(Math.abs(value.imag));
        const sign = value.imag < 0 ? "-" : "+";
        return `${real} ${sign} ${imag}i`;
    }

    return String(value);
}
