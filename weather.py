from pyowm import OWM
from deep_translator import GoogleTranslator
from pyowm.utils import timestamps

owm = OWM('53cf4b96af24237dcf3b521bcf08e74c')
def _get_weather(city, day):
    if day == 'today':
        to_translate = city
        mgr = owm.weather_manager()
        observation = mgr.weather_at_place(f'{city}, RU')
        w = observation.weather
        return f'Температура: {w.temperature("celsius")["temp_max"], }\n' \
               f'{w.detailed_status}\n' \
               f'{w.rain}\n' \
               f'Ветер {w.wind()["speed"]} м/c' # {'temp_max': 10.5, 'temp': 9.7, 'temp_min': 9.0}'
    else:
        to_translate = city
        city = GoogleTranslator(source='auto', target='en').translate(to_translate)
        mgr = owm.weather_manager()
        daily_forecaster = mgr.forecast_at_place(f'{city},RU', 'daily')
        tomorrow = timestamps.tomorrow()
        weather = daily_forecaster.get_weather_at(tomorrow)
        return weather
print(_get_weather('Kazan', 'tomorrow')) # e = pyowm.commons.exceptions.UnauthorizedError: Invalid API Key provided
