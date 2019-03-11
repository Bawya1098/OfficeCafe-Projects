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
def employee_choice():
    return render_template('Employee_choice.html')


@app.route('/cafe2')
def cold_items():
    rows = database_hot()
    items = []
    for row in rows:
        items.append(row[0])
    columns = database_cold_items()
    lists = []
    for column in columns:
        lists.append(column[0])
    return render_template("Juice_world.html", items=items, lists=lists)


def database_hot():
    cursor = connection.cursor()
    query = "select items_name from items  where sold_by=2 and is_available='true'"
    cursor.execute(query)
    record = cursor.fetchall()
    return record


def database_cold_items():
    cursor = connection.cursor()
    cursor.execute("select items_name from items where is_available='true' and sold_by=1 ")
    result = cursor.fetchall()
    return result


@app.route('/cafe3')
def hot_items():
    rows = database_cold()
    items = []
    for row in rows:
        items.append(row[0])
    columns = database_hot_items()
    lists = []
    for column in columns:
        lists.append(column[0])
    return render_template("Madras_cafe.html", items=items, lists=lists)


def database_cold():
    cursor = connection.cursor()
    query = "select items_name from items  where sold_by=1 and is_available='true'"
    cursor.execute(query)
    record = cursor.fetchall()
    return record


def database_hot_items():
    cursor = connection.cursor()
    cursor.execute("select items_name from items where is_available='true' and sold_by=2 ")
    result = cursor.fetchall()
    return result


@app.route('/vendor')
def login_page():
    return render_template('types_vendor.html')


@app.route('/vendor-choice')
def login_choice():
    return render_template('vendor login.html')


@app.route('/vendor-login', methods=['POST'])
def vendor_login():
    return validate_data(connection, request.form)


def validate_data(connection, user_data):
    cursor = connection.cursor()
    cursor.execute("select * from vendor_details where  vendor_id =%(id)s  and shop=1 ",
                   {'id': user_data['id']})

    returned_rows = cursor.fetchall()
    cursor.close()
    if len(returned_rows) == 0:
        return render_template('types_vendor.html')
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
    cursor.execute("select items_name from items where sold_by=1")
    record = cursor.fetchall()
    return record


@app.route('/submission', methods=['POST'])
def menu_list_juices():
    row = database_connection_list_cold(connection, request.form)
    return render_template('Welcome.html', items=row)


def database_connection_list_cold(connection, user_data):
    cursor = connection.cursor()
    array = tuple(user_data.keys())
    sql_query = "update items set is_available='false' where sold_by=1"
    sql_query_yes = "update items set is_available = 'true' WHERE  items_name  IN %s "
    cursor.execute(sql_query)
    cursor.execute(sql_query_yes, (array,))
    connection.commit()
    cursor.close()
    return sql_query_yes


# vendor-login for madras cafe#

@app.route('/vendor-choice')
def login_choice2():
    return render_template('vendor login.html')


@app.route('/vendor-choice', methods=['POST'])
def vendor_login2():
    return validate_data2(connection, request.form)


def validate_data2(connection, user_data):
    cursor = connection.cursor()
    cursor.execute("select * from vendor_details where  vendor_id =%(id)s and shop=2 ",
                   {'id': user_data['id']})
    cursor.fetchall()
    cursor.close()
    return render_template('vendor choice2.html')


@app.route('/vendor-mc', methods=['POST'])
def hot():
    list = database_connect_function_2()
    items = []
    for row in list:
        items.append(row[0])
    return render_template("availability_hot_beverages.html", items=items)


def database_connect_function_2():
    cursor = connection.cursor()
    cursor.execute("select items_name from items where sold_by=2")
    record = cursor.fetchall()
    return record


@app.route('/submission1', methods=['POST'])
def menu_list_hot():
    row = database_connection_list_hot(connection, request.form)
    return render_template('Welcome.html', items=row)


def database_connection_list_hot(connection, user_data):
    cursor = connection.cursor()
    array = tuple(user_data.keys())
    sql_query = "update items set is_available='false' where sold_by=2"
    sql_query_yes = "update  items set is_available = 'true' WHERE  items_name IN  %s "
    cursor.execute(sql_query)
    cursor.execute(sql_query_yes, (array,))
    connection.commit()
    cursor.close()
    return sql_query_yes


@app.route('/hot-item', methods=['POST'])
def update_item():
    update(connection, request.form)
    return render_template('Welcome.html')


def update(connection, user_data):
    values = list(user_data.values())
    employee_value = values[-1]
    values.remove(values[-1])
    item_key = list(user_data.keys())
    item_key.remove(item_key[-1])

    for id in list(item_key):
        quantity = user_data[id]
        if int(quantity) > 0:
            cursor = connection.cursor()
            update_details = "insert into cart(items_id,employee_id,quantity) select items_id,{},{} from items where items_id = {}".format(
                employee_value, quantity, id)

            cursor.execute(update_details)
            connection.commit()
            cursor.close()
        else:
            print(0)


if __name__ == '__main__':
    app.run(debug=True)
