# Optum Member Benefits Wallet

Employee-authenticated healthcare benefits wallet — HSA/FSA balances, deductible tracking, transactions, and US plan rules.

## What's new (v2)

- **Auth:** Employee ID + password (JWT), each user sees their own data
- **Database:** PostgreSQL via Neon (SQLite fallback for local dev)
- **Rulebook:** IRS 2026 HSA/FSA limits + employer policy (`RULEBOOK.md`)
- **UI:** Enterprise portal layout (sidebar, tables, no demo fluff)

---

## Test accounts

| Employee ID | Name | Notes |
|-------------|------|-------|
| EMP-1001 | Alex Morgan | Self-only HDHP |
| EMP-1002 | Jordan Lee | Family coverage |
| EMP-1003 | Sam Rivera | Age 58, HSA catch-up eligible |

Password for all: `Optum@2026`

---

## Local setup

### Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Optional: connect Neon (copy .env.example → .env)
# cp .env.example .env

python seed.py          # create tables + seed users
uvicorn main:app --reload
```

Without `DATABASE_URL`, SQLite file `optum_wallet.db` is used automatically.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Open **http://localhost:5173/login**

---

## NeonDB setup (when you have the key)

1. Create a project at [neon.tech](https://neon.tech)
2. Copy the connection string
3. Create `backend/.env`:

```env
DATABASE_URL=postgresql://user:pass@ep-xxx.neon.tech/neondb?sslmode=require
JWT_SECRET=your-long-random-secret
CORS_ORIGINS=http://localhost:5173,https://your-frontend-url.com
```

4. Run seed:

```bash
cd backend && source venv/bin/activate
python seed.py
uvicorn main:app --host 0.0.0.0 --port 8000
```

---

## Deploy checklist

| Layer | Suggestion |
|-------|------------|
| Database | Neon PostgreSQL |
| Backend | Railway, Render, or Fly.io |
| Frontend | Vercel or Netlify |
| Env vars | `DATABASE_URL`, `JWT_SECRET`, `CORS_ORIGINS`, `VITE_API_URL` |

Set `VITE_API_URL=https://your-api.com/api` when building the frontend.

---

## API

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/api/auth/login` | No | Employee ID + password |
| GET | `/api/member` | Yes | Profile |
| GET | `/api/wallet` | Yes | Balances + limits |
| GET | `/api/benefits` | Yes | Deductible, copays |
| GET | `/api/transactions` | Yes | Transaction history |
| GET | `/api/rules` | No | US healthcare rulebook |
| POST | `/api/wallet/pay-copay` | Yes | Pay from HSA/FSA |

---

## Presentation talking points

1. **Problem:** Members use separate systems for benefits, HSA, and claims.
2. **Solution:** Single authenticated wallet per employee.
3. **Auth:** Employee ID + password → JWT; data scoped per user in Postgres.
4. **Rules:** App follows IRS 2026 HSA limits ($4,400 self / $8,750 family) and employer minimums ($50/mo employee contribution).
5. **Demo:** Log in as EMP-1001 vs EMP-1002 — different balances, plans, transactions.
6. **Stack:** React (routes, auth context) + FastAPI + SQLAlchemy + Neon.

---

## Rulebook

See [`RULEBOOK.md`](RULEBOOK.md) for full US healthcare rules referenced by the app.
