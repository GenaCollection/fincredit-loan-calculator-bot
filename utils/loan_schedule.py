"""Построение графика платежей по сохранённому кредиту."""
from datetime import datetime
from typing import Any, Dict, List, Optional

from database.models import ExtraPayment, ExtraPaymentType, Loan, PaymentType, ReductionType
from utils.calculations import (
    calculate_annuity_schedule,
    calculate_annuity_schedule_with_extras,
    calculate_differentiated_schedule,
)


def _merge_extra_rows(loan: Loan, extra_rows: Optional[List[ExtraPayment]]) -> List[Dict[str, Any]]:
    """Список {month, amount} для calculate_annuity_schedule_with_extras."""
    extra_map: Dict[int, float] = {}
    if loan.has_extra_payments and (loan.extra_payment_amount or 0) > 0:
        for m in range(1, loan.months + 1):
            extra_map[m] = extra_map.get(m, 0.0) + float(loan.extra_payment_amount)
    if extra_rows:
        for ex in extra_rows:
            if ex.extra_type == ExtraPaymentType.ONE_TIME:
                extra_map[ex.payment_month] = extra_map.get(ex.payment_month, 0.0) + float(ex.amount)
    if not extra_map:
        return []
    return [{"month": m, "amount": amt} for m, amt in sorted(extra_map.items())]


def build_schedule_for_loan(loan: Loan, extra_rows: Optional[List[ExtraPayment]] = None) -> List[Dict[str, Any]]:
    """
    Возвращает список строк графика (ключи как в utils.calculations).
    Дифференцированный кредит без учёта разовых досрочек из БД (только страховка).
    """
    start = loan.start_date or datetime.now()
    p, r, m = float(loan.principal), float(loan.annual_rate), int(loan.months)
    ins = float(loan.insurance_monthly or 0.0) if loan.has_insurance else 0.0

    if loan.payment_type == PaymentType.DIFFERENTIATED:
        sch = calculate_differentiated_schedule(p, r, m, start)
        for row in sch:
            row["payment_amount"] = round(row["payment_amount"] + ins, 2)
        return sch

    merged = _merge_extra_rows(loan, extra_rows)
    red = "payment" if loan.reduction_type == ReductionType.PAYMENT else "term"

    if merged:
        schedule, _ = calculate_annuity_schedule_with_extras(
            principal=p,
            annual_rate=r,
            months=m,
            start_date=start,
            extra_payments=merged,
            reduction_type=red,
            insurance_monthly=ins,
            use_exact_days=False,
        )
        return schedule

    if ins > 0:
        schedule, _ = calculate_annuity_schedule_with_extras(
            p,
            r,
            m,
            start_date=start,
            extra_payments=None,
            reduction_type="term",
            insurance_monthly=ins,
            use_exact_days=False,
        )
        return schedule

    return calculate_annuity_schedule(p, r, m, start)


def refresh_loan_cached_totals(session, loan: Loan, schedule: List[Dict[str, Any]]) -> None:
    """Обновляет агрегаты кредита по графику."""
    if not schedule:
        return
    total = sum(float(row["payment_amount"]) for row in schedule)
    loan.monthly_payment = float(schedule[0]["payment_amount"])
    loan.total_payment = round(total, 2)
    loan.total_overpayment = round(total - float(loan.principal), 2)
    loan.actual_months = len(schedule)
