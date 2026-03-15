"""Database models for FinCredit Loan Calculator Bot"""

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

Base = declarative_base()


class PaymentType(enum.Enum):
    """Payment calculation types"""
    ANNUITY = "annuity"
    DIFFERENTIATED = "differentiated"


class User(Base):
    """User model"""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    username = Column(String(255))
    first_name = Column(String(255))
    last_name = Column(String(255))
    language = Column(String(2), default='ru')  # ru, en, hy
    reminder_enabled = Column(Boolean, default=True)
    reminder_days_before = Column(Integer, default=1)
    reminder_time = Column(String(5), default='09:00')
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    loans = relationship("Loan", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(telegram_id={self.telegram_id}, username={self.username})>"


class Loan(Base):
    """Loan model"""
    __tablename__ = 'loans'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    name = Column(String(255), nullable=False)  # e.g., "Кредит 1"
    amount = Column(Float, nullable=False)  # Loan amount
    interest_rate = Column(Float, nullable=False)  # Annual interest rate in %
    term_months = Column(Integer, nullable=False)  # Loan term in months
    payment_type = Column(Enum(PaymentType), nullable=False)
    start_date = Column(DateTime, nullable=True)  # Optional start date
    monthly_payment = Column(Float)  # Calculated monthly payment
    total_payment = Column(Float)  # Total amount to pay
    overpayment = Column(Float)  # Total overpayment
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="loans")
    payments = relationship("Payment", back_populates="loan", cascade="all, delete-orphan")
    extra_payments = relationship("ExtraPayment", back_populates="loan", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Loan(id={self.id}, name={self.name}, amount={self.amount})>"


class Payment(Base):
    """Payment schedule model"""
    __tablename__ = 'payments'

    id = Column(Integer, primary_key=True)
    loan_id = Column(Integer, ForeignKey('loans.id'), nullable=False)
    payment_number = Column(Integer, nullable=False)  # Payment number (1, 2, 3...)
    payment_date = Column(DateTime, nullable=True)  # Scheduled payment date
    amount = Column(Float, nullable=False)  # Payment amount
    principal = Column(Float, nullable=False)  # Principal part
    interest = Column(Float, nullable=False)  # Interest part
    remaining_balance = Column(Float, nullable=False)  # Remaining loan balance
    is_paid = Column(Boolean, default=False)
    paid_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    loan = relationship("Loan", back_populates="payments")

    def __repr__(self):
        return f"<Payment(loan_id={self.loan_id}, number={self.payment_number}, amount={self.amount})>"


class ExtraPayment(Base):
    """Extra payment model"""
    __tablename__ = 'extra_payments'

    id = Column(Integer, primary_key=True)
    loan_id = Column(Integer, ForeignKey('loans.id'), nullable=False)
    amount = Column(Float, nullable=False)
    payment_date = Column(DateTime, nullable=False)
    is_recurring = Column(Boolean, default=False)  # One-time or recurring
    recurrence_months = Column(Integer, nullable=True)  # Every N months
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    loan = relationship("Loan", back_populates="extra_payments")

    def __repr__(self):
        return f"<ExtraPayment(loan_id={self.loan_id}, amount={self.amount})>"
