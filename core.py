
from flask import Flask, jsonify, render_template, request
import random
import time
app = Flask(__name__,  static_url_path='')

ComputationTime = 0
UsersOnline = 0
FirstPrime = 0
CurrentData = ''
isFinished = False
isBegin = True
Check = ''
InputData = ''


def generate_number(n):
    """Generates random number for computing."""
    assert n >= 0
    l = list(range(n))
    while l[0] == 0:
        random.shuffle(l)
    return str(''.join(str(d) for d in l[:n]))


@app.route('/calculate_current')
def calculate():
    """Return current data for calculation(borders of calculation for client)."""
    print 'AJAX getJSON request to get current data and begin compute on new client'
    global isBegin, Check, CurrentData, isFinished, ComputationTime, InputData
    if isBegin:
        ComputationTime = time.time()
        if InputData != '':
            first = InputData
        else:
            first = generate_number(200)
        Check = first
        print 'First number send: ', first
        second = str(int(first) + 5)
        CurrentData = second
        isBegin = False
    else:
        first = CurrentData
        second = str(int(first) + 5)
        print 'Number send: ', first
    if isFinished:
        first = str(-1)
        second = str(-1)
    return jsonify(first_border=first, second_border=second)


@app.route('/online')
def online():
    """Returns number of online clients."""
    global UsersOnline
    print 'AJAX request to get online user count; users online now: ', UsersOnline
    return jsonify(result=UsersOnline)


@app.route('/users_online')
def users_online():
    """Renders page, that displaying number of online clients."""
    return render_template('online.html')


@app.route('/watch_worker', methods=['POST'])
def watch_worker():
    """Watch current worker state."""
    received_data = request.json
    global CurrentData, isFinished, ComputationTime, Check, FirstPrime, UsersOnline
    if isFinished:
        return jsonify(first_border='-1', second_border='-1')
    if received_data == 0:
        print 'AJAX POST current computation data on worker: ', CurrentData
        CurrentData = str(int(CurrentData) + 5)
        print 'AJAX POST new current computation data send: ', CurrentData
    else:
        isFinished = True
        FirstPrime = received_data
        print 'AJAX POST computation data received from worker: ', received_data
        print '--- %s seconds ---' % (time.time() - ComputationTime)
        print '--- Difference between first prime and begin data: %s ---' % (int(FirstPrime) - int(Check))
    return jsonify(first_border=CurrentData, second_border=str(int(CurrentData)+5))


@app.route('/', methods=['GET', 'POST'])
def index():
    """Renders main page. Case work is finished returns alert message."""
    global isFinished
    if isFinished:
        return 'Computation is finished. Nothing to do.'
    return render_template('index.html')


@app.route('/mark_online', methods=['POST'])
def mark_online():
    """Marks client online."""
    user_id = request.remote_addr
    # mark user, before worker started
    global UsersOnline
    UsersOnline += 1
    print 'AJAX POST client registered: ', user_id
    return jsonify(result=user_id)


@app.route('/mark_offline', methods=['POST'])
def mark_offline():
    """Marks client offline."""
    user_id = request.remote_addr
    global UsersOnline
    if UsersOnline != 0:
        UsersOnline -= 1
        print 'AJAX POST client gone offline: ', user_id
    return jsonify(result=user_id)


@app.route('/input_custom_data')
def custom_data():
    return render_template('input_custom_data.html')


@app.route('/custom_data')
def custom_data_try():
    data = request.args.get('a', 0, type=str)
    global InputData
    try:
        data_test = int(data)
    except ValueError:
        print 'Value Error: input data is not integer.'
        return jsonify(result=0)
    InputData = str(data_test)
    print 'Custom data input: ', InputData
    return jsonify(result=InputData)


@app.route('/get_p')
def get_p():
    global FirstPrime
    return jsonify(result=FirstPrime)


if __name__ == "__main__":
    app.run(host='0.0.0.0')  # making server visible across local network for test purposes
