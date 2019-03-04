import psycopg2
from flask import Flask, request, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
connection = psycopg2.connect("dbname = officecafe user=admin")

app = Flask(__name__)

CORS(app)


@app.route('/')
def index():
    return render_template('Welcome.html')


@app.route('/cafe')
def second_page():
    return render_template('Employee_choice.html')


@app.route('/cafe2')
def third_page():
    return render_template('Madras_cafe.html')


@app.route('/cafe3')
def third_page1():
    return render_template('Juice_world.html')


@app.route('/vendor')
def login_page():
    return render_template('vendor login.html')


@app.route('/vendor-menu', methods=['POST'])
def vendor_login():
    return validate_data(connection, request.form)


def validate_data(connection, user_data):
    cursor = connection.cursor()
    cursor.execute("select * from vendor_details where  vendor_id =%(id)s and shop =1 or shop = 2 ",
                   {'id': user_data['id']})
    returned_rows = cursor.fetchall()
    cursor.close()
    if len(returned_rows) == 0:
        return render_template('vendor login .html')
    else:
        return render_template('vendor choice.html')


@app.route('/vendor-jw', methods=['POST'])
def juices():
    list = database_connect_function()
    items = []
    for row in list:
        items.append(row[0])
    return render_template("available_cold_beverages.html", items=items)


def database_connect_function():
    cursor = connection.cursor()
    cursor.execute("select items_name from items ")
    record = cursor.fetchall()
    return record


@app.route('/submission', methods=['POST'])
def menu_list_juices():
    return database_connection_list_cold(connection, request.form)


def database_connection_list_cold(connection, user_data):
    cursor = connection.cursor()
    array = tuple(user_data.keys())
    sql_query_yes = "update  items set is_available = 't' WHERE  items_name = %s"
    cursor.execute(sql_query_yes, array)
    connection.commit()
    cursor.close()


if __name__ == '__main__':
    app.run(debug=True)
