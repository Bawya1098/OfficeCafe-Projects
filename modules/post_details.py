def post_data(connection, user_data):
    cursor = connection.cursor()
    cursor.execute("""insert into orders(employee_id,cart_items) values(%s,%s);""",
                   (user_data['employee_id'], user_data['cart_items']))
    connection.commit()
    cursor.close()
