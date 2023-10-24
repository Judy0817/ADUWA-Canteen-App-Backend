from flask import Flask, request, jsonify
import mysql.connector
from config import MYSQL_CONFIG
from flask_login import current_user
from flask import Flask, session
import time



app = Flask(__name__)

# Configure MySQL database connection
db = mysql.connector.connect(**MYSQL_CONFIG)

@app.route('/insert_food', methods=['GET'])
def insert_record():
    # data = request.get_json()
    # title = data.get('title')
    name = request.args.get('name', type=str)
    description = request.args.get('description', type=str)
    price = request.args.get('price', type=float)
    # description = data.get('description')
    mycursor = db.cursor()
    sql = "INSERT INTO FOOD_TABLE (NAME,PRICE, DESCRIPTION) VALUES (%s, %s,%s)"
    val = (name,price,description)
    mycursor.execute(sql, val)
    db.commit()
    return "Record inserted."

@app.route('/retrieve_food', methods=['GET'])
def retrieve_data():
    try:
        mycursor = db.cursor()
        sql = "SELECT * FROM FOOD_TABLE"
        mycursor.execute(sql)
        data = mycursor.fetchall()
        result = [{'id': row[0], 'name': row[1], 'price':row[2] ,'description': row[3]} for row in data]
        mycursor.close()
        return jsonify(result)

    except mysql.connector.Error as error:
        return jsonify({'error': f"Database error: {error}"}), 500


@app.route('/delete_food/<int:id>', methods=['GET'])
def delete_record(id):
    try:
        mycursor = db.cursor()
        sql = "DELETE FROM FOOD_TABLE WHERE ID = %s"
        val = (id,)
        mycursor.execute(sql, val)
        db.commit()
        if mycursor.rowcount > 0:
            return jsonify({'message': f'Record with ID {id} deleted successfully'})
        else:
            return jsonify({'message': f'Record with ID {id} not found'}), 404

    except mysql.connector.Error as error:
        return jsonify({'error': f"Database error: {error}"}), 500
    

@app.route('/update_food/<int:id>', methods=['GET'])
def update_record(id):
    try:
        # Get the updated title and description from the request
        title = request.args.get('name', type=str)
        description = request.args.get('description', type=str)
        price = request.args.get('price', type=float)

        mycursor = db.cursor()
        sql = "UPDATE FOOD_TABLE SET NAME = %s, DESCRIPTION = %s, PRICE = %s WHERE ID = %s"
        val = (title, description,price,id)
        mycursor.execute(sql, val)
        db.commit()

        if mycursor.rowcount > 0:
            return jsonify({'message': f'Record with ID {id} updated successfully'})
        else:
            return jsonify({'message': f'Record with ID {id} not found'}), 404

    except mysql.connector.Error as error:
        return jsonify({'error': f"Database error: {error}"}), 500

total_price = 0.0

@app.route('/add_to_cart', methods=['GET'])
def add_to_cart():
    global total_price

    try:
        item_price = float(request.args.get('price'))

        if item_price is not None:
            total_price += item_price
            return jsonify({'message': 'Item added to cart successfully'})
        else:
            return jsonify({'error': 'Invalid item data'}), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/store_user_data', methods=['GET'])
def insert_user():
    # data = request.get_json()
    # title = data.get('title')
    username = request.args.get('username', type=str)
    email = request.args.get('email', type=str)

    # description = data.get('description')
    mycursor = db.cursor()
    sql = "INSERT INTO users (username, email) VALUES (%s, %s)"
    val = (username,email)
    mycursor.execute(sql, val)
    db.commit()
    return "User inserted."

@app.route('/retrieve_username', methods=['GET'])
def retrieve_username():
    try:
        email = request.args.get('email')  # Get the email from the query parameters
        if email is not None:
            mycursor = db.cursor()
            sql = "SELECT username FROM users WHERE email = %s"  # Modify the SQL query to filter by email
            mycursor.execute(sql, (email,))
            row = mycursor.fetchone()
            if row is not None:
                username = row[0]
                # Remove double quotation marks from the username
                username = username.replace('"', '')
                mycursor.close()
                return jsonify(username)
            else:
                return jsonify({'error': 'User not found for the provided email'}), 404
        else:
            return jsonify({'error': 'Missing email parameter'}), 400

    except mysql.connector.Error as error:
        return jsonify({'error': f"Database error: {error}"}), 500

@app.route('/insert_bucket', methods=['GET'])
def insert_bucket():
    Username = request.args.get('Username', type=str,default=None)
    FoodName = request.args.get('FoodName', type=str)
    Price = request.args.get('Price', type=float)
    Quantity=request.args.get('Quantity', type=int,default=None)
    SubTotal = request.args.get('SubTotal', type=float,default=None)
    Status = "Pending"
    mycursor = db.cursor()
    sql = "INSERT INTO Bucket (Username,FoodName,Price,Quantity,SubTotal,Status) VALUES (%s, %s,%s,%s,%s,%s)"
    val = (Username,FoodName,Price,Quantity,SubTotal,Status)
    mycursor.execute(sql, val)
    db.commit()
    return "Record inserted."


@app.route('/retrieve_bucket', methods=['GET'])
def retrieve_bucket():
    try:
        username = request.args.get('Username')
        mycursor = db.cursor()
        sql = "SELECT * FROM Bucket WHERE Status = 'Pending' AND Username = %s"
        mycursor.execute(sql, (username,))
        data = mycursor.fetchall()
        result = [{'OrderID': row[0], 'Username': row[1], 'FoodName':row[2] ,'Price': row[3],'Quantity': row[4],'SubTotal': row[5],'Status': row[6]} for row in data]
        mycursor.close()
        return jsonify(result)

    except mysql.connector.Error as error:
        return jsonify({'error': f"Database error: {error}"}), 500
    

@app.route('/update_bucket/<int:OrderID>', methods=['GET'])
def update_bucket(OrderID):
    try:
        # Get the updated title and description from the request
        Quantity = request.args.get('Quantity', type=str)
        SubTotal = request.args.get('SubTotal', type=float)

        mycursor = db.cursor()
        sql = "UPDATE Bucket SET Quantity = %s, SubTotal = %s WHERE OrderID = %s"
        val = (Quantity, SubTotal,OrderID)
        mycursor.execute(sql, val)
        db.commit()

        if mycursor.rowcount > 0:
            return jsonify({'message': f'Record with ID {OrderID} updated successfully'})
        else:
            return jsonify({'message': f'Record with ID {OrderID} not found'}), 404

    except mysql.connector.Error as error:
        return jsonify({'error': f"Database error: {error}"}), 500
    

@app.route('/get_total_price2', methods=['GET'])
def get_total_price2():
    try:

        mycursor = db.cursor()
        sql = "SELECT SUM(SubTotal) AS total_price FROM Bucket"
        mycursor.execute(sql)
        
        # Fetch the result
        result = mycursor.fetchone()
        total_price = result[0] if result else 0.0
        mycursor.close()
        return jsonify({"total_price": total_price})
    except Exception as e:
        return jsonify({"error": str(e)})
    


@app.route('/delete_bucket/<int:id>', methods=['GET'])
def delete_bucket(id):
    try:
        mycursor = db.cursor()
        sql = "DELETE FROM Bucket WHERE OrderID = %s"
        val = (id,)
        mycursor.execute(sql, val)
        db.commit()
        if mycursor.rowcount > 0:
            return jsonify({'message': f'Record with ID {id} deleted successfully'})
        else:
            return jsonify({'message': f'Record with ID {id} not found'}), 404

    except mysql.connector.Error as error:
        return jsonify({'error': f"Database error: {error}"}), 500




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9090)


while True:
    time.sleep(2)
