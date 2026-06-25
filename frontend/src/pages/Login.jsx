import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../api";
import { useAuth } from "../context/AuthContext";
import "./Login.css";

export default function Login() {
  const [employeeId, setEmployeeId] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const data = await api.login(employeeId.trim().toUpperCase(), password);
      login(data);
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
          <p className="help-title">Test accounts (password: <code>1234HCLTECH</code>)</p>
          <table>
            <tbody>
              <tr><td>52381866</td><td>Ayush Parashar</td><td>E0</td></tr>
              <tr><td>52381856</td><td>Satyam Sangal</td><td>E1</td></tr>
              <tr><td>52381857</td><td>Yash Jain</td><td>E2</td></tr>
              <tr><td>52381854</td><td>Vandit Mittal</td><td>E3</td></tr>
              <tr><td>52382046</td><td>Shreeya Agarwal</td><td>E4</td></tr>
              <tr><td>52381898</td><td>Mansi Prajapati</td><td>E5</td></tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
