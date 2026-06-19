import { useEffect, useState } from "react";
import { api } from "../api";
import "./Rules.css";

function fmt(n) {
  return new Intl.NumberFormat("en-US", { style: "currency", currency: "USD" }).format(n);
}

export default function Rules() {
  const [rules, setRules] = useState(null);

  useEffect(() => {
    api.getRules().then(setRules);
  }, []);

  if (!rules) return <p className="page-loading">Loading plan rules…</p>;

  const { hsa, fsa, employer_plan } = rules;

  return (
    <div className="rules-page">
      <div className="page-head">
        <h2>Plan rules — {rules.plan_year}</h2>
        <p>{rules.source}</p>
      </div>

      <section className="rules-section">
        <h3>HSA limits (IRS)</h3>
        <table className="rules-table">
          <tbody>
            <tr><td>Self-only annual contribution</td><td>{fmt(hsa.annual_limit_self_only)}</td></tr>
            <tr><td>Family annual contribution</td><td>{fmt(hsa.annual_limit_family)}</td></tr>
            <tr><td>Catch-up (age {hsa.catch_up_age}+)</td><td>{fmt(hsa.catch_up_amount)}</td></tr>
            <tr><td>HDHP min deductible (self)</td><td>{fmt(hsa.hdhp_min_deductible_self)}</td></tr>
            <tr><td>HDHP min deductible (family)</td><td>{fmt(hsa.hdhp_min_deductible_family)}</td></tr>
          </tbody>
        </table>
        <ul className="rules-notes">
          {hsa.notes.map((n, i) => <li key={i}>{n}</li>)}
        </ul>
      </section>

      <section className="rules-section">
        <h3>FSA limits</h3>
        <table className="rules-table">
          <tbody>
            <tr><td>Healthcare FSA annual limit</td><td>{fmt(fsa.annual_limit_healthcare)}</td></tr>
            <tr><td>Grace period (if offered)</td><td>{fsa.grace_period_days} days</td></tr>
          </tbody>
        </table>
        <ul className="rules-notes">
          {fsa.notes.map((n, i) => <li key={i}>{n}</li>)}
        </ul>
      </section>

      <section className="rules-section">
        <h3>Employer policy — {employer_plan.employer_name}</h3>
        <table className="rules-table">
          <tbody>
            <tr><td>Minimum employee HSA contribution</td><td>{fmt(employer_plan.minimum_employee_hsa_monthly)}/month</td></tr>
            <tr><td>Employer HSA seed</td><td>{fmt(employer_plan.employer_hsa_seed_monthly)}/month</td></tr>
            <tr><td>Employer match (max)</td><td>{fmt(employer_plan.employer_match_max_monthly)}/month</td></tr>
            <tr><td>Enrollment window</td><td>{employer_plan.fsa_enrollment_window}</td></tr>
          </tbody>
        </table>
      </section>
    </div>
  );
}
