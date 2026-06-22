import { NavLink, useNavigate } from "react-router-dom";
import "./Layout.css";

export default function Layout({ children }) {
  const navigate = useNavigate();
  const employeeStr = localStorage.getItem("employee");
  const employee = employeeStr ? JSON.parse(employeeStr) : null;

  function handleLogout() {
    localStorage.removeItem("token");
    localStorage.removeItem("employee");
    navigate("/login");
  }

  return (
    <div className="layout">
      <header className="topbar">
        <div className="topbar-left">
          <span className="topbar-brand">Optum</span>
          <span className="topbar-divider">|</span>
          <span className="topbar-title">Benefits Wallet</span>
        </div>
        <div className="topbar-right">
          <span className="topbar-user">{employee?.name}</span>
          <span className="topbar-id">{employee?.employee_id}</span>
          <button type="button" className="topbar-logout" onClick={handleLogout}>
            Sign out
          </button>
        </div>
      </header>

      <div className="layout-body">
        <nav className="sidebar">
          <NavLink to="/" end className={({ isActive }) => (isActive ? "nav-item active" : "nav-item")}>
            Overview
          </NavLink>
          <NavLink to="/transactions" className={({ isActive }) => (isActive ? "nav-item active" : "nav-item")}>
            Transactions
          </NavLink>
          <NavLink to="/rules" className={({ isActive }) => (isActive ? "nav-item active" : "nav-item")}>
            Plan Rules
          </NavLink>
        </nav>

        <main className="content">
          {children}
        </main>
      </div>
    </div>
  );
}
