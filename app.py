from flask import Flask, render_template, request
from bankInterest import BankInterest

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def calc():
    payments = []
    overpayment = 0.0
    mp = 0.0
    if request.method == 'POST':
        date_registration = request.form.get('date_registration')
        percent = float(request.form.get('credit_percent'))  # запрос к данным формы
        size = float(request.form.get('credit_size'))
        term = int(request.form.get('credit_term'))
        repayment_procedure = request.form.get('repayment_procedure')
        calculator = BankInterest(size, term, percent, date_registration)
        if repayment_procedure == 'diff':
            payments, overpayment = calculator.diff_payments()
        elif repayment_procedure == 'ann':
            payments, overpayment = calculator.ann_payments()

    return render_template('calculator.html', payments=payments, overpayment=overpayment)


if __name__ == "__main__":
    app.run(debug=True)
