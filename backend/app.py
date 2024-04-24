from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="1234",
    database="pricecal"
)
cursor = db.cursor()

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        factory = request.form['factory'].lower()
        distance = float(request.form['distance'])
        petroPriceToday = float(request.form['petro_price'])
        day = int(request.form['day'])

        cursor.execute("SELECT price FROM price_tiers WHERE distance <= %s ORDER BY distance DESC LIMIT 1", (distance,))
        basePrice_result = cursor.fetchone()
        if basePrice_result:
            basePrice = basePrice_result[0]
        else:
            cursor.execute("SELECT max_distance FROM fix_cost")
            maxDistance = cursor.fetchone()[0]
            if distance > maxDistance:
                distance = maxDistance
            cursor.execute("SELECT price FROM price_tiers WHERE distance = %s", (distance,))
            basePrice = cursor.fetchone()[0]

        cursor.execute("SELECT price FROM petro_tiers WHERE %s BETWEEN range_start AND range_end", (petroPriceToday,))
        petroPrice_result = cursor.fetchone()
        if petroPrice_result:
            petroPrice = petroPrice_result[0]
        else:
            cursor.execute("SELECT max_petro_tire FROM fix_cost")
            petroPrice = cursor.fetchone()[0]

        cursor.execute("SELECT * FROM fix_cost")
        fix_cost_data = cursor.fetchone()

        yardCost = fix_cost_data[1]
        portCost = fix_cost_data[2]
        factoryCost = fix_cost_data[3]
        perDayCost = fix_cost_data[4]
        maxPetroTire = fix_cost_data[5]
        maxDistance = fix_cost_data[6]

        standardPrice = (
            basePrice * petroPrice +
            yardCost +
            portCost +
            factoryCost +
            ((day - 1) * perDayCost)
        )

        low_prices = []
        standard_prices = []
        low_price = calculate_base_price(cursor, distance) + yardCost + portCost
        cal_price = calculate_standard_price(cursor, distance, calculate_petro_price(cursor, petroPriceToday), day)
        mean_price = (low_price + cal_price) / 2
        cursor.execute("SELECT * FROM petro_tiers")
        petro_tiers_data = cursor.fetchall()
        for petro_row in petro_tiers_data:
            cal_price_range = calculate_standard_price(cursor, distance, calculate_petro_price(cursor, (petro_row[0] + petro_row[1]) / 2), day)
            standard_prices.append(round(cal_price_range, -2))
            petro_price_range = calculate_petro_price(cursor, (petro_row[0] + petro_row[1]) / 2)
            cal_price_range = calculate_base_price(cursor, distance) * petro_price_range + yardCost + portCost
            low_prices.append(round(cal_price_range, -2))
        mean_prices = calculate_mean_price(standard_prices, low_prices)

        cursor.execute("INSERT INTO transport_data (factory, distance, petro_price, day, price) VALUES (%s, %s, %s, %s, %s)", (factory, distance, petroPriceToday, day, standardPrice))
        db.commit()

        return render_template(
            'result.html',
            factory=factory,
            distance=distance,
            day=day,
            petro_price=petroPriceToday,
            standard_price=standardPrice,
            low_prices=low_prices,
            standard_prices=standard_prices,
            mean_prices=mean_prices,
            low_price=round(low_price, -2),
            cal_price=round(cal_price, -2),
            mean_price=round(mean_price, -2),
            petro_tiers_data=petro_tiers_data
        )
    else:
        return render_template('index.html')

@app.route('/history')
def history():
    cursor.execute("SELECT * FROM transport_data")
    data = cursor.fetchall()

    cal_price_list = []
    for record in data:
        distance = record[2]
        petro_price = record[3]
        day = record[4]
        cal_price = calculate_standard_price(cursor, distance, calculate_petro_price(cursor, petro_price), day)
        cal_price_list.append(cal_price)

    return render_template('history.html', transport_data=data, cal_price_list=cal_price_list)

def calculate_mean_price(standard_prices, low_prices):
    mean_prices = []
    for standard_price, low_price in zip(standard_prices, low_prices):
        if standard_price < low_price:
            mean_price = standard_price
        else:
            mean_price = (standard_price + low_price) / 2
        mean_prices.append(mean_price)
    return mean_prices

def calculate_base_price(cursor, distance):
    cursor.execute("SELECT price FROM price_tiers WHERE distance <= %s ORDER BY distance DESC LIMIT 1", (distance,))
    basePrice_result = cursor.fetchone()
    if basePrice_result:
        basePrice = basePrice_result[0]
    else:
        cursor.execute("SELECT max_distance FROM fix_cost")
        maxDistance = cursor.fetchone()[0]
        if distance > maxDistance:
            distance = maxDistance
        cursor.execute("SELECT price FROM price_tiers WHERE distance = %s", (distance,))
        basePrice = cursor.fetchone()[0]
    return basePrice * distance

def calculate_petro_price(cursor, petro):
    cursor.execute("SELECT price FROM petro_tiers WHERE %s BETWEEN range_start AND range_end", (petro,))
    petroPrice_result = cursor.fetchone()
    if petroPrice_result:
        petroPrice = petroPrice_result[0]
    else:
        cursor.execute("SELECT max_petro_tire FROM fix_cost")
        petroPrice = cursor.fetchone()[0]
    return petroPrice

def calculate_standard_price(cursor, distance, petro_price, day):
    cursor.execute("SELECT * FROM fix_cost")
    fix_cost_data = cursor.fetchone()
    yardCost = fix_cost_data[1]
    portCost = fix_cost_data[2]
    factoryCost = fix_cost_data[3]
    perDayCost = fix_cost_data[4]

    standard_price = (
        calculate_base_price(cursor, distance) * petro_price +
        yardCost +
        portCost +
        factoryCost +
        ((day - 1) * perDayCost)
    )
    return standard_price

if __name__ == '__main__':
    app.run(debug=True)
