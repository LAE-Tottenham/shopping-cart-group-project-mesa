from currency_exchange_tool import check_currency_exists, currency_convert
import requests
import math

items = {
    'bread': 1.20,
    'milk': 1.15,
    'chocolate': 0.5,
    'eggs': 0.65,
    'water': 1.0,
    'plastic bag': 0.1,
    'crisps': 1.25,
    'biscuits': 1.25,
    'energy drink': 1.0,
    'cake': 5.0,
}

def start_shop():
    for item, amount in items.items():
        print("{} = £{:.2f}".format(item, amount))

def select_items():
    selection = []
    cont = ''
    while cont != 'n':
        item_selected = input("Enter item: ")
        if item_selected in items:
            selection.append(item_selected)
        else:
            print("Item not available.")
        cont = input("Would you like more items? y/n\n").lower()
    return selection

def calculate_distance(lat1, lon1, lat2, lon2):
    # Convert degrees to radians
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = (math.sin(dlat / 2) ** 2 + 
         math.cos(lat1) * math.cos(lat2) * 
         (math.sin(dlon / 2) ** 2))
    c = 2 * math.asin(math.sqrt(a))

    radius = 6371
    distance = radius * c
    return distance

def calculate_price(selection):
    price = 0
    for item in selection:
        price += items[item]
    
    print(f'Your total cost is £{price}')
    address = input("Enter your address:\n")
    
    postcode_resp = requests.get(f"https://api.postcodes.io/postcodes/{address}").json()
    user_latitude = postcode_resp['result']['latitude']
    user_longitude = postcode_resp['result']['longitude']
    area = postcode_resp['result']['admin_ward']

    fixed_latitude = 51.6013
    fixed_longitude = -0.0664

    distance = calculate_distance(user_latitude, user_longitude, fixed_latitude, fixed_longitude)
    
    print(f'You live in {area}, that is {distance:.2f} km away')

    if distance < 1:
        delivery_charge = 1.0
    elif distance < 5:
        delivery_charge = 2.0
    else:
        delivery_charge = 5.0
    print(f'Your price including delivery charge is £{delivery_charge + price}')
    return price + delivery_charge

def payment(price, username, selection):
    conv = input("Would you like to convert? y/n\n")
    if conv.lower() == 'y':
        if price > 10 and price < 1000:
            currency = input("What currency would you like to convert to?\n")
            if not check_currency_exists(currency):
                while not check_currency_exists(currency):
                    currency = input("Please enter valid currency:\n")
            converted = currency_convert(currency, price)
            print(f'Your price in the currency you chose is {converted} {currency}')
        else:
            print("You are not eligible to convert")

    last_purchase = " and ".join(selection)
    update_last_purchase(username, last_purchase)

def update_last_purchase(username, last_purchase):
    # Read existing data
    with open("database.txt", "r") as db:
        lines = db.readlines()
    
    with open("database.txt", "w") as db:
        for line in lines:
            parts = line.strip().split(", ")
            if len(parts) == 3:
                if parts[0] == username:
                    db.write(f"{parts[0]}, {parts[1]}, {last_purchase}\n")
                else:
                    db.write(line)

def make_account():
    with open("database.txt", "a") as db:
        username = input("Enter Username:\n")
        password = input("Create a password:\n")
        verify_p = input("Confirm password:\n")
        
        if password != verify_p:
            print("Passwords don't match! Please restart.")
            make_account()

        # Check if username exists
        if any(username in line for line in open("database.txt")):
            print("Username exists")
            make_account()

        db.write(f"{username}, {password}, No purchases yet\n")
        print("Success!")

def save_last_purchase(username, purchase, currency):
    lines = []
    with open("database.txt", "r") as db:
        for line in db:
            if line.startswith(username):
                lines.append(f"{username}, {line.split(',')[1].strip()}, Last purchase: {purchase} {currency}\n")
            else:
                lines.append(line)
    with open("database.txt", "w") as db:
        db.writelines(lines)

def access():
    with open("database.txt", "r") as db:
        username = input("Enter your username:\n")
        password = input("Enter your password:\n")
        
        if username and password:
            d = {}
            for line in db:
                parts = line.strip().split(", ")
                if len(parts) == 3:
                    a, b, last_purchase = parts
                    d[a] = (b, last_purchase)
                else:
                    print(f"Skipping improperly formatted line: {line.strip()}")  # Optional logging
            
            if username in d:
                if password == d[username][0]:
                    print("Log in Success!")
                    print("Hi,", username)
                    last_purchase = d[username][1]
                    if last_purchase:
                        print(f'Your last purchase was: {last_purchase}')
                    else:
                        print("No purchases yet.")
                    return username
                else: 
                    print("Incorrect password.")
            else:
                print("Username doesn't exist.")
        else:
            print("Please enter a value.")
    return None

def option():
    user_option = input("Login | Signup: ")
    if user_option.lower() == "login":
        return access()
    elif user_option.lower() == "signup":
        make_account()
        print("Account created successfully! Please log in.")
        return access()
    else:
        print("Please select a valid option.")
        return None