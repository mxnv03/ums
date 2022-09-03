import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import random
import json

vk = vk_api.VkApi(token=
                  "vk1.a.7e3JWELeDsFfTuEwRaHzsVzlGYHdj0xBY8bFTnMVu5kEAlBfi-U8CX8YlQMjMR-"
                  "HrBxNEdqH8Izkze9oMAJxHEyFMc1wxsICoohaESJlfwc82O2UER5X43_1_wHtXK2rmApxuXU_YZC-"
                  "jCV8o0XGU8RxA8VSxPNtAE2ZwLhzqC5xTCcbbsNB6krpaSSsp5D1"
                  )
longpoll = VkLongPoll(vk)
api = vk.get_api()

# flags
new_mess = True
inp_city = False
check_inp_city = False
city = ''
weather = False
cork = False
poster = False
currency = False


def write_msg(user_id, message, key):
    vk.method('messages.send',
              {'user_id': user_id,
               'message': message,
               'keyboard': key,
               'random_id': random.randint(0, 2048)})


about_us_keyboard = {
    "inline": True,
    "buttons": [
        [{
            "action": {
                "type": "text",
                "payload": "{\"button\": \"1\"}",
                "label": "Основная информация"
            },
            "color": "positive"
        }],
        [{
            "action": {
                "type": "text",
                "payload": "{\"button\": \"2\"}",
                "label": "Чем мы занимаемся ?"
            },
            "color": "primary"
        },
        {
            "action": {
                "type": "text",
                "payload": "{\"button\": \"3\"}",
                "label": "Где мы находимся ?",
            },
            "color": "positive"
        }],
        [{
            "action": {
                "type": "text",
                "payload": "{\"button\": \"4\"}",
                "label": "Как попасть в команду ?",
            },
            "color": "primary"
        }],
        [{
            "action": {
                "type": "text",
                "payload": "{\"button\": \"5\"}",
                "label": "Контакты",
            },
            "color": 'secondary'
        }],
        [{
            "action": {
                "type": "text",
                "payload": "{\"button\": \"6\"}",
                "label": "Задать вопрос руководителю проекта",
            },
            "color": "negative"
        }]
    ],
}
about_us_keyboard = json.dumps(about_us_keyboard, ensure_ascii=False).encode('utf-8')
about_us_keyboard = str(about_us_keyboard.decode('utf-8'))

city_answer = {
    "inline": True,
    "buttons": [
        [{
            "action": {
                "type": "text",
                "payload": "{\"button\": \"1\"}",
                "label": "Да"
            },
            "color": "positive"
        }],
        [{
            "action": {
                "type": "text",
                "payload": "{\"button\": \"2\"}",
                "label": "Нет"
            },
            "color": "primary"
        }]
]}
city_answer = json.dumps(city_answer, ensure_ascii=False).encode('utf-8')
city_answer = str(city_answer.decode('utf-8'))

main_key = {
    "inline": True,
    "buttons": [
        [{
            "action": {
                "type": "text",
                "payload": "{\"button\": \"1\"}",
                "label": "Погода"
            },
            "color": "positive"
        }],
        [{
            "action": {
                "type": "text",
                "payload": "{\"button\": \"2\"}",
                "label": "Пробки"
            },
            "color": "positive"
        }],
        [{
            "action": {
                "type": "text",
                "payload": "{\"button\": \"2\"}",
                "label": "Афиша"
            },
            "color": "positive"
        }],
        [{
            "action": {
                "type": "text",
                "payload": "{\"button\": \"2\"}",
                "label": "Валюта"
            },
            "color": "positive"
        }],
        [{
            "action": {
                "type": "text",
                "payload": "{\"button\": \"2\"}",
                "label": "Изменить город"
            },
            "color": "primary"
        }]

]}
main_key = json.dumps(main_key, ensure_ascii=False).encode('utf-8')
main_key = str(main_key.decode('utf-8'))

weather_key = {
    "inline": True,
    "buttons": [
        [{
            "action": {
                "type": "text",
                "payload": "{\"button\": \"1\"}",
                "label": "Сегодня"
            },
            "color": "positive"
        }],
        [{
            "action": {
                "type": "text",
                "payload": "{\"button\": \"2\"}",
                "label": "Завтра"
            },
            "color": "primary"
        }]
]}
weather_key = json.dumps(weather_key, ensure_ascii=False).encode('utf-8')
weather_key = str(weather_key.decode('utf-8'))
poster_key = weather_key

try:
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                if event.text.lower() == "начать" and new_mess:
                    new_mess = False
                    user = api.users.get(user_ids=event.user_id)[0]
                    if 'city' in user.keys():
                        write_msg(event.user_id, f'Привет, {user["first_name"]}! \nТвой город {user["city"]}, верно?', city_answer)
                    else:
                        inp_city = True
                        write_msg(event.user_id, f'Привет, {user["first_name"]}! \nВведи твой город', key='')
                elif event.text.lower() == "изменить город":
                    inp_city = True
                    write_msg(event.user_id, f'Введи твой город', key='')

                elif event.text.lower() == "начать" and not new_mess:
                    write_msg(event.user_id, f'Что вы хотели бы узнать?', main_key)
                elif event.text.lower() == 'нет' and check_inp_city:
                    inp_city = True
                    check_inp_city = False
                    write_msg(event.user_id, f'Введи твой город ещё раз', key='')
                elif event.text.lower() == 'да' and check_inp_city:
                    write_msg(event.user_id, f'Хорошо, запомнил, что ты живёшь в г. {city}!', key=main_key)
                elif event.text.lower() == 'погода':
                    write_msg(event.user_id, f'На какой день сказать погоду?', key=weather_key)
                    weather = True
                elif weather and event.text.lower() == 'завтра':
                    weather = False
                    write_msg(event.user_id, f"Вот погода в г. {city} завтра:\n\n"
                                             f"Температура 15 оС\n"
                                             f"Облачно с прояснениями\n"
                                             f"Ветер 2 м/с", key=main_key)
                elif weather and event.text.lower() == 'сегодня':
                    weather = False
                    write_msg(event.user_id, f"Вот погода в г. {city} сегодня:\n\n"
                                             f"Температура 14 ℃\n"
                                             f"Облачно с прояснениями\n"
                                             f"Ветер 3 м/с", key=main_key)
                elif event.text.lower() == 'валюта':
                    write_msg(event.user_id, f"1$ = 60,37₽\n"
                                             f"1€ = 60,22₽\n"
                                             f"1£ = 69,58₽\n"
                                             f"1円 = 0,4311₽\n"
                                             f"1元 = 8,74₽\n", key=main_key)
                elif event.text.lower() == 'пробки' and cork:
                    write_msg(event.user_id, f"Сейчас в г. {city} пробки {random.randint(1, 10)} балла(ов)", key=main_key)
                elif event.text.lower() == 'афиша':
                    write_msg(event.user_id, f'На какой день показать афишу?', key=poster_key)
                    poster = True
                elif poster and event.text.lower() == 'сегодня':
                    poster = False
                    write_msg(event.user_id, f"Афиша на сегодня\n\n"
                                             f"Прогулки с «Гаражом». Назад в будущее. Мифы и легенды Северного Чертанова\n"
                                             f"Цена от 800₽\n"
                                             f"https://afisha.yandex.ru/moscow/excursions/progulki-s-garazhom-nazad-v-budushchee-mify-i-legendy-severnogo-chertanova?source=rubric\n\n"
                                             f"Путешествие по ночной библиотеке\n"
                                             f"Цена от 1500₽\n"
                                             f"https://afisha.yandex.ru/moscow/excursions/puteshestvie-po-nochnoi-biblioteke-rossiiskaia-gosudarstvennaia-biblioteka?source=rubric\n\n"
                                             f"Хабиб\n"
                                             f"Цена от 1800₽\n"
                                             f"https://afisha.yandex.ru/moscow/concert/khabib-2022-09-03?source=rubric\n\n"
                                             f"Найти Бэнкси\n"
                                             f"Цена от 1150₽\n"
                                             f"https://afisha.yandex.ru/moscow/art/naiti-benksi?source=rubric\n\n"
                                             f"Шахматы\n"
                                             f"Цена от 1900₽\n"
                                             f"https://afisha.yandex.ru/moscow/musical/chess-musical?source=rubric\n\n", key=main_key)
                elif poster and event.text.lower() == 'завтра':
                    poster = False
                    write_msg(event.user_id, f"Афиша на завтра\n\n"
                                             f"Посещение смотровой площадки «Выше только любовь»\n"
                                             f"Цена от 1000₽\n"
                                             f"https://afisha.yandex.ru/moscow/excursions/poseshchenie-smotrovoi-ploshchadki?source=rubric&schedule-preset=today\n\n"
                                             f"StandUp & Action\n"
                                             f"Цена от 1690₽\n"
                                             f"https://afisha.yandex.ru/moscow/standup/standup-action?source=rubric\n\n"
                                             f"День New Israeli Sound\n"
                                             f"Цена от 2000₽\n"
                                             f"https://afisha.yandex.ru/moscow/concert/den-new-israeli-sound?source=rubric\n\n"
                                             f"Гурам Амарян\n"
                                             f"Цена от 1500₽\n"
                                             f"https://afisha.yandex.ru/moscow/standup/guram-amaryan-coin-event-hall?source=rubric\n\n"
                                             f"Чайка\n"
                                             f"Цена от 600₽\n"
                                             f"https://afisha.yandex.ru/moscow/theatre_show/chaika-moskovskii-khudozhestvennyi-teatr-imeni-a-p-chekhova?source=rubric\n\n" ,key=main_key)

                elif inp_city:
                    city = event.text
                    write_msg(event.user_id, f'Твой город {city}, верно?', key=city_answer)
                    inp_city = False
                    check_inp_city = True
                    cork = True
                    weather = True
                    poster = True

                else:
                    write_msg(event.user_id, f'Ой, что-то пошло не так :(', key='')
except Exception as e:
    print(e)
