import requests
from config import OPENCAGE_API_KEY, EXCHANGE_API_KEY

def get_timezone_by_city(city):
    url = f"https://api.opencagedata.com/geocode/v1/json?q={city}&key={OPENCAGE_API_KEY}&language=ru"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            timezone = data['results'][0]['annotations']['timezone']['name']
            return timezone
    return None

def get_exchange_rate(from_currency, to_currency):
    url = f"https://v6.exchangerate-api.com/v6/{EXCHANGE_API_KEY}/latest/{from_currency}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if 'conversion_rates' in data and to_currency in data['conversion_rates']:
            return data['conversion_rates'][to_currency]
    return None