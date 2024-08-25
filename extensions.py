import requests
import json
from config import API_KEY, EXCHANGE_API_URL


class APIException(Exception):
    pass


class CurrencyConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f"Неверное количество валюты: {amount}")

        if base == quote:
            raise APIException(f"Введены одинаковые валюты {base}.")

        try:
            response = requests.get(f'{EXCHANGE_API_URL}{API_KEY}/latest/{base.upper()}')
            data = json.loads(response.text)
        except requests.exceptions.RequestException:
            raise APIException("Ошибка при запросе к API.")

        if response.status_code != 200:
            raise APIException(f"Ошибка API: {data.get('error-type', 'Неизвестная ошибка')}")

        rates = data.get('conversion_rates', {})
        if quote.upper() not in rates:
            raise APIException(f"Валюта {quote} не найдена.")

        rate = rates[quote.upper()]
        total_amount = rate * amount

        return total_amount
