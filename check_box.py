import psycopg2
from flask import Flask, render_template, request

from app import connection

app = Flask(__name__)


@app.route('/')
def juices():
    list = database_connect_function()
    items = []
    for row in list:
        items.append(row[0])
    return render_template("check_box_juices.html", items=items)


@app.route('/submission', methods=['POST'])
def menu_list_juices():
    return database_connection_list_cold(connection, request.form)


def database_connection_list_cold(connection, user_data):
    cursor = connection.cursor()
    array = tuple(user_data.keys())
    sql_query = "update  list_juces set checkbox_yes_no = ' '"
    sql_query_yes = "update  list_juces set checkbox_yes_no = 'yes' WHERE available_juices IN %s"
    print(cursor.mogrify(sql_query, (array,)))
    cursor.execute(sql_query)
    cursor.execute(sql_query_yes, (array,))
    connection.commit()
    cursor.close()


def database_connect_function():
    try:
        connection = psycopg2.connect(user="admin", host="127.0.0.1", port="5432",
                                      database="officecafe")
        cursor = connection.cursor()
        cursor.execute("select available_juices from list_juces")
        record = cursor.fetchall()
        return record
    except (Exception, psycopg2.Error) as error:
        print("Error in connecting to PSQL", error)


# def database_connect_function1(connection,user_data):
#     try:
#         cursor = connection.cursor()
#         cursor.execute("select available_juices  from list_juces where available_juices ='yes' ")
#         record = cursor.fetchall()
#         return record
#
#     except (Exception, psycopg2.Error) as error:
#         print("Error in connecting to PSQL", error)
#

if __name__ == '__main__':
    app.run()
