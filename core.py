
from flask import Flask, jsonify, render_template, request
app = Flask(__name__,  static_url_path='')

NUMBER_TO_START = 100


@app.route('/_add_numbers')
def add_numbers():
    """Add two numbers server side, ridiculous but well..."""
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)

    return jsonify(result=a + b + 100)


@app.route('/_check_prime')
def check_number():

    result = request.args.get('result', 0, type=int)
    if result == 1:
        return jsonify(result='True')

    # return jsonify(result=a + b + 100)



@app.route('/worker')
def work():
    return render_template('worker.html')


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run()


