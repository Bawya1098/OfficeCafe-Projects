import psycopg2
from flask import Flask, render_template, request
from flask_cors import CORS
from modules.post_details import post_data


app = Flask(__name__)
CORS(app)
connection = psycopg2.connect("dbname = officecafe  user=admin")


@app.route('/')
def index():
    return render_template('cart_practice.html')


@app.route('/post-data', methods=['POST'])
def get_data():
    post_data(connection, request.form)
    return render_template('display.html', shared=request.form)


if __name__ == '__main__':
    app.run()
