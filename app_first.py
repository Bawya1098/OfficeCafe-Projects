import psycopg2
from flask import Flask, render_template, request
from flask_cors import CORS
from modules.post_details import post_data

app = Flask(__name__)
CORS(app)
connection = psycopg2.connect("dbname=officecafe user=admin")


@app.route('/')
def index():
    return render_template('first_page.html')


# @app.route('/first_page.html')
# def get_data():
#     return render_template('second_page.html')


if __name__ == '__main__':
    app.run()
