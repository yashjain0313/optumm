import os
from datetime import datetime, timezone

from fastapi import Depends, FastAPI, HTTPException

from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session

from auth import create_access_token, get_current_employee, verify_password
from database import get_db
from models import Employee, Transaction, Wallet
from rules import FSA, get_rulebook, hsa_annual_limit, hsa_remaining_allowance, fsa_remaining_allowance
from schemas import LoginRequest, LoginResponse, PayCopayRequest
from seed import init_db

app = FastAPI(
    title="Optum Member Benefits Wallet API",
    description="Employee-authenticated healthcare benefits wallet",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    init_db()


@app.get("/")
def root():
    return {"service": "Optum Member Benefits Wallet", "status": "healthy", "docs": "/docs"}


@app.post("/api/auth/login", response_model=LoginResponse)
def login(body: LoginRequest, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.employee_id == body.employee_id.upper()).first()
    if not employee or not verify_password(body.password, employee.password_hash):
        raise HTTPException(status_code=401, detail="Invalid employee ID or password")

    token = create_access_token(employee.employee_id)
    return LoginResponse(
        access_token=token,
        employee_id=employee.employee_id,
        name=employee.name,
    )


@app.get("/api/member")
def get_member(employee: Employee = Depends(get_current_employee)):
    return {
        "employee_id": employee.employee_id,
        "name": employee.name,
        "plan": employee.plan,
        "employer": employee.employer,
        "member_since": employee.member_since,
        "coverage_type": employee.coverage_type,
        "age": employee.age,
    }


@app.get("/api/wallet")
def get_wallet(employee: Employee = Depends(get_current_employee)):
    w = employee.wallet
    return {
        "hsa_balance": w.hsa_balance,
        "fsa_balance": w.fsa_balance,
        "hsa_contributed_ytd": w.hsa_contributed_ytd,
        "fsa_contributed_ytd": w.fsa_contributed_ytd,
        "hsa_annual_limit": hsa_annual_limit(employee.coverage_type, employee.age),
        "hsa_remaining": hsa_remaining_allowance(employee.coverage_type, employee.age, w.hsa_contributed_ytd),
        "fsa_annual_limit": FSA["annual_limit_healthcare"],
        "fsa_remaining": fsa_remaining_allowance(w.fsa_contributed_ytd),
        "last_updated": w.last_updated.isoformat() + "Z" if w.last_updated else None,
    }


@app.get("/api/benefits")
def get_benefits(employee: Employee = Depends(get_current_employee)):
    b = employee.benefits
    deductible_remaining = max(0, b.deductible_individual - b.deductible_met)
    oop_remaining = max(0, b.out_of_pocket_max - b.out_of_pocket_met)
    return {
        "deductible_individual": b.deductible_individual,
        "deductible_met": b.deductible_met,
        "deductible_remaining": round(deductible_remaining, 2),
        "out_of_pocket_max": b.out_of_pocket_max,
        "out_of_pocket_met": b.out_of_pocket_met,
        "out_of_pocket_remaining": round(oop_remaining, 2),
        "deductible_progress_pct": round((b.deductible_met / b.deductible_individual) * 100, 1) if b.deductible_individual else 0,
        "copay_primary_care": b.copay_primary_care,
        "copay_specialist": b.copay_specialist,
        "copay_urgent_care": b.copay_urgent_care,
        "rx_generic": b.rx_generic,
        "rx_brand": b.rx_brand,
        "plan_year": b.plan_year,
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


@app.get("/api/rules")
def get_rules():
    return get_rulebook()


@app.post("/api/wallet/pay-copay")
def pay_copay(
    body: PayCopayRequest,
    employee: Employee = Depends(get_current_employee),
    db: Session = Depends(get_db),
):
    wallet: Wallet = employee.wallet

    if body.source == "HSA" and body.amount > wallet.hsa_balance:
        raise HTTPException(status_code=400, detail="Insufficient HSA balance")
    if body.source == "FSA" and body.amount > wallet.fsa_balance:
        raise HTTPException(status_code=400, detail="Insufficient FSA balance")

    if body.source == "HSA":
        wallet.hsa_balance = round(wallet.hsa_balance - body.amount, 2)
    else:
        wallet.fsa_balance = round(wallet.fsa_balance - body.amount, 2)

    wallet.last_updated = datetime.now(timezone.utc)

    count = db.query(Transaction).filter(Transaction.employee_id == employee.id).count()
    txn = Transaction(
        employee_id=employee.id,
        txn_id=f"TXN-{employee.id}{count + 1:03d}",
        txn_date=datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        description=body.description,
        category="Medical",
        amount=-body.amount,
        source=body.source,
        status="Completed",
    )
    db.add(txn)
    db.commit()
    db.refresh(wallet)
    db.refresh(txn)

    return {
        "message": "Copay paid successfully",
        "transaction": {
            "id": txn.txn_id,
            "date": txn.txn_date,
            "description": txn.description,
            "category": txn.category,
            "amount": txn.amount,
            "source": txn.source,
            "status": txn.status,
        },
        "wallet": {
            "hsa_balance": wallet.hsa_balance,
            "fsa_balance": wallet.fsa_balance,
            "hsa_contributed_ytd": wallet.hsa_contributed_ytd,
            "fsa_contributed_ytd": wallet.fsa_contributed_ytd,
            "last_updated": wallet.last_updated.isoformat() + "Z",
        },
    }
