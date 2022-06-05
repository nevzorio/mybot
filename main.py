# Телеграм-бот v.004
from io import BytesIO

import telebot  # pyTelegramBotAPI 4.3.1
from telebot import types
import requests
import bs4
import botGames  # бот-игры, файл botGames.py
import menuBot
import DZ  # домашнее задание от первого урока

bot = telebot.TeleBot('5272453284:AAE-Hyl6DrRhoQyolTv4kth2SbRTTPWydjg')  # Создаем экземпляр бота


# -----------------------------------------------------------------------
# Функция, обрабатывающая команды
@bot.message_handler(commands="start")
def command(message, res=False):
    chat_id = message.chat.id
    bot.send_sticker(chat_id, "CAACAgIAAxkBAAIxLmJipPIAAQ61R4Qvvorisn_IpTKu7wAC3g0AAopIuUnIn2ULM-mCUiQE")
    txt_message = f"Привет, {message.from_user.first_name}! Я тестовый бот для курса программирования на языке Python"
    bot.send_message(chat_id, text=txt_message, reply_markup=menuBot.Menu.getMenu(chat_id, "Главное меню").markup)


# -----------------------------------------------------------------------
# Получение стикеров от юзера
@bot.message_handler(content_types=['sticker'])
def get_messages(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Это " + message.content_type)

    sticker = message.sticker
    bot.send_message(message.chat.id, sticker)

    # глубокая инспекция объекта
    # import inspect,pprint
    # i = inspect.getmembers(sticker)
    # pprint.pprint(i)


# -----------------------------------------------------------------------
# Получение аудио от юзера
@bot.message_handler(content_types=['audio'])
def get_messages(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Это " + message.content_type)

    audio = message.audio
    bot.send_message(chat_id, audio)

# -----------------------------------------------------------------------
# Получение голосовухи от юзера
@bot.message_handler(content_types=['voice'])
def get_messages(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Это " + message.content_type)

    voice = message.voice
    bot.send_message(message.chat.id, voice)


# -----------------------------------------------------------------------
# Получение фото от юзера
@bot.message_handler(content_types=['photo'])
def get_messages(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Это " + message.content_type)

    photo = message.photo
    bot.send_message(message.chat.id, photo)


# -----------------------------------------------------------------------
# Получение видео от юзера
@bot.message_handler(content_types=['video'])
def get_messages(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Это " + message.content_type)

    video = message.video
    bot.send_message(message.chat.id, video)


# -----------------------------------------------------------------------
# Получение документов от юзера
@bot.message_handler(content_types=['document'])
def get_messages(message):
    chat_id = message.chat.id
    mime_type = message.document.mime_type
    bot.send_message(chat_id, "Это " + message.content_type + " (" + mime_type + ")")

    document = message.document
    bot.send_message(message.chat.id, document)
    if message.document.mime_type == "video/mp4":
        bot.send_message(message.chat.id, "This is a GIF!")

# -----------------------------------------------------------------------
# Получение координат от юзера
@bot.message_handler(content_types=['location'])
def get_messages(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Это " + message.content_type)

    location = message.location
    bot.send_message(message.chat.id, location)


# -----------------------------------------------------------------------
# Получение контактов от юзера
@bot.message_handler(content_types=['contact'])
def get_messages(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Это " + message.content_type)

    contact = message.contact
    bot.send_message(message.chat.id, contact)


# -----------------------------------------------------------------------
# Получение сообщений от юзера
@bot.message_handler(content_types=['text'])
def get_text_messages(message):

    chat_id = message.chat.id
    ms_text = message.text

    cur_user = menuBot.Users.getUser(chat_id)
    if cur_user == None:
        cur_user = menuBot.Users(chat_id, message.json["from"])

    result = goto_menu(chat_id, ms_text)  # попытаемся использовать текст как команду меню, и войти в него
    if result == True:
        return  # мы вошли в подменю, и дальнейшая обработка не требуется

    cur_menu = menuBot.Menu.getCurMenu(chat_id)
    if cur_menu != None and ms_text in cur_menu.buttons:  # проверим, что команда относится к текущему меню

        if ms_text == "Помощь":
            send_help(chat_id)

        elif ms_text == "Прислать лису":
            bot.send_photo(chat_id, photo=get_foxURL(), caption="Вот тебе лис!")

        elif ms_text == "Прислать анекдот":
            # bot.send_message(chat_id, text=get_anekdot())
            bot.send_message(chat_id, text=get_news())
        elif ms_text == "Погода":
            get_weather()
            bot.send_message(chat_id, text=get_weather())
        elif ms_text == "Симпсоны":
            get_si()
            bot.send_message(chat_id, text=get_si())


        elif ms_text == "Прислать фильм":
            send_film(chat_id)


        elif ms_text == "Угадай кто?":

            get_ManOrNot(chat_id)


        elif ms_text == "Карту!":

            if game21 == None:  # если мы случайно попали в это меню, а объекта с игрой нет

                goto_menu(chat_id, "Выход")

                return

            text_game = game21.get_cards(1)

            bot.send_media_group(chat_id, media=getMediaCards(game21))  # получим и отправим изображения карт

            bot.send_message(chat_id, text=text_game)

            if game21.status != None:  # выход, если игра закончена

                goto_menu(chat_id, "Выход")

                return


        elif ms_text == "Стоп!":

            game21 = None

            goto_menu(chat_id, "Выход")

            return





    elif ms_text == "Задание 1":

        DZ.dz1(bot, chat_id)

    elif ms_text == "Задание 2":

        DZ.dz2(bot, chat_id)

    elif ms_text == "Задание 3":

        DZ.dz3(bot, chat_id)

    elif ms_text == "Задание 4,5":

        DZ.dz45(bot, chat_id)

    elif ms_text == "Задание 6":

        DZ.dz6(bot, chat_id)

    elif ms_text == "Задание 7.1":

        DZ.dz7n(bot, chat_id)

    elif ms_text == "Задание 7.2":

        DZ.dz7a(bot, chat_id)

    elif ms_text == "Задание 8":

        DZ.dz8(bot, chat_id)

    elif ms_text == "Задание 9.1":

        DZ.dz91(bot, chat_id)

    elif ms_text == "Задание 9.2":

        DZ.dz92(bot, chat_id)

    elif ms_text == "Задание 10":

        DZ.dz10(bot, chat_id)
    else:  # ...........................................................................................................
        bot.send_message(chat_id, text="Мне жаль, я не понимаю вашу команду: " + ms_text)
        goto_menu(chat_id, "Главное меню")

# -----------------------------------------------------------------------
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    # если требуется передать параметр или несколько параметров в обработчик кнопки, использовать методы Menu.getExtPar() и Menu.setExtPar()
    pass
    # if call.data == "ManOrNot_GoToSite": #call.data это callback_data, которую мы указали при объявлении InLine-кнопки
    #
    #     # После обработки каждого запроса нужно вызвать метод answer_callback_query, чтобы Telegram понял, что запрос обработан.
    #     bot.answer_callback_query(call.id)

# -----------------------------------------------------------------------
def goto_menu(chat_id, name_menu):
    # получение нужного элемента меню
    cur_menu = menuBot.Menu.getCurMenu(chat_id)
    if name_menu == "Выход" and cur_menu != None and cur_menu.parent != None:
        target_menu = menuBot.Menu.getMenu(chat_id, cur_menu.parent.name)
    else:
        target_menu = menuBot.Menu.getMenu(chat_id, name_menu)

    if target_menu != None:
        bot.send_message(chat_id, text=target_menu.name, reply_markup=target_menu.markup)

        # Проверим, нет ли обработчика для самого меню. Если есть - выполним нужные команды
        if target_menu.name == "Игра в 21":
            game21 = botGames.newGame(chat_id, botGames.Game21(jokers_enabled=True))  # создаём новый экземпляр игры
            text_game = game21.get_cards(2)  # просим 2 карты в начале игры
            bot.send_media_group(chat_id, media=getMediaCards(game21))  # получим и отправим изображения карт
            bot.send_message(chat_id, text=text_game)

        elif target_menu.name == "Камень, ножницы, бумага":
            gameRSP = botGames.newGame(chat_id, botGames.GameRPS())  # создаём новый экземпляр игры
            text_game = "<b>Победитель определяется по следующим правилам:</b>\n" \
                        "1. Камень побеждает ножницы\n" \
                        "2. Бумага побеждает камень\n" \
                        "3. Ножницы побеждают бумагу"
            bot.send_photo(chat_id, photo="https://i.ytimg.com/vi/Gvks8_WLiw0/maxresdefault.jpg", caption=text_game, parse_mode='HTML')

        return True
    else:
        return False


# -----------------------------------------------------------------------
def getMediaCards(game21):
    medias = []
    for url in game21.arr_cards_URL:
        medias.append(types.InputMediaPhoto(url))
    return medias


# -----------------------------------------------------------------------
def send_help(chat_id):
    global bot
    bot.send_message(chat_id, "Автор: Егор Невзоров")
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="Напишите автору", url="https://t.me/l61lll")
    markup.add(btn1)
    img = open('blackman.jpg', 'rb')
    bot.send_photo(chat_id, img, reply_markup=markup)

    bot.send_message(chat_id, "Активные пользователи чат-бота:")
    for el in menuBot.Users.activeUsers:
        bot.send_message(chat_id, menuBot.Users.activeUsers[el].getUserHTML(), parse_mode='HTML')

# -----------------------------------------------------------------------
def send_film(chat_id):
    film = get_randomFilm()
    info_str = f"<b>{film['Наименование']}</b>\n" \
               f"Год: {film['Год']}\n" \
               f"Страна: {film['Страна']}\n" \
               f"Жанр: {film['Жанр']}\n" \
               f"Продолжительность: {film['Продолжительность']}"
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="Трейлер", url=film["Трейлер_url"])
    btn2 = types.InlineKeyboardButton(text="СМОТРЕТЬ онлайн", url=film["фильм_url"])
    markup.add(btn1, btn2)
    bot.send_photo(chat_id, photo=film['Обложка_url'], caption=info_str, parse_mode='HTML', reply_markup=markup)


# -----------------------------------------------------------------------
def get_anekdot():
    array_anekdots = []
    req_anek = requests.get('http://anekdotme.ru/random')
    if req_anek.status_code == 200:
        soup = bs4.BeautifulSoup(req_anek.text, "html.parser")
        result_find = soup.select('.anekdot_text')
        for result in result_find:
            array_anekdots.append(result.getText().strip())
    if len(array_anekdots) > 0:
        return array_anekdots[0]
    else:
        return ""

# -----------------------------------------------------------------------
def get_news():
    url = 'https://lovesimpsons.ru/random/'
    infoFilm = {}
    req_film = requests.get(url)
    soup = bs4.BeautifulSoup(req_film.text, "html.parser")
    result_find = soup.find('div', align="center", style="width: 100%")
    infoFilm["Наименование"] = result_find.find("h2").getText()
    names = infoFilm["Наименование"].split(" / ")
    infoFilm["Наименование_rus"] = names[0].strip()
    if len(names) > 1:
        infoFilm["Наименование_eng"] = names[1].strip()

    images = []
    for img in result_find.findAll('img'):
        images.append(url + img.get('src'))
    infoFilm["Обложка_url"] = images[0]

    details = result_find.findAll('td')



    infoFilm["фильм_url"] = url + details[7].contents[0]["href"]

    return infoFilm

# -----------------------------------------------------------------------
def get_foxURL():
    url = ""
    req = requests.get('https://randomfox.ca/floof/')
    if req.status_code == 200:
        r_json = req.json()
        url = r_json['image']
        # url.split("/")[-1]
    return url
# -----------------------------------------------------------------------
def get_dogURL():
    url = ""
    req = requests.get('https://random.dog/woof.json')
    if req.status_code == 200:
        r_json = req.json()
        url = r_json['url']
        # url.split("/")[-1]
    return url
# -----------------------------------------------------------------------
def get_ManOrNot(chat_id):
    global bot

    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="Проверить", url="https://vc.ru/dev/58543-thispersondoesnotexist-sayt-generator-realistichnyh-lic")
    markup.add(btn1)

    req = requests.get("https://thispersondoesnotexist.com/image", allow_redirects=True)
    if req.status_code == 200:
        img = BytesIO(req.content)
        bot.send_photo(chat_id, photo=img, reply_markup=markup, caption="Этот человек реален?")

# ---------------------------------------------------------------------
def get_randomFilm():
    url = 'https://randomfilm.ru/'
    infoFilm = {}
    req_film = requests.get(url)
    soup = bs4.BeautifulSoup(req_film.text, "html.parser")
    result_find = soup.find('div', align="center", style="width: 100%")
    infoFilm["Наименование"] = result_find.find("h2").getText()
    names = infoFilm["Наименование"].split(" / ")
    infoFilm["Наименование_rus"] = names[0].strip()
    if len(names) > 1:
        infoFilm["Наименование_eng"] = names[1].strip()

    images = []
    for img in result_find.findAll('img'):
        images.append(url + img.get('src'))
    infoFilm["Обложка_url"] = images[0]

    details = result_find.findAll('td')
    infoFilm["Год"] = details[0].contents[1].strip()
    infoFilm["Страна"] = details[1].contents[1].strip()
    infoFilm["Жанр"] = details[2].contents[1].strip()
    infoFilm["Продолжительность"] = details[3].contents[1].strip()
    infoFilm["Режиссёр"] = details[4].contents[1].strip()
    infoFilm["Актёры"] = details[5].contents[1].strip()
    infoFilm["Трейлер_url"] = url + details[6].contents[0]["href"]
    infoFilm["фильм_url"] = url + details[7].contents[0]["href"]

    return infoFilm

# -----------------------------------------------------------------------
def get_weather():
    from yaweather import Russia, YaWeather

    y = YaWeather(
        api_key='7a4600f8-b028-4278-baf2-b06c443f01f4')  # Мой ключ АПИ, но лучше создай свой тут - https://developer.tech.yandex.ru/services/18

    res = y.forecast(Russia.SaintPetersburg)  # Указываешь местоположение

    for f in res.forecasts:
        day = f.parts.day_short
        b = (f'{f.date} | {day.temp} °C, {day.condition}')
        return b # То, что выведет функция

def get_si():
    url = requests.get('https://lovesimpsons.ru/random/')  # Указываем сайт с которого будем вытаскивать инфу
    b = bs4.BeautifulSoup(url.text, "html.parser")
    url1 = b.select(".episode__title")  # Выбираем место откуда будет вытаскиваться текст
    url2 = b.select(".episode__info-number")  # Выбираем место откуда будет вытаскиваться текст

    url_print = url1[0].getText()
    url1_print = url2[0].getText()

    a = 'Название Серии:'
    a = str(a + url_print + url1_print)
    return a  # То, что выведет функция

bot.polling(none_stop=True, interval=0)  # Запускаем бота

print()

