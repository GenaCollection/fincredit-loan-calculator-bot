"""Enhanced loan calculation formulas with early repayment support"""
from typing import List, Dict, Tuple, Optional
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


def calculate_annuity_payment(principal: float, annual_rate: float, months: int) -> float:
    """Calculate monthly payment for annuity loan."""
    if annual_rate == 0:
        return principal / months
    
    monthly_rate = annual_rate / 12 / 100
    payment = principal * (monthly_rate * (1 + monthly_rate) ** months) / \
              ((1 + monthly_rate) ** months - 1)
    return round(payment, 2)


def calculate_days_in_period(start_date: datetime, end_date: datetime) -> int:
    """Calculate exact number of days between dates."""
    return (end_date - start_date).days


def calculate_daily_interest_rate(annual_rate: float, year: int) -> float:
    """Calculate daily interest rate based on year (365 or 366 days)."""
    days_in_year = 366 if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0) else 365
    return annual_rate / days_in_year / 100


def calculate_annuity_schedule_with_extras(
    principal: float,
    annual_rate: float,
    months: int,
    start_date: Optional[datetime] = None,
    extra_payments: Optional[List[Dict]] = None,
    reduction_type: str = 'payment',  # 'payment' or 'term'
    insurance_monthly: float = 0.0,
    use_exact_days: bool = True
) -> Tuple[List[Dict], Dict]:
    """
    Calculate full payment schedule with early repayments support.
    
    Args:
        principal: Loan amount
        annual_rate: Annual interest rate in percent
        months: Initial loan term in months
        start_date: Loan start date
        extra_payments: List of extra payment dicts with 'amount', 'month', 'type'
        reduction_type: 'payment' (reduce monthly payment) or 'term' (reduce term)
        insurance_monthly: Monthly insurance payment
        use_exact_days: Use exact days for interest calculation
        
    Returns:
        Tuple of (schedule list, summary dict)
    """
    if start_date is None:
        start_date = datetime.now()
    
    monthly_payment = calculate_annuity_payment(principal, annual_rate, months)
    monthly_rate = annual_rate / 12 / 100
    remaining_balance = principal
    schedule = []
    total_extra = 0
    
    # Process extra payments
    extra_map = {}
    if extra_payments:
        for extra in extra_payments:
            month_num = extra.get('month', 0)
            if month_num not in extra_map:
                extra_map[month_num] = 0
            extra_map[month_num] += extra.get('amount', 0)
    
    current_month = 1
    remaining_months = months
    
    while remaining_balance > 0.01 and current_month <= months + 120:  # Max 120 extra months
        payment_date = start_date + relativedelta(months=current_month)
        
        # Calculate interest
        if use_exact_days:
            prev_date = start_date + relativedelta(months=current_month - 1)
            days = calculate_days_in_period(prev_date, payment_date)
            daily_rate = calculate_daily_interest_rate(annual_rate, payment_date.year)
            interest_payment = round(remaining_balance * daily_rate * days, 2)
        else:
            interest_payment = round(remaining_balance * monthly_rate, 2)
        
        # Regular principal payment
        principal_payment = min(monthly_payment - interest_payment, remaining_balance)
        
        # Add extra payment
        extra_amount = extra_map.get(current_month, 0)
        if extra_amount > 0:
            total_extra += extra_amount
            principal_payment += extra_amount
            principal_payment = min(principal_payment, remaining_balance)
        
        total_payment = round(principal_payment + interest_payment + insurance_monthly, 2)
        remaining_balance = max(0, round(remaining_balance - principal_payment, 2))
        
        schedule.append({
            'payment_number': current_month,
            'payment_date': payment_date,
            'payment_amount': total_payment,
            'principal': round(principal_payment, 2),
            'interest': round(interest_payment, 2),
            'insurance': insurance_monthly,
            'extra_payment': extra_amount,
            'remaining_balance': remaining_balance
        })
        
        # Recalculate if reducing payment
        if extra_amount > 0 and reduction_type == 'payment' and remaining_balance > 0:
            remaining_months = months - current_month
            if remaining_months > 0:
                monthly_payment = calculate_annuity_payment(
                    remaining_balance, annual_rate, remaining_months
                )
        
        current_month += 1
        
        if remaining_balance <= 0:
            break
    
    # Calculate summary
    total_paid = sum(p['payment_amount'] for p in schedule)
    total_interest = sum(p['interest'] for p in schedule)
    total_insurance = sum(p['insurance'] for p in schedule)
    
    summary = {
        'total_payment': round(total_paid, 2),
        'total_principal': principal,
        'total_interest': round(total_interest, 2),
        'total_insurance': round(total_insurance, 2),
        'total_extra_payments': round(total_extra, 2),
        'overpayment': round(total_paid - principal, 2),
        'overpayment_without_extras': round(total_interest + total_insurance, 2),
        'actual_months': len(schedule),
        'months_saved': months - len(schedule)
    }
    
    return schedule, summary


def calculate_recurring_extra_payment_schedule(
    principal: float,
    annual_rate: float,
    months: int,
    extra_monthly: float,
    reduction_type: str = 'payment',
    start_date: Optional[datetime] = None,
    insurance_monthly: float = 0.0
) -> Tuple[List[Dict], Dict]:
    """
    Calculate schedule with recurring extra payments (like t-j.ru "Весь срок").
    
    Args:
        principal: Loan amount
        annual_rate: Annual interest rate
        months: Loan term
        extra_monthly: Additional monthly payment
        reduction_type: 'payment' or 'term'
        start_date: Start date
        insurance_monthly: Monthly insurance
        
    Returns:
        Tuple of (schedule, summary)
    """
    extra_payments = [
        {'month': m, 'amount': extra_monthly, 'type': 'recurring'}
        for m in range(1, months + 1)
    ]
    
    return calculate_annuity_schedule_with_extras(
        principal=principal,
        annual_rate=annual_rate,
        months=months,
        start_date=start_date,
        extra_payments=extra_payments,
        reduction_type=reduction_type,
        insurance_monthly=insurance_monthly
    )


def compare_reduction_strategies(
    principal: float,
    annual_rate: float,
    months: int,
    extra_monthly: float,
    insurance_monthly: float = 0.0
) -> Dict:
    """
    Compare two strategies: reducing payment vs reducing term.
    
    Returns:
        Dict with comparison data for both strategies
    """
    # Strategy 1: Reduce payment
    schedule_payment, summary_payment = calculate_recurring_extra_payment_schedule(
        principal, annual_rate, months, extra_monthly, 'payment', None, insurance_monthly
    )
    
    # Strategy 2: Reduce term
    schedule_term, summary_term = calculate_recurring_extra_payment_schedule(
        principal, annual_rate, months, extra_monthly, 'term', None, insurance_monthly
    )
    
    return {
        'reduce_payment': {
            'schedule': schedule_payment,
            'summary': summary_payment,
            'final_months': summary_payment['actual_months'],
            'total_overpayment': summary_payment['overpayment']
        },
        'reduce_term': {
            'schedule': schedule_term,
            'summary': summary_term,
            'final_months': summary_term['actual_months'],
            'total_overpayment': summary_term['overpayment']
        },
        'difference': {
            'months_saved': summary_payment['actual_months'] - summary_term['actual_months'],
            'money_saved': summary_payment['overpayment'] - summary_term['overpayment']
        }
    }


# Keep old functions for backward compatibility
def calculate_annuity_schedule(principal: float, annual_rate: float, months: int, 
                               start_date: datetime = None) -> List[Dict]:
    """Legacy function - use calculate_annuity_schedule_with_extras instead."""
    schedule, _ = calculate_annuity_schedule_with_extras(
        principal, annual_rate, months, start_date, None, 'term', 0.0, False
    )
    return schedule


def calculate_differentiated_schedule(principal: float, annual_rate: float, months: int,
                                     start_date: datetime = None) -> List[Dict]:
    """Calculate full payment schedule for differentiated loan."""
    monthly_rate = annual_rate / 12 / 100
    principal_payment = principal / months
    remaining_balance = principal
    schedule = []
    
    if start_date is None:
        start_date = datetime.now()
    
    for month in range(1, months + 1):
        interest_payment = round(remaining_balance * monthly_rate, 2)
        
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
    """Calculate total loan costs."""
    if payment_type == 'annuity':
        schedule = calculate_annuity_schedule(principal, annual_rate, months)
        monthly_payment = calculate_annuity_payment(principal, annual_rate, months)
    else:
        schedule = calculate_differentiated_schedule(principal, annual_rate, months)
        monthly_payment = schedule[0]['payment_amount'] if schedule else 0
    
    total_payment = sum(payment['payment_amount'] for payment in schedule)
    overpayment = total_payment - principal
    
    return {
        'monthly_payment': round(monthly_payment, 2),
        'total_payment': round(total_payment, 2),
        'overpayment': round(overpayment, 2)
    }
