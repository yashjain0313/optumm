from datetime import datetime
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(String(32), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    name = Column(String(120), nullable=False)
    plan = Column(String(120), nullable=False)
    employer = Column(String(120), nullable=False)
    member_since = Column(String(10), nullable=False)
    coverage_type = Column(String(20), default="self_only")  # self_only | family
    age = Column(Integer, default=35)

    wallet = relationship("Wallet", back_populates="employee", uselist=False)
    benefits = relationship("Benefits", back_populates="employee", uselist=False)
    transactions = relationship(
        "Transaction",
        back_populates="employee",
        order_by="desc(Transaction.txn_date)",
    )


class Wallet(Base):
    __tablename__ = "wallets"

    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), unique=True, nullable=False)
    hsa_balance = Column(Float, default=0.0)
    fsa_balance = Column(Float, default=0.0)
    hsa_contributed_ytd = Column(Float, default=0.0)
    fsa_contributed_ytd = Column(Float, default=0.0)
    last_updated = Column(DateTime, default=datetime.utcnow)

    employee = relationship("Employee", back_populates="wallet")


class Benefits(Base):
    __tablename__ = "benefits"

    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), unique=True, nullable=False)
    deductible_individual = Column(Float, nullable=False)
    deductible_met = Column(Float, default=0.0)
    out_of_pocket_max = Column(Float, nullable=False)
    out_of_pocket_met = Column(Float, default=0.0)
    copay_primary_care = Column(Float, nullable=False)
    copay_specialist = Column(Float, nullable=False)
    copay_urgent_care = Column(Float, nullable=False)
    rx_generic = Column(Float, nullable=False)
    rx_brand = Column(Float, nullable=False)
    plan_year = Column(String(4), default="2026")

    employee = relationship("Employee", back_populates="benefits")


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    txn_id = Column(String(20), nullable=False)
    txn_date = Column(String(10), nullable=False)
    description = Column(String(200), nullable=False)
    category = Column(String(40), nullable=False)
    amount = Column(Float, nullable=False)
    source = Column(String(20), nullable=False)
    status = Column(String(20), default="Completed")

    employee = relationship("Employee", back_populates="transactions")
