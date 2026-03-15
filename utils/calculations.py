"""Loan calculation formulas"""

from typing import List, Dict, Tuple
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


def calculate_annuity_payment(principal: float, annual_rate: float, months: int) -> float:
    """
    Calculate monthly payment for annuity loan.
    
    Formula: A = P * (r * (1 + r)^n) / ((1 + r)^n - 1)
    where:
    A = monthly payment
    P = principal (loan amount)
    r = monthly interest rate (annual_rate / 12 / 100)
    n = number of months
    
    Args:
        principal: Loan amount
        annual_rate: Annual interest rate in percent (e.g., 12.5)
        months: Loan term in months
        
    Returns:
        Monthly payment amount
    """
    if annual_rate == 0:
        return principal / months
    
    monthly_rate = annual_rate / 12 / 100
    payment = principal * (monthly_rate * (1 + monthly_rate) ** months) / \
              ((1 + monthly_rate) ** months - 1)
    return round(payment, 2)


def calculate_annuity_schedule(principal: float, annual_rate: float, months: int, 
                               start_date: datetime = None) -> List[Dict]:
    """
    Calculate full payment schedule for annuity loan.
    
    Args:
        principal: Loan amount
        annual_rate: Annual interest rate in percent
        months: Loan term in months
        start_date: Loan start date (optional)
        
    Returns:
        List of payment dictionaries with schedule details
    """
    monthly_payment = calculate_annuity_payment(principal, annual_rate, months)
    monthly_rate = annual_rate / 12 / 100
    remaining_balance = principal
    schedule = []
    
    if start_date is None:
        start_date = datetime.now()
    
    for month in range(1, months + 1):
        interest_payment = round(remaining_balance * monthly_rate, 2)
        principal_payment = round(monthly_payment - interest_payment, 2)
        
        # Adjust last payment to cover any rounding differences
        if month == months:
            principal_payment = remaining_balance
            monthly_payment = principal_payment + interest_payment
        
        remaining_balance = max(0, round(remaining_balance - principal_payment, 2))
        payment_date = start_date + relativedelta(months=month)
        
        schedule.append({
            'payment_number': month,
            'payment_date': payment_date,
            'payment_amount': round(monthly_payment, 2),
            'principal': round(principal_payment, 2),
            'interest': round(interest_payment, 2),
            'remaining_balance': round(remaining_balance, 2)
        })
    
    return schedule


def calculate_differentiated_schedule(principal: float, annual_rate: float, months: int,
                                     start_date: datetime = None) -> List[Dict]:
    """
    Calculate full payment schedule for differentiated loan.
    
    Formula for each month:
    Principal payment = Total principal / Number of months
    Interest payment = Remaining balance * monthly rate
    Total payment = Principal payment + Interest payment
    
    Args:
        principal: Loan amount
        annual_rate: Annual interest rate in percent
        months: Loan term in months
        start_date: Loan start date (optional)
        
    Returns:
        List of payment dictionaries with schedule details
    """
    monthly_rate = annual_rate / 12 / 100
    principal_payment = principal / months
    remaining_balance = principal
    schedule = []
    
    if start_date is None:
        start_date = datetime.now()
    
    for month in range(1, months + 1):
        interest_payment = round(remaining_balance * monthly_rate, 2)
        
        # Adjust last payment to cover any rounding differences
        if month == months:
            current_principal = remaining_balance
        else:
            current_principal = round(principal_payment, 2)
        
        total_payment = round(current_principal + interest_payment, 2)
        remaining_balance = max(0, round(remaining_balance - current_principal, 2))
        payment_date = start_date + relativedelta(months=month)
        
        schedule.append({
            'payment_number': month,
            'payment_date': payment_date,
            'payment_amount': total_payment,
            'principal': round(current_principal, 2),
            'interest': round(interest_payment, 2),
            'remaining_balance': round(remaining_balance, 2)
        })
    
    return schedule


def calculate_loan_totals(principal: float, annual_rate: float, months: int,
                         payment_type: str = 'annuity') -> Dict[str, float]:
    """
    Calculate total loan costs.
    
    Args:
        principal: Loan amount
        annual_rate: Annual interest rate in percent
        months: Loan term in months
        payment_type: 'annuity' or 'differentiated'
        
    Returns:
        Dictionary with total_payment, overpayment, and monthly_payment
    """
    if payment_type == 'annuity':
        schedule = calculate_annuity_schedule(principal, annual_rate, months)
        monthly_payment = calculate_annuity_payment(principal, annual_rate, months)
    else:
        schedule = calculate_differentiated_schedule(principal, annual_rate, months)
        # For differentiated, first payment is typically the highest
        monthly_payment = schedule[0]['payment_amount'] if schedule else 0
    
    total_payment = sum(payment['payment_amount'] for payment in schedule)
    overpayment = total_payment - principal
    
    return {
        'monthly_payment': round(monthly_payment, 2),
        'total_payment': round(total_payment, 2),
        'overpayment': round(overpayment, 2)
    
