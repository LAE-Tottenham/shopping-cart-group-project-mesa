from shop_functions import start_shop, payment, option, select_items, calculate_price
import pyfiglet

f = pyfiglet.figlet_format("Welcome to my shop", font='slant')
print(f)

username = option()
if username:
    start_shop()
    selection = select_items()
    price = calculate_price(selection)
    payment(price, username, selection)