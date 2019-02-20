from flask import Flask, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return render_template('first_page.html')


# @app.route('/first_page.html')
# def get_data():
#     return render_template('second_page.html')


if __name__ == ('__main__'):
    app.run()
