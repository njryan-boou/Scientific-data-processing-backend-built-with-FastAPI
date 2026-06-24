function getApiErrorMessage(data, fallback = "The request failed. Please try again.") {
    const detail = getApiErrorDetail(data);

    if (typeof detail === "string" && detail.trim()) {
        return cleanErrorMessage(detail);
    }

    if (Array.isArray(detail) && detail.length > 0) {
        return "Fix the input and try again.";
    }

    return fallback;
}

function getApiErrorItems(data) {
    const detail = getApiErrorDetail(data);

    if (Array.isArray(detail)) {
        return detail.map(formatValidationError).filter(Boolean);
    }

    if (typeof detail === "string" && detail.trim()) {
        return [cleanErrorMessage(detail)];
    }

    return [];
}

function getApiErrorDetail(data) {
    if (data && typeof data === "object" && !Array.isArray(data) && "detail" in data) {
        return data.detail;
    }

    return data;
}

function formatValidationError(error) {
    if (!error || typeof error !== "object") {
        return cleanErrorMessage(String(error));
    }

    const field = formatErrorLocation(error.loc);
    const message = cleanErrorMessage(error.msg || "Invalid value.");

    return field ? `${field}: ${message}` : message;
}

function formatErrorLocation(location) {
    if (!Array.isArray(location)) {
        return "";
    }

    return location
        .filter(part => part !== "body")
        .map(part => String(part).replace(/_/g, " "))
        .join(" > ");
}

function cleanErrorMessage(message) {
    return message
        .replace(/^value error,\s*/i, "")
        .replace(/^input should be\s+/i, "Must be ")
        .replace(/\.$/, "")
        .trim()
        .replace(/^./, letter => letter.toUpperCase());
}
