from flask import Flask, render_template, request, redirect, url_for
from datetime import date
from db.connection import DataBase
from db.interfaces import Ticket

app = Flask(__name__)

db = DataBase()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/customer', methods=['GET', 'POST'])
def customer_login():

    if request.method == 'POST':
        customer_id = request.form.get('customer_id')
        if customer_id:
            return redirect(url_for('customer_overview', customer_id=customer_id))

    return render_template('customer_login.html')

@app.route('/customer/overview')
def customer_overview():

    customer_id = request.args.get('customer_id')

    if not customer_id:
        return redirect(url_for('customer_login'))

    tickets = db.get_tickets_by_customer(customer_id)

    return render_template('customer_template.html', tickets=tickets)

@app.route('/employee')
def employee_overview():
    tickets_none = db.get_tickets_by_priority(None)
    tickets_p1   = db.get_tickets_by_priority(1)
    tickets_p2   = db.get_tickets_by_priority(2)
    tickets_p3   = db.get_tickets_by_priority(3)

    return render_template(
        'employee_template.html',
        tickets_none=tickets_none,
        tickets_p1=tickets_p1,
        tickets_p2=tickets_p2,
        tickets_p3=tickets_p3
    )

@app.route('/tickets/new', methods=['GET', 'POST'])
def create_ticket():
    if request.method == 'POST':
        customer_id = int(request.form.get('customer_id', 0))
        thema = request.form.get('thema', '')
        beschreibung = request.form.get('beschreibung', '')
        firma = request.form.get('firma', '')

        ticket = Ticket(
            customer_id=customer_id,
            thema=thema,
            beschreibung=beschreibung,
            firma=firma,
            created_at=date.today()
        )

        db.add_ticket(ticket)

        return redirect(url_for('ticket_created'))

    # GET: Formular anzeigen
    return render_template('create_ticket.html')

@app.route('/tickets/created')
def ticket_created():
    return "<h2>Ticket erfolgreich erstellt!</h2><a href='/tickets/new'>Neues Ticket erstellen</a>"


@app.route('/employee/ticket/<int:ticket_id>', methods=['GET', 'POST'])
def edit_ticket(ticket_id):

    if request.method == 'POST':
        related_ticket_id = request.form.get('related_ticket_id')
        status = request.form.get('status')
        prioritaet = request.form.get('prioritaet')
        mitarbeiter_notizen = request.form.get('mitarbeiter_notizen')


        employee_id = 1


        db.update_ticket_by_employee(
            ticket_id=ticket_id,
            employee_id=employee_id,
            status=status,
            prioritaet=int(prioritaet) if prioritaet else None,
            mitarbeiter_notizen=mitarbeiter_notizen,
            related_ticket_id=related_ticket_id
        )

        return redirect(url_for('employee_overview'))


    ticket = db.get_ticket_by_id(ticket_id)

    
    customer = db.get_customer_by_id(ticket[1])  # CustomerId ist Feld 1

    return render_template('edit_ticket.html', ticket=ticket, customer=customer)

if __name__ == '__main__':
    app.run(debug=True)