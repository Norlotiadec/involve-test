from flask import Flask, render_template, request, redirect
import hashlib
import requests
import logging
from config import SECRET_KEY, shop_id, shop_order_id, payway
from models import add_value

app = Flask(__name__)


def sing(data, fields, descriptions=None):
    sorted_data = [data[field] for field in sorted(fields)]
    sing_str = ':'.join(sorted_data) + SECRET_KEY
    data['sign'] = hashlib.sha256(sing_str.encode('utf-8')).hexdigest()
    if descriptions:
        data['description'] = descriptions
    return data


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        amount = request.form.get('amount')
        currency = request.form.get('Currency')
        description = request.form.get('description')

        if currency == '978':
            required_param = ['amount', 'currency', 'shop_id', 'shop_order_id']
            data_api = {
                "amount": amount,
                "shop_id": shop_id,
                "currency": currency,
                "shop_order_id": shop_order_id
            }

            sing(data_api, required_param, description)
            add_value(currency, float(amount), description)

            return render_template('pay_index.html', data=data_api)

        elif currency == '840':
            required_param = ['payer_currency', 'shop_amount', 'shop_currency', 'shop_id', 'shop_order_id']
            data_api = {
                "payer_currency": currency,
                "shop_amount": amount,
                "shop_currency": currency,
                "shop_id": shop_id,
                "shop_order_id": shop_order_id
            }

            sing(data_api, required_param, description)
            add_value(currency, float(amount), description)

            response = requests.post('https://core.piastrix.com/bill/create', json=data_api)
            if response.json()['data']:
                success_url = response.json()['data']['url']
                return redirect(success_url)
            else:
                logging.error(f'''{response.json()['message']}''')
                return render_template('index.html')

        else:
            required_param = ['amount', 'currency', 'shop_id', 'payway', 'shop_order_id']
            data_api = {
                "amount": amount,
                "currency": currency,
                "shop_id": shop_id,
                "payway": payway,
                "shop_order_id": shop_order_id
            }

            sing(data_api, required_param, description)
            add_value(currency, float(amount), description)

            response = requests.post('https://core.piastrix.com/invoice/create', json=data_api)
            if response.json()['data']:
                success_url = response.json()['data']['data']['PAYMENT_URL']
                return redirect(success_url)
            else:
                logging.error(f'''{response.json()['message']}''')
                return render_template('index.html')

    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.run()
