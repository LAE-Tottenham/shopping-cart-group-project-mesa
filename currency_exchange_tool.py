import math # you'll probably need this

exchange_rates = {
    'USD': 1.3, #I.E. 1 Pound is 1.3 Dollars
    'EUR': 1.2,
    'CAD': 1.8, 
    'TRY': 44.72,
    'JMD': 206.68
}

def check_currency_exists(currency):
    return

def currency_convert(original_c, new_c, amount):
    if original_c != "GBP":
        x = exchange_rates[original_c]
        y = exchange_rates[new_c]
        GBP = amount / x
        converted_c = GBP * y
        return converted_c
    else:
        y = exchange_rates[new_c]
        converted_c = amount * y
        return converted_c

print(currency_convert("USD", "CAD", 484))
    