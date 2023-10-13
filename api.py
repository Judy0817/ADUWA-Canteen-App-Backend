from flask import Flask, request, jsonify
import mysql.connector
from config import MYSQL_CONFIG

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



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9090)
