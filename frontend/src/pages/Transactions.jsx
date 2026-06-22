import { Navigate } from "react-router-dom";
import { useEffect, useState } from "react";
import { api } from "../api";
import Layout from "../components/Layout";
import "./Transactions.css";

function fmt(n) {
  return new Intl.NumberFormat("en-US", { style: "currency", currency: "USD" }).format(Math.abs(n));
}

export default function Transactions() {
  const isAuthenticated = !!localStorage.getItem("token");
  const [rows, setRows] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.getTransactions().then(setRows).finally(() => setLoading(false));
  }, []);

  if (!isAuthenticated) return <Navigate to="/login" replace />;
  if (loading) return <Layout><p className="page-loading">Loading transactions…</p></Layout>;

  return (
    <Layout>
      <div className="transactions-page">
        <div className="page-head">
          <h2>Transaction history</h2>
          <p>Claims, contributions, and wallet activity</p>
        </div>

        <div className="table-wrap">
          <table className="data-table">
            <thead>
              <tr>
                <th>Date</th>
                <th>ID</th>
                <th>Description</th>
                <th>Category</th>
                <th>Source</th>
                <th>Amount</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {rows.map((t) => (
                <tr key={t.id}>
                  <td>{t.date}</td>
                  <td className="mono">{t.id}</td>
                  <td>{t.description}</td>
                  <td>{t.category}</td>
                  <td>{t.source}</td>
                  <td className={t.amount < 0 ? "debit" : "credit"}>
                    {t.amount < 0 ? "−" : "+"}{fmt(t.amount)}
                  </td>
                  <td><span className={`badge badge-${t.status.toLowerCase()}`}>{t.status}</span></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </Layout>
  );
}
