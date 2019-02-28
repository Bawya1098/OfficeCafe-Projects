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
    cursor.execute("select vendor_id from vendor_details where  vendor_id =%(id)s",
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
    return render_template("check_box_juices.html", items=items)


def database_connect_function():
    try:
        connection = psycopg2.connect(user="admin", host="127.0.0.1", port="5432",
                                      database="officecafe")
        cursor = connection.cursor()
        cursor.execute("select available_juices from list_juices")
        record = cursor.fetchall()
        return record
    except (Exception, psycopg2.Error) as error:
        print("Error in connecting to PSQL", error)


@app.route('/submission', methods=['POST'])
def menu_list_juices():
    return database_connection_list_cold(connection, request.form)


def database_connection_list_cold(connection, user_data):
    cursor = connection.cursor()
    array = tuple(user_data.keys())
    sql_query = "update  list_juices set checkbox_yes_no = ' '"
    sql_query_yes = "update  list_juices set checkbox_yes_no = 'yes' WHERE available_juices IN %s"
    cursor.execute(sql_query)
    cursor.execute(sql_query_yes, (array,))
    connection.commit()
    cursor.close()


if __name__ == '__main__':
    app.run(debug=True)
