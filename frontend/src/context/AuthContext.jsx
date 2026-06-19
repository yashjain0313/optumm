import { createContext, useContext, useState } from "react";
import { Navigate } from "react-router-dom";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [employee, setEmployee] = useState(() => {
    const stored = localStorage.getItem("employee");
    return stored ? JSON.parse(stored) : null;
  });

  const isAuthenticated = !!localStorage.getItem("token");

  function login(data) {
    localStorage.setItem("token", data.access_token);
    const emp = { employee_id: data.employee_id, name: data.name };
    localStorage.setItem("employee", JSON.stringify(emp));
    setEmployee(emp);
  }

  function logout() {
    localStorage.removeItem("token");
    localStorage.removeItem("employee");
    setEmployee(null);
  }

  return (
    <AuthContext.Provider value={{ employee, isAuthenticated, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}

export function ProtectedRoute({ children }) {
  const { isAuthenticated } = useAuth();
  if (!isAuthenticated) return <Navigate to="/login" replace />;
  return children;
}
