import requests
import bs4


# Функция, которая показывает курс BNB (криптовалюты)

def get_si():
    url = requests.get('https://lovesimpsons.ru/random/')  # Указываем сайт с которого будем вытаскивать инфу
    b = bs4.BeautifulSoup(url.text, "html.parser")
    url1 = b.select(".episode__title")  # Выбираем место откуда будет вытаскиваться текст
    url2 = b.select(".episode__info-number")  # Выбираем место откуда будет вытаскиваться текст
    url3 = b.select(".episode__features")  # Выбираем место откуда будет вытаскиваться текст")  # Выбираем место откуда будет вытаскиваться текст
    url_print = url1[0].getText()
    url1_print = url2[0].getText()
    url2_print = url3[0].getText()
    a = 'Название Серии:'
    a = str(a + url_print + url1_print + url2_print)
    return a  # То, что выведет функция


print(get_si())


def get_weather():
    from yaweather import Russia, YaWeather

    y = YaWeather(
        api_key='7a4600f8-b028-4278-baf2-b06c443f01f4')  # Мой ключ АПИ, но лучше создай свой тут - https://developer.tech.yandex.ru/services/18

    res = y.forecast(Russia.SaintPetersburg)  # Указываешь местоположение

    for f in res.forecasts:
        day = f.parts.day_short
        b = (f'{f.date} | {day.temp} °C, {day.condition}')
        return b # То, что выведет функция


print('Погода в СПб на - '+get_weather())


def get_raccoonURL():
    url = ""
    req = requests.get('https://some-random-api.ml/animal/raccoon')
    if req.status_code == 200:
        r_json = req.json()
        url = r_json['image']
        # url.split("/")[-1]
    return url
