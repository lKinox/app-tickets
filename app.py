import random
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

tickets = []

@app.route('/')
def index():
    return render_template('index.html', tickets=tickets)

@app.route('/comprar', methods=['POST'])
def comprar():
    ticket_number = request.form['ticket']
    serial_number = str(random.randint(10000, 99999))
    ticket = ticket_number + '-' + serial_number
    tickets.append(ticket)
    return redirect('/')

@app.route('/eliminar', methods=['POST'])
def eliminar():
    ticket = request.form['ticket']
    tickets.remove(ticket)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)

