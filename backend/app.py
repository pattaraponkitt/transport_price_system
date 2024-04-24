from flask import Flask, jsonify, request
import mysql.connector
# Import the necessary functions from your original app.py file

app = Flask(__name__)

# Add your database connection and helper functions here

@app.route('/api/calculate', methods=['POST'])
def calculate_price():
    data = request.get_json()
    factory = data['factory'].lower()
    distance = float(data['distance'])
    petro_price = float(data['petroPrice'])
    day = int(data['day'])

    # Perform calculations and retrieve the necessary data
    result = {
        'factory': factory,
        'distance': distance,
        'petroPrice': petro_price,
        'day': day,
        'lowPrice': low_price,
        'calculatedPrice': cal_price,
        'canUseRate': can_use_rate,
        'petroTiersData': petro_tiers_data,
        'lowPrices': low_prices,
        'meanPrices': mean_prices,
        'standardPrices': standard_prices,
    }

    # Save the data to the database
    cursor.execute("INSERT INTO transport_data (factory, distance, petro_price, day, price) VALUES (%s, %s, %s, %s, %s)", (factory, distance, petro_price, day, cal_price))
    db.commit()

    return jsonify(result)

@app.route('/api/history', methods=['GET'])
def get_history():
    cursor.execute("SELECT * FROM transport_data")
    data = cursor.fetchall()

    transport_data = []
    for record in data:
        distance = record[2]
        petro_price = record[3]
        day = record[4]
        cal_price = calculate_standard_price(cursor, distance, calculate_petro_price(cursor, petro_price), day)
        transport_data.append([
            record[0],  # Record ID
            record[1],  # Factory name
            record[2],  # Distance
            record[3],  # Petro price
            cal_price,  # Calculated price
            record[5],  # Date and time
            record[4],  # Working day
        ])

    return jsonify(transport_data)

if __name__ == '__main__':
    app.run()