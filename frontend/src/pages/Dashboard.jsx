import { useEffect, useState } from "react";
import { api } from "../api";
import "./Dashboard.css";

// Format a number as Indian Rupees
function fmt(n) {
  return "Rs " + Number(n).toLocaleString("en-IN");
}

export default function Dashboard() {
  // State: what we're showing
  const [member, setMember]     = useState(null);
  const [wallet, setWallet]     = useState(null);
  const [benefits, setBenefits] = useState(null);
  const [loading, setLoading]   = useState(true);

  // Payment modal state
  const [showPay, setShowPay] = useState(false);
  const [payForm, setPayForm] = useState({ amount: "500", source: "HSA", description: "Medical checkup" });
  const [paying,  setPaying]  = useState(false);
  const [notice,  setNotice]  = useState("");
  const [isError, setIsError] = useState(false);

  // Load all data when the page opens
  useEffect(() => {
    async function load() {
      const [m, w, b] = await Promise.all([api.getMember(), api.getWallet(), api.getBenefits()]);
      setMember(m);
      setWallet(w);
      setBenefits(b);
      setLoading(false);
    }
    load();
  }, []);

  // Handle the payment form submit
  async function handlePay(e) {
    e.preventDefault();
    setPaying(true);
    try {
      const updated = await api.pay({
        amount: parseFloat(payForm.amount),
        source: payForm.source,
        description: payForm.description,
      });
      // Update wallet balances without a full reload
      setWallet(updated);
      setShowPay(false);
      setIsError(false);
      setNotice("Payment recorded.");
      setTimeout(() => setNotice(""), 3000);
    } catch (err) {
      setIsError(true);
      setNotice(err.message);
    } finally {
      setPaying(false);
    }
  }

  if (loading) return <p className="page-loading">Loading…</p>;

  return (
    <div className="dashboard">

      {/* Toast — success only */}
      {notice && !isError && (
        <div className="notice">
          {notice}
        </div>
      )}

      {/* Page header */}
      <div className="page-head">
        <h2>Account overview</h2>
        <p>Band {member.band} · {member.employer} · Member since {member.member_since.substring(0, 4)}</p>
      </div>

      {/* Intern notice */}
      {member.band === "E0" && (
        <div className="notice" style={{ backgroundColor: "#e0f2fe", color: "#0369a1", borderColor: "#bae6fd", marginBottom: "2rem" }}>
          <strong>Intern Benefits:</strong> Free annual health checkups only. No HSA or Emergency fund.
        </div>
      )}

      {/* Balance cards */}
      <div className="stat-row">
        <div className="stat">
          <span className="stat-label">HSA Balance</span>
          <span className="stat-value">{fmt(wallet.hsa_balance)}</span>
          <span className="stat-sub">Monthly allowance: {fmt(benefits.hsa_monthly_allowance)}</span>
        </div>
        <div className="stat">
          <span className="stat-label">Emergency Medical Fund</span>
          <span className="stat-value">{fmt(wallet.emergency_balance)}</span>
          <span className="stat-sub">Maximum limit: {fmt(benefits.emergency_limit)}</span>
        </div>
      </div>

      {/* Benefits summary panel */}
      <div className="panel-row">
        <section className="panel" style={{ flex: 1 }}>
          <h3>Benefits Summary</h3>
          <ul style={{ paddingLeft: "1.2rem", color: "#475467", lineHeight: "1.8" }}>
            <li><strong>Checkups:</strong> {benefits.checkups_covered ? "100% Covered" : "Not Covered"}</li>
            <li><strong>Monthly HSA:</strong> {fmt(benefits.hsa_monthly_allowance)} credited every month</li>
            <li><strong>Emergency Fund:</strong> Up to {fmt(benefits.emergency_limit)} for urgent care</li>
          </ul>
          {member.band !== "E0" && (
            <button className="btn" onClick={() => setShowPay(true)} style={{ marginTop: "1rem" }}>
              Make Payment
            </button>
          )}
        </section>
      </div>

      {/* Payment modal */}
      {showPay && (
        <div className="overlay" onClick={() => setShowPay(false)}>
          <div className="dialog" onClick={(e) => e.stopPropagation()}>
              <h3>Make Medical Payment</h3>
              {/* Error shown in red inside modal */}
              {isError && notice && (
                <div style={{ background: "#fef2f2", color: "#b91c1c", border: "1px solid #fca5a5", borderRadius: "4px", padding: "0.5rem 0.75rem", fontSize: "0.8125rem", marginBottom: "0.75rem" }}>
                  {notice}
                </div>
              )}
            <form onSubmit={handlePay}>
              <label>Amount
                <input type="number" min="1" max="100000" required
                  value={payForm.amount}
                  onChange={(e) => setPayForm({ ...payForm, amount: e.target.value })} />
              </label>
              <label>Pay From
                <select value={payForm.source} onChange={(e) => setPayForm({ ...payForm, source: e.target.value })}>
                  <option value="HSA">HSA ({fmt(wallet.hsa_balance)} available)</option>
                  <option value="Emergency Fund">Emergency Fund ({fmt(wallet.emergency_balance)} available)</option>
                </select>
              </label>
              <label>Description
                <input type="text" maxLength={120} required
                  value={payForm.description}
                  onChange={(e) => setPayForm({ ...payForm, description: e.target.value })} />
              </label>
              <div className="dialog-actions">
                <button type="button" className="btn-secondary" onClick={() => setShowPay(false)}>Cancel</button>
                <button type="submit" className="btn" disabled={paying}>{paying ? "Processing…" : "Submit"}</button>
              </div>
            </form>
          </div>
        </div>
      )}

    </div>
  );
}
