import requests
from config import OPENCAGE_API_KEY, EXCHANGE_API_KEY, WEATHER_API_KEY
from bs4 import BeautifulSoup


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

def get_weather(city):
    url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={city}&lang=ru"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather_description = data['current']['condition']['text']
        temperature = data['current']['temp_c']
        humidity = data['current']['humidity']
        wind_speed = data['current']['wind_mph']
        return   (
                f"Погода в городе {city}:\n"
                f"Описание: {weather_description}\n"
                f"Температура: {temperature}°C\n"
                f"Влажность: {humidity}%\n"
                f"Скорость ветра: {wind_speed} м/с"
            )
    else:
        return None

def search_google(query):
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        search_results = []
        
        for item in soup.find_all('h3'):
            title = item.get_text()
            parent_link = item.find_parent('a')

            if parent_link and 'href' in parent_link.attrs:
                link = parent_link['href']
                search_results.append(f"{title}\nCсылка на ресурс: {link}\n")
        
        return "\n".join(search_results) if search_results else "Результаты не найдены."
    else:
        return "Не удалось выполнить поиск."