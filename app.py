import os
import sqlite3
import requests
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'Nazarka'

db_path = os.path.abspath('instance/menu.db')


def get_menu_items():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, description, price FROM menu_items')
    items = cursor.fetchall()
    conn.close()
    return [{'id': id, 'name': name, 'description': description, 'price': price} for id, name, description, price in items]

def add_menu_item(name, description, price):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(''' 
        INSERT INTO menu_items (name, description, price)
        VALUES (?, ?, ?)
    ''', (name, description, price))
    conn.commit()
    conn.close()

def delete_menu_item(item_id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM menu_items WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()

def get_temperature():
    API_KEY = "975ccb71edb9ade5e2a8415c67eb9107"
    CITY = "Zhytomyr"
    URL = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

    response = requests.get(URL)
    data = response.json()

    if response.status_code == 200:
        temperature = data["main"]["temp"]

        try:
            temperature = float(temperature)
        except ValueError:
            print("Помилка перетворення температури в число.")
            temperature = None
        print(f"Поточна температура у місті Житомир: {temperature}°C")
        return temperature
    else:
        print("Помилка отримання погоди:", data)
        return None

@app.route("/dostavka")
def dostavka():
    return render_template("dostavka.html")


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/menu/")
def get_menu():
    pizzas = get_menu_items()
    cart_count = len(session.get('cart', []))
    temperature = get_temperature()


    if 'holodno_visits' in session and session['holodno_visits'] >= 1:

        print("Кількість відвідувань holodno_event більше або дорівнює 1. Не редіректимо.")
    elif temperature is not None and temperature <= 5:

        return redirect(url_for('holodno_event'))

    if isinstance(temperature, (int, float)):
        temperature = round(temperature)
        print(f"Температура передана в шаблон: {temperature}")
    else:
        print("Помилка: Температура не є числом")

    print(f"це передається в меню {temperature}")
    return render_template("menu.html", pizzas=pizzas, cart_count=cart_count, temperature=temperature)



@app.route("/holodno_event/")
def holodno_event():

    if 'holodno_visits' not in session:
        session['holodno_visits'] = 0


    session['holodno_visits'] += 1


    visits = session['holodno_visits']
    print(f"Кількість відвідувань сторінки holodno_event: {visits}")

    return render_template("holodno_event.html", visits=visits)


@app.route("/cart/")
def cart():
    cart_items = session.get('cart', [])
    total_price = sum(item['price'] for item in cart_items)
    return render_template("cart.html", cart_items=cart_items, total_price=total_price)

@app.route("/add_to_cart/<name>/<int:price>")
def add_to_cart(name, price):
    if 'cart' not in session:
        session['cart'] = []
    session['cart'].append({'name': name, 'price': price})
    session.modified = True
    return redirect(url_for('get_menu'))

@app.route("/admin/add", methods=["GET", "POST"])
def add_item():
    if request.method == "POST":
        name = request.form['name']
        description = request.form['description']
        price = int(request.form['price'])
        add_menu_item(name, description, price)
        return redirect(url_for('get_menu'))
    return render_template("add_item.html")

@app.route("/admin/")
def admin_panel():
    return render_template("admin_panel.html")

@app.route("/admin/delete", methods=["GET", "POST"])
def delete_item():
    if request.method == "POST":
        item_id = int(request.form['item_id'])
        delete_menu_item(item_id)
        return redirect(url_for('get_menu'))
    pizzas = get_menu_items()
    return render_template("delete_item.html", pizzas=pizzas)

if __name__ == "__main__":
    app.run(port=5050, debug=True)
