from flask import Flask, render_template, request
from flask_cors import CORS

app = Flask(__name__)

CORS(app)


@app.route('/')
def index():
    return render_template('first_page.html')


@app.route('/cafe')
def second_page():
    return render_template('second_page.html')


@app.route('/cafe2')
def third_page():
    return render_template('third_page_mc.html')


@app.route('/cafe3')
def third_page1():
    return render_template('third_page.html')


if __name__ == '__main__':
    app.run()
