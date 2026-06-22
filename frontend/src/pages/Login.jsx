import { useState } from "react";
import { useNavigate, Navigate } from "react-router-dom";
import { api } from "../api";
import "./Login.css";

export default function Login() {
  const [employeeId, setEmployeeId] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  // If already logged in, go to dashboard
  if (localStorage.getItem("token")) {
    return <Navigate to="/" replace />;
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const data = await api.login(employeeId.trim().toUpperCase(), password);
      
      // Save token directly
      localStorage.setItem("token", data.access_token);
      const emp = { employee_id: data.employee_id, name: data.name };
      localStorage.setItem("employee", JSON.stringify(emp));

      navigate("/");
    } catch (err) {
      setError(err.message || "Login failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="login-page">
      <div className="login-box">
        <div className="login-header">
          <h1>Optum Benefits</h1>
          <p>Employee sign in</p>
        </div>

        <form onSubmit={handleSubmit} className="login-form">
          <div className="field">
            <label htmlFor="employeeId">Employee ID</label>
            <input
              id="employeeId"
              type="text"
              placeholder="EMP-1001"
              value={employeeId}
              onChange={(e) => setEmployeeId(e.target.value)}
              required
              autoComplete="username"
            />
          </div>

          <div className="field">
            <label htmlFor="password">Password</label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              autoComplete="current-password"
            />
          </div>

          {error && <p className="login-error">{error}</p>}

          <button type="submit" className="login-btn" disabled={loading}>
            {loading ? "Signing in…" : "Sign in"}
          </button>
        </form>

        <div className="login-help">
          <p className="help-title">Test accounts</p>
          <table>
            <tbody>
              <tr><td>EMP-1001</td><td>Alex Morgan</td></tr>
              <tr><td>EMP-1002</td><td>Jordan Lee</td></tr>
              <tr><td>EMP-1003</td><td>Sam Rivera (55+ catch-up)</td></tr>
            </tbody>
          </table>
          <p className="help-note">Password for all: <code>Optum@2026</code></p>
        </div>
      </div>
    </div>
  );
}
