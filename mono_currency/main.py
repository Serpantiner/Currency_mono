import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QFont

import requests
import json

# Check if the data is already cached
try:
    with open('currency_data.json', 'r') as file:
        data = json.load(file)
except (FileNotFoundError, json.JSONDecodeError):
    data = []

if not data:
    url = 'https://api.monobank.ua/bank/currency'
    headers = {'X-Token': 'uiJBN_DZFKUqO7OE34O3cnwbmRpsL_FsU056B8koQtt4'}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        # Cache the data
        with open('currency_data.json', 'w') as file:
            json.dump(data, file)
    else:
        print('Error:', response.status_code)
        data = []

# Filter the currency data for UAH to USD, EUR
target_currencies = [840, 978]  # USD, EUR
filtered_data = []
processed_currencies = set()

for currency in data:
    if currency['currencyCodeA'] in target_currencies and currency['currencyCodeA'] not in processed_currencies:
        filtered_data.append(currency)
        processed_currencies.add(currency['currencyCodeA'])

# Create a PyQt application
app = QApplication(sys.argv)

# Create a QWidget (window)
window = QWidget()
window.setWindowTitle('Currency Exchange Rates')
window.setStyleSheet('background-color: grey;')

# Create a QVBoxLayout to hold the labels
layout = QVBoxLayout()

# Create labels for each currency
for currency in filtered_data:
    if currency['currencyCodeA'] == 840:
        currency_name = 'USD'
    elif currency['currencyCodeA'] == 978:
        currency_name = 'EUR'

    rate_buy = currency['rateBuy']
    rate_sell = currency['rateSell']
    exchange_rate = f'$1 {currency_name} = {rate_buy:.2f} UAH / {rate_sell:.2f} UAH'

    label = QLabel(exchange_rate)
    label.setStyleSheet(
        '''
        QLabel {
            color: black;
            background-color: #ECECEC;
            border-style: solid;
            border-width: 1px;
            border-color: #AAAAAA;
            padding: 10px;
            font-size: 12pt;
        }
        '''
    )
    layout.addWidget(label)

# Set the layout for the window
window.setLayout(layout)

# Set the font for all labels
font = QFont('Helvetica', 12)
app.setFont(font)

# Show the window
window.show()

# Run the application event loop
sys.exit(app.exec_())
