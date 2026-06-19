const API_BASE = import.meta.env.VITE_API_URL || "/api";

function getToken() {
  return localStorage.getItem("token");
}

async function request(path, options = {}) {
  const headers = { "Content-Type": "application/json", ...options.headers };
  const token = getToken();
  if (token) headers.Authorization = `Bearer ${token}`;

  const res = await fetch(`${API_BASE}${path}`, { ...options, headers });

  if (res.status === 401) {
    localStorage.removeItem("token");
    localStorage.removeItem("employee");
    window.location.href = "/login";
    throw new Error("Session expired");
  }

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    const msg = typeof err.detail === "string" ? err.detail : "Request failed";
    throw new Error(msg);
  }
  return res.json();
}

export const api = {
  login: (employee_id, password) =>
    request("/auth/login", {
      method: "POST",
      body: JSON.stringify({ employee_id, password }),
    }),
  getMember: () => request("/member"),
  getWallet: () => request("/wallet"),
  getBenefits: () => request("/benefits"),
  getTransactions: () => request("/transactions"),
  getRules: () => request("/rules"),
  payCopay: (body) =>
    request("/wallet/pay-copay", { method: "POST", body: JSON.stringify(body) }),
};
