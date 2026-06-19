from datetime import datetime, timedelta, timezone

# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session

from auth import hash_password
from database import Base, engine
from models import Benefits, Employee, Transaction, Wallet


def seed(db: Session) -> None:
    if db.query(Employee).first():
        return

    employees_data = [
        {
            "employee_id": "52381866",
            "password": "1234HCLTECH",
            "name": "Ayush Parashar",
            "plan": "Optum Select HDHP",
            "employer": "UnitedHealth Group",
            "member_since": "2022-03-01",
            "coverage_type": "self_only",
            "age": 25,
            "wallet": {"hsa_balance": 2840.50, "fsa_balance": 620.00, "hsa_contributed_ytd": 1200.00, "fsa_contributed_ytd": 800.00},
            "benefits": {
                "deductible_individual": 1700.00,
                "deductible_met": 875.00,
                "out_of_pocket_max": 8500.00,
                "out_of_pocket_met": 1240.00,
                "copay_primary_care": 25.00,
                "copay_specialist": 50.00,
                "copay_urgent_care": 75.00,
                "rx_generic": 10.00,
                "rx_brand": 35.00,
            },
            "transactions": [
                ("Primary care — Dr. Patel", "Medical", -25.00, "HSA"),
            ],
        },
        {
            "employee_id": "52381856",
            "password": "1234HCLTECH",
            "name": "Satyam Sangal",
            "plan": "Optum Family PPO",
            "employer": "UnitedHealth Group",
            "member_since": "2020-08-15",
            "coverage_type": "family",
            "age": 25,
            "wallet": {"hsa_balance": 5120.00, "fsa_balance": 1450.00, "hsa_contributed_ytd": 3200.00, "fsa_contributed_ytd": 1950.00},
            "benefits": {
                "deductible_individual": 3400.00,
                "deductible_met": 2100.00,
                "out_of_pocket_max": 17000.00,
                "out_of_pocket_met": 4800.00,
                "copay_primary_care": 30.00,
                "copay_specialist": 60.00,
                "copay_urgent_care": 90.00,
                "rx_generic": 15.00,
                "rx_brand": 45.00,
            },
            "transactions": [
                ("Pediatric visit — Dr. Kim", "Medical", -30.00, "HSA"),
            ],
        },
        {
            "employee_id": "52381857",
            "password": "1234HCLTECH",
            "name": "Yash Jain",
            "plan": "Optum Select HDHP",
            "employer": "UnitedHealth Group",
            "member_since": "2018-01-10",
            "coverage_type": "self_only",
            "age": 25,
            "wallet": {"hsa_balance": 8920.00, "fsa_balance": 0.00, "hsa_contributed_ytd": 4100.00, "fsa_contributed_ytd": 0.00},
            "benefits": {
                "deductible_individual": 1700.00,
                "deductible_met": 1700.00,
                "out_of_pocket_max": 8500.00,
                "out_of_pocket_met": 3200.00,
                "copay_primary_care": 0.00,
                "copay_specialist": 50.00,
                "copay_urgent_care": 75.00,
                "rx_generic": 10.00,
                "rx_brand": 35.00,
            },
            "transactions": [
                ("Specialist — cardiology follow-up", "Medical", -50.00, "HSA"),
            ],
        },
        {
            "employee_id": "52381854",
            "password": "1234HCLTECH",
            "name": "Vandit Mittal",
            "plan": "Optum Select HDHP",
            "employer": "UnitedHealth Group",
            "member_since": "2021-05-12",
            "coverage_type": "self_only",
            "age": 25,
            "wallet": {"hsa_balance": 3100.00, "fsa_balance": 200.00, "hsa_contributed_ytd": 1500.00, "fsa_contributed_ytd": 200.00},
            "benefits": {
                "deductible_individual": 1700.00,
                "deductible_met": 900.00,
                "out_of_pocket_max": 8500.00,
                "out_of_pocket_met": 1300.00,
                "copay_primary_care": 25.00,
                "copay_specialist": 50.00,
                "copay_urgent_care": 75.00,
                "rx_generic": 10.00,
                "rx_brand": 35.00,
            },
            "transactions": [
                ("Primary care — Dr. Patel", "Medical", -25.00, "HSA"),
            ],
        },
        {
            "employee_id": "52382046",
            "password": "1234HCLTECH",
            "name": "Shreeya Agarwal",
            "plan": "Optum Family PPO",
            "employer": "UnitedHealth Group",
            "member_since": "2019-11-20",
            "coverage_type": "family",
            "age": 25,
            "wallet": {"hsa_balance": 6200.00, "fsa_balance": 1800.00, "hsa_contributed_ytd": 4000.00, "fsa_contributed_ytd": 2000.00},
            "benefits": {
                "deductible_individual": 3400.00,
                "deductible_met": 2500.00,
                "out_of_pocket_max": 17000.00,
                "out_of_pocket_met": 5200.00,
                "copay_primary_care": 30.00,
                "copay_specialist": 60.00,
                "copay_urgent_care": 90.00,
                "rx_generic": 15.00,
                "rx_brand": 45.00,
            },
            "transactions": [
                ("Pediatric visit — Dr. Kim", "Medical", -30.00, "HSA"),
            ],
        },
        {
            "employee_id": "52381898",
            "password": "1234HCLTECH",
            "name": "Mansi Prajapati",
            "plan": "Optum Select HDHP",
            "employer": "UnitedHealth Group",
            "member_since": "2023-02-14",
            "coverage_type": "self_only",
            "age": 25,
            "wallet": {"hsa_balance": 1500.00, "fsa_balance": 0.00, "hsa_contributed_ytd": 1500.00, "fsa_contributed_ytd": 0.00},
            "benefits": {
                "deductible_individual": 1700.00,
                "deductible_met": 200.00,
                "out_of_pocket_max": 8500.00,
                "out_of_pocket_met": 300.00,
                "copay_primary_care": 25.00,
                "copay_specialist": 50.00,
                "copay_urgent_care": 75.00,
                "rx_generic": 10.00,
                "rx_brand": 35.00,
            },
            "transactions": [
                ("Specialist — dermatology", "Medical", -50.00, "HSA"),
            ],
        },
        {
            "employee_id": "52382051",
            "password": "1234HCLTECH",
            "name": "Mansi Saini",
            "plan": "Optum Select HDHP",
            "employer": "UnitedHealth Group",
            "member_since": "2020-05-10",
            "coverage_type": "self_only",
            "age": 25,
            "wallet": {"hsa_balance": 4200.00, "fsa_balance": 500.00, "hsa_contributed_ytd": 2200.00, "fsa_contributed_ytd": 500.00},
            "benefits": {
                "deductible_individual": 1700.00,
                "deductible_met": 1500.00,
                "out_of_pocket_max": 8500.00,
                "out_of_pocket_met": 2000.00,
                "copay_primary_care": 25.00,
                "copay_specialist": 50.00,
                "copay_urgent_care": 75.00,
                "rx_generic": 10.00,
                "rx_brand": 35.00,
            },
            "transactions": [
                ("Urgent Care", "Medical", -75.00, "HSA"),
            ],
        },
        {
            "employee_id": "52381896",
            "password": "1234HCLTECH",
            "name": "Arpit Singh",
            "plan": "Optum Family PPO",
            "employer": "UnitedHealth Group",
            "member_since": "2017-09-01",
            "coverage_type": "family",
            "age": 25,
            "wallet": {"hsa_balance": 7800.00, "fsa_balance": 2000.00, "hsa_contributed_ytd": 5000.00, "fsa_contributed_ytd": 2000.00},
            "benefits": {
                "deductible_individual": 3400.00,
                "deductible_met": 3000.00,
                "out_of_pocket_max": 17000.00,
                "out_of_pocket_met": 6000.00,
                "copay_primary_care": 30.00,
                "copay_specialist": 60.00,
                "copay_urgent_care": 90.00,
                "rx_generic": 15.00,
                "rx_brand": 45.00,
            },
            "transactions": [
                ("Dental — family cleaning", "Dental", -80.00, "FSA"),
            ],
        },
        {
            "employee_id": "52381868",
            "password": "1234HCLTECH",
            "name": "Anushka Srivastava",
            "plan": "Optum Select HDHP",
            "employer": "UnitedHealth Group",
            "member_since": "2021-12-05",
            "coverage_type": "self_only",
            "age": 25,
            "wallet": {"hsa_balance": 2500.00, "fsa_balance": 300.00, "hsa_contributed_ytd": 1000.00, "fsa_contributed_ytd": 300.00},
            "benefits": {
                "deductible_individual": 1700.00,
                "deductible_met": 700.00,
                "out_of_pocket_max": 8500.00,
                "out_of_pocket_met": 1000.00,
                "copay_primary_care": 25.00,
                "copay_specialist": 50.00,
                "copay_urgent_care": 75.00,
                "rx_generic": 10.00,
                "rx_brand": 35.00,
            },
            "transactions": [
                ("Primary care — Dr. Patel", "Medical", -25.00, "HSA"),
            ],
        },
    ]

    for idx, data in enumerate(employees_data, start=1):
        emp = Employee(
            employee_id=data["employee_id"],
            password_hash=hash_password(data["password"]),
            name=data["name"],
            plan=data["plan"],
            employer=data["employer"],
            member_since=data["member_since"],
            coverage_type=data["coverage_type"],
            age=data["age"],
        )
        db.add(emp)
        db.flush()

        w = data["wallet"]
        db.add(
            Wallet(
                employee_id=emp.id,
                hsa_balance=w["hsa_balance"],
                fsa_balance=w["fsa_balance"],
                hsa_contributed_ytd=w["hsa_contributed_ytd"],
                fsa_contributed_ytd=w["fsa_contributed_ytd"],
            )
        )

        b = data["benefits"]
        db.add(Benefits(employee_id=emp.id, plan_year="2026", **b))

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
                    status="Completed" if src != "Insurance" else "Processed",
                )
            )

    db.commit()


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
    from database import SessionLocal

    db = SessionLocal()
    try:
        seed(db)
    finally:
        db.close()


if __name__ == "__main__":
    init_db()
    print("Database initialized and seeded.")
