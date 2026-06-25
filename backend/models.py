from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(String(32), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    name = Column(String(120), nullable=False)
    band = Column(String(20), nullable=False)  # E0, E1, E2, E3, E4, E5
    employer = Column(String(120), nullable=False)
    member_since = Column(String(10), nullable=False)
    age = Column(Integer, default=25)

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
    emergency_balance = Column(Float, default=0.0)
    last_updated = Column(DateTime, default=datetime.utcnow)

    employee = relationship("Employee", back_populates="wallet")


class Benefits(Base):
    __tablename__ = "benefits"

    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), unique=True, nullable=False)
    checkups_covered = Column(Boolean, default=True)
    hsa_monthly_allowance = Column(Float, nullable=False)
    emergency_limit = Column(Float, nullable=False)

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
    source = Column(String(20), nullable=False)  # 'HSA' or 'Emergency Fund'
    status = Column(String(20), default="Completed")

    employee = relationship("Employee", back_populates="transactions")
