from datetime import datetime, timezone

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from auth import create_access_token, get_current_employee, verify_password
from database import get_db
from models import Employee, Transaction, Wallet
from schemas import LoginRequest, LoginResponse, PayRequest

app = FastAPI(title="Optum Benefits Wallet")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Auth ──────────────────────────────────────────────────────────────────────

@app.post("/api/auth/login", response_model=LoginResponse)
def login(body: LoginRequest, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.employee_id == body.employee_id).first()
    if not employee or not verify_password(body.password, employee.password):
        raise HTTPException(status_code=401, detail="Invalid employee ID or password")
    token = create_access_token(employee.employee_id)
    return LoginResponse(access_token=token, employee_id=employee.employee_id, name=employee.name)


# ── Employee data (protected) ─────────────────────────────────────────────────

@app.get("/api/member")
def get_member(employee: Employee = Depends(get_current_employee)):
    return {
        "employee_id": employee.employee_id,
        "name": employee.name,
        "band": employee.band,
        "employer": employee.employer,
        "member_since": employee.member_since,
    }


@app.get("/api/wallet")
def get_wallet(employee: Employee = Depends(get_current_employee)):
    w = employee.wallet
    return {
        "hsa_balance": w.hsa_balance,
        "emergency_balance": w.emergency_balance,
    }


@app.get("/api/benefits")
def get_benefits(employee: Employee = Depends(get_current_employee)):
    b = employee.benefits
    return {
        "checkups_covered": b.checkups_covered,
        "hsa_monthly_allowance": b.hsa_monthly_allowance,
        "emergency_limit": b.emergency_limit,
    }


@app.get("/api/transactions")
def get_transactions(employee: Employee = Depends(get_current_employee)):
    return [
        {
            "id": t.txn_id,
            "date": t.txn_date,
            "description": t.description,
            "category": t.category,
            "amount": t.amount,
            "source": t.source,
            "status": t.status,
        }
        for t in employee.transactions
    ]


# ── Payment ───────────────────────────────────────────────────────────────────

@app.post("/api/wallet/pay")
def pay(body: PayRequest, employee: Employee = Depends(get_current_employee), db: Session = Depends(get_db)):
    wallet: Wallet = employee.wallet

    if body.source == "HSA" and body.amount > wallet.hsa_balance:
        raise HTTPException(status_code=400, detail="Insufficient HSA balance")
    if body.source == "Emergency Fund" and body.amount > wallet.emergency_balance:
        raise HTTPException(status_code=400, detail="Insufficient Emergency balance")

    # Deduct from the right wallet
    if body.source == "HSA":
        wallet.hsa_balance = round(wallet.hsa_balance - body.amount, 2)
    else:
        wallet.emergency_balance = round(wallet.emergency_balance - body.amount, 2)

    # Save transaction record
    count = db.query(Transaction).filter(Transaction.employee_id == employee.id).count()
    db.add(Transaction(
        employee_id=employee.id,
        txn_id=f"TXN-{employee.id}{count + 1:03d}",
        txn_date=datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        description=body.description,
        category="Medical",
        amount=-body.amount,
        source=body.source,
        status="Completed",
    ))
    db.commit()
    db.refresh(wallet)

    return {"hsa_balance": wallet.hsa_balance, "emergency_balance": wallet.emergency_balance}
