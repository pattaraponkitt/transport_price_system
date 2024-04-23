from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

def connect_to_database():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="1234",
        database="tran_price"
    )

def get_constants(cursor):
    cursor.execute("SELECT constant_name, constant_value FROM constants")
    return dict(cursor.fetchall())

def get_constants(cursor):
    cursor.execute("SELECT constant_name, constant_value FROM constants")
    constants = dict(cursor.fetchall())

    price_tiers = get_price_tiers(cursor)
    constants['price_tiers'] = price_tiers

    return constants


def get_price_tiers(cursor):
    cursor.execute("SELECT distance, price FROM price_tiers")
    return dict(cursor.fetchall())

def get_petro_tiers(cursor):
    cursor.execute("SELECT min_petro, max_petro, price_multiplier FROM petro_tiers")
    return dict(((min_petro, max_petro), price_multiplier) for min_petro, max_petro, price_multiplier in cursor.fetchall())

def calculate_base_price(distance, price_tiers, default_base_price=0):
    if not price_tiers:
        return distance * default_base_price

    for tier_distance, tier_price in price_tiers.items():
        if distance <= tier_distance:
            return distance * tier_price
    return distance * default_base_price


def calculate_petro_price(petro, petro_tiers, default_petro_price=0):
    if not petro_tiers:
        return default_petro_price

    for petro_range, tier_price in petro_tiers.items():
        if petro_range[0] <= petro <= petro_range[1]:
            return tier_price
    return default_petro_price


def calculate_standard_price(distance, petro_price, day, constants):
    base_price = calculate_base_price(distance, constants['price_tiers'])
    standard_price = (
        base_price * petro_price +
        constants['YARD_COST'] +
        constants['PORT_COST'] +
        constants['FACTORY_COST'] +
        ((day - 1) * constants['PER_DAY_COST'])
    )
    return standard_price

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        factory = request.form['factory'].lower()
        distance = float(request.form['distance'])
        petro_price_today = float(request.form['petro_price'])
        day = int(request.form['day'])

        db_connection = connect_to_database()
        cursor = db_connection.cursor()

        constants = get_constants(cursor)
        price_tiers = get_price_tiers(cursor)
        petro_tiers = get_petro_tiers(cursor)

        low_prices = []
        standard_prices = []
        low_price = calculate_base_price(distance, price_tiers) + constants['YARD_COST'] + constants['PORT_COST']
        cal_price = calculate_standard_price(distance, petro_price_today, day, constants)
        mean_price = (low_price + cal_price) / 2

        for petro_range, petro_price_range in petro_tiers.items():
            cal_price_range = calculate_standard_price(distance, petro_price_range, day, constants)
            standard_prices.append(round(cal_price_range, -2))

        for petro_range, petro_price_range in petro_tiers.items():
            petro_price_range = calculate_petro_price((petro_range[0] + petro_range[1]) / 2, petro_tiers)
            cal_price_range = calculate_base_price(distance, price_tiers) * petro_price_range + constants['YARD_COST'] + constants['PORT_COST']
            low_prices.append(round(cal_price_range, -2))

        mean_prices = calculate_mean_price(standard_prices, low_prices)

        db_connection.close()

        return render_template(
            'result.html',
            factory=factory,
            distance=distance,
            day=day,
            petro_price=petro_price_today,
            low_prices=low_prices,
            standard_prices=standard_prices,
            mean_prices=mean_prices,
            low_price=round(low_price, -2),
            cal_price=round(cal_price, -2),
            mean_price=round(mean_price, -2),
            PETRO_TIERS=petro_tiers
        )
    else:
        return render_template('index.html')

def calculate_mean_price(standard_prices, low_prices):
    mean_prices = []
    for standard_price, low_price in zip(standard_prices, low_prices):
        if standard_price < low_price:
            mean_price = standard_price
        else:
            mean_price = (standard_price + low_price) / 2
        mean_prices.append(mean_price)
    return mean_prices

if __name__ == '__main__':
    app.run(debug=True)
