
from flask import Flask, jsonify, render_template, request
app = Flask(__name__,  static_url_path='')

Number = 120
UsersOnline = 0
CurrentUsers = []
FirstPrime = 0
BeginCompute = True
EndOfCurrentPiece = Number + 5
isFinished = False
Result = None


@app.route('/online')
def online():
    """Returns number of online clients."""
    global UsersOnline
    print 'AJAX request to get online user count'
    return jsonify(result=UsersOnline)


@app.route('/calculate_current')
def calculate():
    """Return borders of calculation."""
    print 'AJAX request to get current data and begin compute'
    global UsersOnline
    global BeginCompute
    global Number
    if BeginCompute:
        first = Number
        second = -1
        BeginCompute = False
    if not BeginCompute:
        first = EndOfCurrentPiece
        second = EndOfCurrentPiece + 5
    return jsonify(first_border=first, second_border=second)


@app.route('/', methods=['GET', 'POST'])
def index():
    """Renders main page."""
    global isFinished
    if isFinished:
        return 'Computation is finished. Nothing to do.'
    return render_template('index.html')


@app.route('/print', methods=['POST'])
def receive_data():
    """Return data of computation."""
    received_data = request.json
    # worker made his job so decrement online users
    global UsersOnline
    UsersOnline -= 1
    print 'AJAX POST data received from worker: ', received_data
    return jsonify(result=received_data)


@app.route('/watch_worker', methods=['POST'])
def watch_worker():
    """Watch current worker state."""
    received_data = request.json
    global CurrentData
    CurrentData = received_data
    print 'AJAX POST current computation data received from worker: ', received_data
    return jsonify(result=received_data)


@app.route('/mark_online', methods=['POST'])
def mark_online():
    """Marks client online."""
    user_id = request.remote_addr
    # mark user, before worker started
    global CurrentUsers
    CurrentUsers.append(user_id)
    global UsersOnline
    UsersOnline += 1
    print 'AJAX POST client registered: ', user_id
    return jsonify(result=user_id)


@app.before_request
def check_finish():
    """Checked if finished."""
    global isFinished
    global Result
    if isFinished:
        print 'Computation is finished. Result: ', Result

if __name__ == "__main__":
    app.run()


