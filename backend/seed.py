from datetime import datetime, timedelta, timezone

# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session

from auth import hash_password
from database import Base, engine
from models import Benefits, Employee, Transaction, Wallet


def seed(db: Session) -> None:
    employees_data = [
        {
            "employee_id": "52381866",
            "password": "1234HCLTECH",
            "name": "Ayush Parashar",
            "band": "E0",
            "employer": "UnitedHealth Group",
            "member_since": "2022-03-01",
            "age": 25,
            "wallet": {"hsa_balance": 0.0, "emergency_balance": 0.0},
            "benefits": {"checkups_covered": True, "hsa_monthly_allowance": 0.0, "emergency_limit": 0.0},
            "transactions": [],
        },
        {
            "employee_id": "52381856",
            "password": "1234HCLTECH",
            "name": "Satyam Sangal",
            "band": "E1",
            "employer": "UnitedHealth Group",
            "member_since": "2020-08-15",
            "age": 25,
            "wallet": {"hsa_balance": 1000.0, "emergency_balance": 10000.0},
            "benefits": {"checkups_covered": True, "hsa_monthly_allowance": 1000.0, "emergency_limit": 10000.0},
            "transactions": [
                ("Basic checkup", "Medical", -250.0, "HSA"),
            ],
        },
        {
            "employee_id": "52381857",
            "password": "1234HCLTECH",
            "name": "Yash Jain",
            "band": "E2",
            "employer": "UnitedHealth Group",
            "member_since": "2018-01-10",
            "age": 25,
            "wallet": {"hsa_balance": 2000.0, "emergency_balance": 25000.0},
            "benefits": {"checkups_covered": True, "hsa_monthly_allowance": 2000.0, "emergency_limit": 25000.0},
            "transactions": [],
        },
        {
            "employee_id": "52381854",
            "password": "1234HCLTECH",
            "name": "Vandit Mittal",
            "band": "E3",
            "employer": "UnitedHealth Group",
            "member_since": "2021-05-12",
            "age": 25,
            "wallet": {"hsa_balance": 3000.0, "emergency_balance": 50000.0},
            "benefits": {"checkups_covered": True, "hsa_monthly_allowance": 3000.0, "emergency_limit": 50000.0},
            "transactions": [
                ("Emergency room visit", "Medical", -1200.0, "Emergency Fund"),
                ("Specialist consult", "Medical", -300.0, "HSA"),
            ],
        },
        {
            "employee_id": "52382046",
            "password": "1234HCLTECH",
            "name": "Shreeya Agarwal",
            "band": "E4",
            "employer": "UnitedHealth Group",
            "member_since": "2019-11-20",
            "age": 25,
            "wallet": {"hsa_balance": 4000.0, "emergency_balance": 75000.0},
            "benefits": {"checkups_covered": True, "hsa_monthly_allowance": 4000.0, "emergency_limit": 75000.0},
            "transactions": [],
        },
        {
            "employee_id": "52381898",
            "password": "1234HCLTECH",
            "name": "Mansi Prajapati",
            "band": "E5",
            "employer": "UnitedHealth Group",
            "member_since": "2023-02-14",
            "age": 25,
            "wallet": {"hsa_balance": 5000.0, "emergency_balance": 100000.0},
            "benefits": {"checkups_covered": True, "hsa_monthly_allowance": 5000.0, "emergency_limit": 100000.0},
            "transactions": [
                ("Executive health screening", "Medical", -1500.0, "HSA"),
            ],
        },
        {
            "employee_id": "52382051",
            "password": "1234HCLTECH",
            "name": "Mansi Saini",
            "band": "E1",
            "employer": "UnitedHealth Group",
            "member_since": "2020-05-10",
            "age": 25,
            "wallet": {"hsa_balance": 1000.0, "emergency_balance": 10000.0},
            "benefits": {"checkups_covered": True, "hsa_monthly_allowance": 1000.0, "emergency_limit": 10000.0},
            "transactions": [
                ("Basic checkup", "Medical", -250.0, "HSA"),
            ],
        },
        {
            "employee_id": "52381896",
            "password": "1234HCLTECH",
            "name": "Arpit Singh",
            "band": "E2",
            "employer": "UnitedHealth Group",
            "member_since": "2017-09-01",
            "age": 25,
            "wallet": {"hsa_balance": 2000.0, "emergency_balance": 25000.0},
            "benefits": {"checkups_covered": True, "hsa_monthly_allowance": 2000.0, "emergency_limit": 25000.0},
            "transactions": [],
        },
        {
            "employee_id": "52381868",
            "password": "1234HCLTECH",
            "name": "Anushka Srivastava",
            "band": "E3",
            "employer": "UnitedHealth Group",
            "member_since": "2021-12-05",
            "age": 25,
            "wallet": {"hsa_balance": 3000.0, "emergency_balance": 50000.0},
            "benefits": {"checkups_covered": True, "hsa_monthly_allowance": 3000.0, "emergency_limit": 50000.0},
            "transactions": [
                ("Specialist consult", "Medical", -300.0, "HSA"),
            ],
        },
    ]

    for idx, data in enumerate(employees_data, start=1):
        emp = Employee(
            employee_id=data["employee_id"],
            password=hash_password(data["password"]),
            name=data["name"],
            band=data["band"],
            employer=data["employer"],
            member_since=data["member_since"],
            age=data["age"],
        )
        db.add(emp)
        db.flush()

        w = data["wallet"]
        db.add(
            Wallet(
                employee_id=emp.id,
                hsa_balance=w["hsa_balance"],
                emergency_balance=w["emergency_balance"],
            )
        )

        b = data["benefits"]
        db.add(Benefits(employee_id=emp.id, **b))

        for t_idx, (desc, cat, amt, src) in enumerate(data["transactions"]):
            days_ago = (t_idx + 1) * 7
            db.add(
                Transaction(
                    employee_id=emp.id,
                    txn_id=f"TXN-{idx}{t_idx + 1:02d}",
                    txn_date=(datetime.now(timezone.utc) - timedelta(days=days_ago)).strftime("%Y-%m-%d"),
                    description=desc,
                    category=cat,
                    amount=amt,
                    source=src,
                    status="Completed",
                )
            )

    db.commit()


def init_db() -> None:
    print("Dropping existing tables...")
    Base.metadata.drop_all(bind=engine)
    print("Creating new tables...")
    Base.metadata.create_all(bind=engine)
    
    from database import SessionLocal

    db = SessionLocal()
    try:
        seed(db)
    finally:
        db.close()


if __name__ == "__main__":
    init_db()
    print("Database re-initialized and seeded with Band Data.")
