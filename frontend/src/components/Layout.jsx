import { NavLink, Outlet, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import "./Layout.css";

export default function Layout() {
  const { employee, logout } = useAuth();
  const navigate = useNavigate();

  function handleLogout() {
    logout();
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
          <Outlet />
        </main>
      </div>
    </div>
  );
}
