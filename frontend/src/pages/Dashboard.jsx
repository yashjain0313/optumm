import { Navigate } from "react-router-dom";
import { useCallback, useEffect, useState } from "react";
import { api } from "../api";
import Layout from "../components/Layout";
import "./Dashboard.css";

function fmt(n) {
  return new Intl.NumberFormat("en-US", { style: "currency", currency: "USD" }).format(n);
}

function Meter({ label, used, total }) {
  const pct = total > 0 ? Math.min(100, (used / total) * 100) : 0;
  return (
    <div className="meter">
      <div className="meter-top">
        <span>{label}</span>
        <span>{fmt(used)} of {fmt(total)}</span>
      </div>
      <div className="meter-bar">
        <div className="meter-fill" style={{ width: `${pct}%` }} />
      </div>
    </div>
  );
}

export default function Dashboard() {
  const isAuthenticated = !!localStorage.getItem("token");

  const [member, setMember] = useState(null);
  const [wallet, setWallet] = useState(null);
  const [benefits, setBenefits] = useState(null);
  const [loading, setLoading] = useState(true);
  const [showPay, setShowPay] = useState(false);
  const [payForm, setPayForm] = useState({ amount: "25", source: "HSA", description: "Office visit copay" });
  const [paying, setPaying] = useState(false);
  const [notice, setNotice] = useState("");

  const load = useCallback(async () => {
    const [m, w, b] = await Promise.all([api.getMember(), api.getWallet(), api.getBenefits()]);
    setMember(m);
    setWallet(w);
    setBenefits(b);
    setLoading(false);
  }, []);

  useEffect(() => { load(); }, [load]);

  async function handlePay(e) {
    e.preventDefault();
    setPaying(true);
    try {
      await api.payCopay({
        amount: parseFloat(payForm.amount),
        source: payForm.source,
        description: payForm.description,
      });
      setShowPay(false);
      setNotice("Payment recorded.");
      setTimeout(() => setNotice(""), 3000);
      load();
    } catch (err) {
      setNotice(err.message);
    } finally {
      setPaying(false);
    }
  }

  if (!isAuthenticated) return <Navigate to="/login" replace />;
  if (loading) return <Layout><p className="page-loading">Loading account…</p></Layout>;

  return (
    <Layout>
      <div className="dashboard">
        {notice && <div className="notice">{notice}</div>}

      <div className="page-head">
        <h2>Account overview</h2>
        <p>{member.plan} · {member.coverage_type === "family" ? "Family" : "Self-only"} coverage · Plan year {benefits.plan_year}</p>
      </div>

      <div className="stat-row">
        <div className="stat">
          <span className="stat-label">HSA balance</span>
          <span className="stat-value">{fmt(wallet.hsa_balance)}</span>
          <span className="stat-sub">{fmt(wallet.hsa_contributed_ytd)} contributed · {fmt(wallet.hsa_remaining)} remaining</span>
        </div>
        <div className="stat">
          <span className="stat-label">FSA balance</span>
          <span className="stat-value">{fmt(wallet.fsa_balance)}</span>
          <span className="stat-sub">{fmt(wallet.fsa_contributed_ytd)} contributed · {fmt(wallet.fsa_remaining)} remaining</span>
        </div>
        <div className="stat">
          <span className="stat-label">HSA annual limit</span>
          <span className="stat-value">{fmt(wallet.hsa_annual_limit)}</span>
          <span className="stat-sub">IRS 2026 · {member.age >= 55 ? "includes catch-up" : "standard limit"}</span>
        </div>
      </div>

      <div className="panel-row">
        <section className="panel">
          <h3>Deductible & out-of-pocket</h3>
          <Meter label="Deductible" used={benefits.deductible_met} total={benefits.deductible_individual} />
          <Meter label="Out-of-pocket max" used={benefits.out_of_pocket_met} total={benefits.out_of_pocket_max} />
        </section>

        <section className="panel">
          <h3>Copay schedule</h3>
          <dl className="copay-list">
            <div><dt>Primary care</dt><dd>{fmt(benefits.copay_primary_care)}</dd></div>
            <div><dt>Specialist</dt><dd>{fmt(benefits.copay_specialist)}</dd></div>
            <div><dt>Urgent care</dt><dd>{fmt(benefits.copay_urgent_care)}</dd></div>
            <div><dt>Generic Rx</dt><dd>{fmt(benefits.rx_generic)}</dd></div>
            <div><dt>Brand Rx</dt><dd>{fmt(benefits.rx_brand)}</dd></div>
          </dl>
          <button type="button" className="btn" onClick={() => setShowPay(true)}>Pay copay</button>
        </section>
      </div>

      {showPay && (
        <div className="overlay" onClick={() => setShowPay(false)}>
          <div className="dialog" onClick={(e) => e.stopPropagation()}>
            <h3>Pay copay</h3>
            <form onSubmit={handlePay}>
              <label>Amount<input type="number" min="0.01" max="500" step="0.01" required value={payForm.amount} onChange={(e) => setPayForm({ ...payForm, amount: e.target.value })} /></label>
              <label>Account
                <select value={payForm.source} onChange={(e) => setPayForm({ ...payForm, source: e.target.value })}>
                  <option value="HSA">HSA ({fmt(wallet.hsa_balance)})</option>
                  <option value="FSA">FSA ({fmt(wallet.fsa_balance)})</option>
                </select>
              </label>
              <label>Description<input type="text" maxLength={120} value={payForm.description} onChange={(e) => setPayForm({ ...payForm, description: e.target.value })} /></label>
              <div className="dialog-actions">
                <button type="button" className="btn-secondary" onClick={() => setShowPay(false)}>Cancel</button>
                <button type="submit" className="btn" disabled={paying}>{paying ? "Processing…" : "Submit"}</button>
              </div>
            </form>
          </div>
        </div>
      )}
      </div>
    </Layout>
  );
}
