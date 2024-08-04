from datetime import datetime, date, timedelta
import calendar


class BankInterest(object):

    def __init__(self, sum, period, percent, reg_date):
        self.reg_date = datetime.strptime(reg_date, "%Y-%m-%d").date()
        self.sum = sum
        self.period = period
        self.percent = percent  # процентная ставка

    # Дифференциальная формула
    def diff_payments(self):
        payments = []  # график платежей |дата платежа|платёж|проценты|тело|остаток|
        amount = round(self.sum, 2)  # сумма кредита
        amortization = round(amount / self.period, 2)  # величина платежа по погашению кредита
        i = self.percent / 1200.0  # процентная ставка за один период
        total = 0.0
        date = self.reg_date
        overpayment = 0.0

        for m in range(self.period + 1):
            if m != 0:
                days_in_month = calendar.monthrange(date.year, date.month)[1]
                date += timedelta(days=days_in_month)
                repayment_percent = round(amount * i, 2)
                monthly_payment = round(amortization + repayment_percent, 2)  # ежемесячный платёж
                total = total + monthly_payment
                overpayment = overpayment + repayment_percent
                amount = round(amount - amortization, 2)
                if m == self.period:
                    amount = 0.0
                payments.append([date, monthly_payment, repayment_percent, amortization, amount])

        overpayment = round(overpayment, 2)
        return payments, overpayment

    # Аннуитетная формула
    def ann_payments(self):
        payments = []  # график платежей |дата платежа|платёж|проценты|тело|остаток|
        amount = round(self.sum, 2)  # сумма кредита
        i = self.percent / 1200  # процентная ставка за один период
        m = self.period
        ann_coefficient = (i * (1 + i) ** m) / ((1 + i) ** m - 1)
        monthly_payment = round(amount * ann_coefficient, 2)
        total = monthly_payment * m
        overpayment = round(total - self.sum, 2)
        date = self.reg_date

        for m in range(self.period + 1):
            if m != 0:
                days_in_month = calendar.monthrange(date.year, date.month)[1]
                date += timedelta(days=days_in_month)
                repayment_percent = round(amount * i, 2)
                amortization = round(monthly_payment - repayment_percent, 2)
                amount = round(amount - amortization, 2)
                if m == self.period:
                    amount = 0.0
                payments.append([date, monthly_payment, repayment_percent, amortization, amount])

        return payments, overpayment
