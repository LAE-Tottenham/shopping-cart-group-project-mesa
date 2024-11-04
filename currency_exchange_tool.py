import math

exchange_rates = {
    'GBP' : 1.0,
    'USD': 1.13,
    'EUR': 1.15,
    'CAD' : 1.8,
    'TRY' : 44.72,
    'JMD' : 206.88
}

def check_currency_exists(currency):
    for key in exchange_rates:
        if  currency == key:
            return True
    return False

def currency_convert(new_c, amount):
    converted = amount * exchange_rates[new_c]
    return round(converted,2)