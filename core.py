
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
    global isBegin, Check, CurrentData, isFinished, ComputationTime
    if isBegin:
        ComputationTime = time.time()
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
    global CurrentData, isFinished, ComputationTime, Check, FirstPrime
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


if __name__ == "__main__":
    app.run(host='0.0.0.0')  # making server visible across local network for tests
