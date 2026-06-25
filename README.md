# Optum Benefits Wallet

An employee benefits portal where employees log in with their ID and password to view their HSA balance, Emergency Medical Fund, and transaction history. Benefits are tied to employee bands (E0–E5).

**Stack:** React + FastAPI + SQLAlchemy + SQLite (local) / PostgreSQL (production)

---

## How it works

- Employee logs in → gets a **JWT token**
- Token is used on every API call to fetch **their own data only**
- Benefits (monthly HSA, emergency fund) are determined by their **band (E0–E5)**

| Band | Role | Monthly HSA | Emergency Fund |
|------|------|-------------|----------------|
| E0 | Intern | Rs 0 | Rs 0 (checkups only) |
| E1 | Junior | Rs 1,000 | Rs 10,000 |
| E2 | Mid-Level | Rs 2,000 | Rs 25,000 |
| E3 | Senior | Rs 3,000 | Rs 50,000 |
| E4 | Lead | Rs 4,000 | Rs 75,000 |
| E5 | Executive | Rs 5,000 | Rs 1,00,000 |

---

## Test accounts

Password for all: `1234HCLTECH`

| Employee ID | Name | Band |
|-------------|------|------|
| 52381866 | Ayush Parashar | E0 |
| 52381856 | Satyam Sangal | E1 |
| 52381857 | Yash Jain | E2 |
| 52381854 | Vandit Mittal | E3 |
| 52382046 | Shreeya Agarwal | E4 |
| 52381898 | Mansi Prajapati | E5 |
| 52382051 | Mansi Saini | E1 |
| 52381896 | Arpit Singh | E2 |
| 52381868 | Anushka Srivastava | E3 |

---

## Local setup

### Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

python3 seed.py          # drops + recreates tables, seeds all employees
uvicorn main:app --reload
```

> **Note:** Always run `source venv/bin/activate` first. The system Python 3.13 has a known SQLAlchemy bug.

Without `DATABASE_URL` in `.env`, it uses **SQLite** (`backend/optum_wallet.db`) automatically.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Open **http://localhost:5173**

---

## API endpoints

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/api/auth/login` | No | Login with employee ID + password |
| GET | `/api/member` | Yes | Employee info (name, band, employer) |
| GET | `/api/wallet` | Yes | HSA + Emergency Fund balances |
| GET | `/api/benefits` | Yes | Monthly allowance + emergency limit |
| GET | `/api/transactions` | Yes | Payment history |
| POST | `/api/wallet/pay` | Yes | Deduct from HSA or Emergency Fund |

---

## Production (NeonDB)

Create `backend/.env`:

```env
DATABASE_URL=postgresql://user:pass@ep-xxx.neon.tech/neondb?sslmode=require
JWT_SECRET=your-long-random-secret
```

Then run `python3 seed.py` once to populate the database.
