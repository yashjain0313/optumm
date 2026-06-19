# Optum Benefits Wallet — US Healthcare Rulebook (2026)

Reference document for the application. Rules are enforced in `backend/rules.py`.

---

## HSA — Health Savings Account (IRS Rev. Proc. 2025-19)

| Rule | 2026 Limit |
|------|------------|
| Annual contribution — self-only HDHP | **$4,400** |
| Annual contribution — family HDHP | **$8,750** |
| Catch-up (age 55+, not on Medicare) | **+$1,000** |
| HDHP minimum deductible — self-only | $1,700 |
| HDHP minimum deductible — family | $3,400 |
| HDHP max out-of-pocket — self-only | $8,500 |
| HDHP max out-of-pocket — family | $17,000 |

**Key rules:**
- Employee and employer contributions **combined** count toward the annual limit.
- Must be enrolled in a qualified **High-Deductible Health Plan (HDHP)**.
- HSA funds roll over year to year — no use-it-or-lose-it.
- Withdrawals for qualified medical expenses are **tax-free**.

---

## FSA — Flexible Spending Account

| Rule | 2026 Limit |
|------|------------|
| Healthcare FSA annual deferral | **$3,400** |
| Grace period (if offered) | Up to 75 days |
| Carryover (if offered) | Up to 15% of limit (~$510) |

**Key rules:**
- Generally **use-it-or-lose-it** unless employer offers grace period or carryover.
- Cannot contribute to a general healthcare FSA and HSA in the same year (limited-purpose FSA is allowed with HSA).

---

## Employer Plan Policy (Optum)

| Policy | Amount |
|--------|--------|
| Minimum employee HSA contribution | **$50/month** |
| Employer HSA seed contribution | **$75/month** |
| Employer match (max) | **$100/month** |
| Match requires minimum employee contribution | Yes |

These are organizational rules on top of IRS limits. The app validates minimum contribution amounts against this policy.

---

## Copays & Cost Sharing

Copays vary by plan tier. The app stores per-member values in the database:
- Primary care, specialist, urgent care
- Generic and brand prescription copays
- Deductible and out-of-pocket maximum tracking

---

## Sources

- [IRS Rev. Proc. 2025-19](https://www.irs.gov/pub/irs-drop/rp-25-19.pdf)
- [IRS Publication 502 — Medical Expenses](https://www.irs.gov/publications/p502)
- Optum employer benefits policy (internal)
