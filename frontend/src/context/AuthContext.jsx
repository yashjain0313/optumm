import { createContext, useContext, useState } from "react";
import { Navigate } from "react-router-dom";

// 1. Create the context
const AuthContext = createContext(null);

// 2. Provider — wraps the whole app
export function AuthProvider({ children }) {
  const [token, setToken] = useState(() => localStorage.getItem("token") || null);
  const [employee, setEmployee] = useState(() => {
    const saved = localStorage.getItem("employee");
    return saved ? JSON.parse(saved) : null;
  });

  // Call this after a successful /api/auth/login response
  function login(data) {
    localStorage.setItem("token", data.access_token);
    localStorage.setItem("employee", JSON.stringify({ name: data.name, employee_id: data.employee_id }));
    setToken(data.access_token);
    setEmployee({ name: data.name, employee_id: data.employee_id });
  }

  // Call this to sign out
  function logout() {
    localStorage.removeItem("token");
    localStorage.removeItem("employee");
    setToken(null);
    setEmployee(null);
  }

  return (
    <AuthContext.Provider value={{ token, employee, isAuthenticated: !!token, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

// 3. Hook — use this in any component: const { employee, logout } = useAuth()
export function useAuth() {
  return useContext(AuthContext);
}

// 4. Guard — wraps protected routes
export function ProtectedRoute({ children }) {
  const { isAuthenticated } = useAuth();
  if (!isAuthenticated) return <Navigate to="/login" replace />;
  return children;
}
