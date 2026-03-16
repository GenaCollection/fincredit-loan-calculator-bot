"""Database models for FinCredit Loan Calculator Bot"""
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Enum as SQLEnum, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

Base = declarative_base()


class PaymentType(enum.Enum):
    """Payment type enum"""
    ANNUITY = "annuity"
    DIFFERENTIATED = "differentiated"


class ReductionType(enum.Enum):
    """Early repayment reduction type"""
    PAYMENT = "payment"  # Уменьшать платеж
    TERM = "term"  # Уменьшать срок


class ExtraPaymentType(enum.Enum):
    """Type of extra payment"""
    ONE_TIME = "one_time"  # Разово
    PERIOD = "period"  # Период
    RECURRING = "recurring"  # Весь срок (ежемесячно)


class User(Base):
    """User model"""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False, index=True)
    username = Column(String(255), nullable=True)
    first_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)
    language = Column(String(10), default='ru')  # ru, en, hy
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Reminder settings
    reminder_enabled = Column(Boolean, default=True)
    reminder_days_before = Column(Integer, default=3)
    
    # Relationships
    loans = relationship("Loan", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(telegram_id={self.telegram_id}, username={self.username})>"


class Loan(Base):
    """Loan model with enhanced features"""
    __tablename__ = 'loans'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    
    # Basic loan info
    name = Column(String(255), default='Кредит')
    principal = Column(Float, nullable=False)
    annual_rate = Column(Float, nullable=False)
    months = Column(Integer, nullable=False)
    payment_type = Column(SQLEnum(PaymentType), default=PaymentType.ANNUITY)
    
    # Dates
    start_date = Column(DateTime, default=datetime.utcnow)
    first_payment_date = Column(DateTime, nullable=True)
    
    # NEW: Insurance
    has_insurance = Column(Boolean, default=False)
    insurance_monthly = Column(Float, default=0.0)
    
    # NEW: Early repayment settings
    has_extra_payments = Column(Boolean, default=False)
    extra_payment_amount = Column(Float, default=0.0)
    extra_payment_type = Column(SQLEnum(ExtraPaymentType), nullable=True)
    reduction_type = Column(SQLEnum(ReductionType), default=ReductionType.TERM)
    
    # NEW: Calculation settings
    use_exact_days = Column(Boolean, default=True)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Cached calculations
    monthly_payment = Column(Float, nullable=True)
    total_payment = Column(Float, nullable=True)
    total_overpayment = Column(Float, nullable=True)
    actual_months = Column(Integer, nullable=True)  # После досрочных погашений
    
    # Relationships
    user = relationship("User", back_populates="loans")
    payments = relationship("Payment", back_populates="loan", cascade="all, delete-orphan")
    extra_payments = relationship("ExtraPayment", back_populates="loan", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Loan(id={self.id}, name={self.name}, principal={self.principal})>"


class Payment(Base):
    """Payment schedule entry"""
    __tablename__ = 'payments'
    
    id = Column(Integer, primary_key=True)
    loan_id = Column(Integer, ForeignKey('loans.id'), nullable=False, index=True)
    
    payment_number = Column(Integer, nullable=False)
    payment_date = Column(DateTime, nullable=False)
    
    # Payment breakdown
    payment_amount = Column(Float, nullable=False)
    principal_amount = Column(Float, nullable=False)
    interest_amount = Column(Float, nullable=False)
    insurance_amount = Column(Float, default=0.0)  # NEW
    remaining_balance = Column(Float, nullable=False)
    
    # Payment status
    is_paid = Column(Boolean, default=False)
    paid_date = Column(DateTime, nullable=True)
    paid_amount = Column(Float, nullable=True)
    
    # NEW: Extra payment in this month
    extra_payment_amount = Column(Float, default=0.0)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    loan = relationship("Loan", back_populates="payments")
    
    def __repr__(self):
        return f"<Payment(id={self.id}, loan_id={self.loan_id}, payment_number={self.payment_number})>"


class ExtraPayment(Base):
    """Extra/early payment record"""
    __tablename__ = 'extra_payments'
    
    id = Column(Integer, primary_key=True)
    loan_id = Column(Integer, ForeignKey('loans.id'), nullable=False, index=True)
    
    # Extra payment details
    amount = Column(Float, nullable=False)
    payment_month = Column(Integer, nullable=False)  # В каком месяце применить
    extra_type = Column(SQLEnum(ExtraPaymentType), nullable=False)
    
    # For period type
    start_month = Column(Integer, nullable=True)
    end_month = Column(Integer, nullable=True)
    
    # Status
    is_applied = Column(Boolean, default=False)
    applied_date = Column(DateTime, nullable=True)
    
    # Description
    description = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    loan = relationship("Loan", back_populates="extra_payments")
    
    def __repr__(self):
        return f"<ExtraPayment(id={self.id}, loan_id={self.loan_id}, amount={self.amount})>"


class ReminderLog(Base):
    """Log of sent reminders"""
    __tablename__ = 'reminder_logs'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    loan_id = Column(Integer, ForeignKey('loans.id'), nullable=False)
    payment_id = Column(Integer, ForeignKey('payments.id'), nullable=True)
    
    reminder_date = Column(DateTime, default=datetime.utcnow)
    payment_due_date = Column(DateTime, nullable=False)
    
    was_sent = Column(Boolean, default=False)
    sent_at = Column(DateTime, nullable=True)
    
    def __repr__(self):
        return f"<ReminderLog(id={self.id}, loan_id={self.loan_id})>"
