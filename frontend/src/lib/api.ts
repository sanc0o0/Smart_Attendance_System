const API_BASE = "http://127.0.0.1:8000";

export async function getSessionStatus() {
    const res = await fetch(`${API_BASE}/session/status`, {
        cache: "no-store",
    });
    if (!res.ok) throw new Error("Failed to fetch session status");
    return res.json();
}

export async function getTodayAnalytics() {
    const res = await fetch(`${API_BASE}/analytics/today`, {
        cache: "no-store",
    });
    if (!res.ok) throw new Error("Failed to fetch today analytics");
    return res.json();
}

export async function getStudentAnalytics() {
    const res = await fetch(`${API_BASE}/analytics/students`, {
        cache: "no-store",
    });
    if (!res.ok) throw new Error("Failed to fetch student analytics");
    return res.json();
}

export async function openSession(session: "morning" | "afternoon") {
    const res = await fetch(
        `${API_BASE}/session/open?session=${session}`,
        { method: "POST" }
    );

    const data = await res.json();

    if (!res.ok) {
        throw new Error(data.detail || "Cannot open session");
    }
    return data;
}

export async function closeSession(session: "morning" | "afternoon" ) {
    const res = await fetch(
        `${API_BASE}/session/close?session=${session}`,
        { method: "POST" }
    );
    if (!res.ok) throw new Error("Failed to close session");
    return res.json();
}
