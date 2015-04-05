
from flask import Flask, jsonify, render_template, request
app = Flask(__name__,  static_url_path='')

UsersOnline = 0


@app.route('/_add_numbers')
def add_numbers():
    """Add two numbers server side, ridiculous but well..."""
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    return jsonify(result=a + b + 100)


@app.route('/online')
def online():
    # count online users
    return jsonify(result=UsersOnline)


@app.route('/calculate_current')
def calculate():
    # data to worker
    return jsonify(result=15000000)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/print', methods=['POST'])
def receive_data():
    received_data = request.json
    print 'AJAX POST data received from worker'
    print received_data
    return jsonify(result=received_data)


@app.before_request
def mark_user():
    global UsersOnline
    UsersOnline += 1
    print UsersOnline

if __name__ == "__main__":
    app.run()


