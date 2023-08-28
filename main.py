from datetime import datetime, timedelta
import time

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
import requests

from bs4 import BeautifulSoup

import config
import url


session = requests.Session()

bot = Bot(token=config.BOT_API_TOKEN)
dp = Dispatcher(bot)

answ = ()

url_login = "http://us.gblnet.net/oper/"


HEADERS = {
    "main": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:105.0) Gecko/20100101 Firefox/105.0"
}

data = {
    "action": "login",
    "username": config.loginUS,
    "password": config.pswUS
}
response = session.post(url_login, data=data, headers=HEADERS).text


def create_sessions():
    global data
    global response
    # По бесконечному циклу запустим создание сессий
    while True:
        try:
            response = session.post(url_login, data=data, headers=HEADERS).text
            print("Сессия Юзера создана 2")
            break
        except ConnectionError:
            print("Ошибка создания сессии")
            time.sleep(60)


@dp.message_handler()
async def echo_mess(message: types.Message):
    # Получим ид пользователя и сравним со списком разрешенных в файле конфига
    user_id = message.from_user.id
    print(f"user_id {user_id}")
    # if user_id == 976374565:
    if user_id in config.users:
        answer = []
        if message.text == "1" or message.text.lower() == "кировский":
            await bot.send_message(message.chat.id, f"Ответ: Кировский")
            answer = get_html(url.url_link_kirov)
        elif message.text == "2" or message.text.lower() == "адмирал":
            await bot.send_message(message.chat.id, f"Ответ: Адмиралтейский")
            answer = get_html(url.url_link_admiral)
        elif message.text == "3" or message.text.lower() == "центр":
            await bot.send_message(message.chat.id, f"Ответ: Центральный")
            answer = get_html(url.url_link_central)
        elif message.text == "4" or message.text.lower() == "парфеновская":
            await bot.send_message(message.chat.id, f"Ответ: Парфеновская")
            answer = get_html(url.url_link_parf)
        elif message.text == "5" or message.text.lower() == "измайловский":
            await bot.send_message(message.chat.id, f"Ответ: Измайловский")
            answer = get_html(url.url_link_izmail)
        elif message.text == "6" or message.text.lower() == "фрунзенский":
            await bot.send_message(message.chat.id, f"Ответ: Фрунзенский")
            answer = get_html(url.url_link_frunz)
        elif message.text == "7" or message.text.lower() == "малая":
            await bot.send_message(message.chat.id, f"Ответ: Малая Митрофаньевская")
            answer = get_html(url.url_link_mitrof)
        elif message.text == "8" or message.text.lower() == "московский":
            await bot.send_message(message.chat.id, f"Ответ: Московский")
            answer = get_html(url.url_link_moscow)
        elif message.text == "9" or message.text.lower() == "петроградка":
            await bot.send_message(message.chat.id, f"Ответ: Петроградский")
            answer = get_html(url.url_link_petr)
        elif message.text == "10" or message.text.lower() == "васька":
            await bot.send_message(message.chat.id, f"Ответ: Василеостровский")
            answer = get_html(url.url_link_vas)
        elif message.text == "11" or message.text.lower() == "мой":
            await bot.send_message(message.chat.id, f"Ответ: Старый Адмирал")
            # Запустим функцию отсортируюущие не нужные мне улицы
            pre_answer = get_html(url.url_link_admiral)
            answer = get_old_admiral(pre_answer)
        elif message.text == "12" or message.text.lower() == "мой2":
            await bot.send_message(message.chat.id, f"Ответ: Тестовый Кировский")
            # Запустим функцию отсортируюущие не нужные мне улицы
            pre_answer = get_html(url.url_link_kirov)
            answer = get_old_admiral(pre_answer)
        elif message.text == "13" or message.text.lower() == "мои":
            await bot.send_message(message.chat.id, f"Ответ: Выставленные на меня")
            # Запустим функцию отсортируюущие не нужные мне улицы
            answer = get_html(url.url_link_my)
        elif message.text == "14" or message.text.lower() == "гончар":
            await bot.send_message(message.chat.id, f"Ответ: Гончар")
            # Запустим функцию отсортируюущие не нужные мне улицы
            answer = get_html(url.url_link_vas_petr)
        else:
            help = "1: Кировский, 2: Адмирал, 3: Центр, 4: Парфеновская, 5: Измайловский, 6: Фрунзенский, 7: Малая М, " \
                   "8: Московский, 9: Петроградка, 10: Васька"
            await bot.send_message(message.chat.id, f"Подсказка: {help}")
            # await bot.send_message(message.chat.id, reply_markup=urlkb)
            # await message.answer("Ссылки", reply_markup=urlkb)

        try:
            if len(answer) > 0:
                # await bot.send_message(message.chat.id, f"Ответ: {mes}")
                for i in answer:
                    # await bot.send_message(message.chat.id, f"Ответ: {answer[x]}")
                    await bot.send_message(message.chat.id, i)
                    # send_telegram(mes[x])
            else:
                print(f"{datetime.now()}: Ремонтов нет")
        except:
            print(f"{datetime.now()}: Ошибка с получением ответа от парсера")
            await bot.send_message(message.chat.id, f"Ответ: Ошибка с получением ответа от парсера")
            # send_telegram(f"Ответ: Ошибка с получением ответа от парсера")
    else:
        await bot.send_message(message.chat.id, "Вы не авторизованны")


def get_old_admiral(all_answer):
    answer = []
    print("start")
    for i in all_answer:
        if i.find("Парфеновская") != -1:
            print("Парфеновская")
        elif i.find("Измайловский") != -1:
            print("Измайловский")
        elif i.find("Малая Митрофаньевская") != -1:
            print("Малая Митрофаньевская")
        else:
            answer.append(i)
    print(len(answer))
    answer.append(f"Всего ремонтов в выбранном районе: {len(answer)}")
    return answer


def get_html(url2):
    try:
        html = session.get(url2)
        answer = ["Больше ничего нету"]  # Ответ боту
        list_repairs_id = []  # Тут храним ИД ремонтов
        if html.status_code == 200:
            soup = BeautifulSoup(html.text, 'lxml')
            table = soup.find_all('tr', class_="cursor_pointer")
            for i in table:  # Цикл по списку всей таблицы
                list_a = i.find_all('a')  # Ищем ссылки во всей таблице
                for ii in list_a:  # Цикл по найденным ссылкам
                    if len(ii.text) == 6 or len(ii.text) == 7:  # Ищем похожесть на ид ремонта, он пока из 6 цифр
                        list_repairs_id.append(ii.text)
            # Перебор полученного списка ремонтов
            if len(list_repairs_id) > 0:
                x = 0  # Счетчик индексов новых ремонтов
                for one_repair_id in list_repairs_id:
                    # Собираем ссылку на сам ремонт
                    repair_link = url.url_link_repair + one_repair_id
                    repair_link = repair_link.strip()
                    td_class_all = table[x].find_all('td', class_="")
                    # print(td_class_all)
                    td_class_div_center_all = table[x].find_all('td', class_="div_center")
                    # TODO необходимо вставить дату и время принятия
                    data_repair = td_class_div_center_all[1]  # Пока не используем
                    # print(f"""data_repair_all: {data_repair}""")
                    # print(f"""data_repair: {data_repair}""")

                    address_repair = td_class_all[0]
                    address_repair_text = address_repair.text.strip()
                    address_split = address_repair_text.split(" ")
                    # Сделаем срез уберем страну и город
                    address_split = address_split[2:]
                    address_msg = ""
                    # for num, value in enumerate(address_split):
                    for i in address_split:
                        if i != '':
                            address_msg += i
                            address_msg += " "
                        else:
                            break

                    # print(f"""address_repair: {address_repair.text}""")
                    print(f"""address_repair: {address_msg}""")
                    # print(f"""address_repair: {address_repair}""")

                    mission_repair = td_class_all[1].b
                    print(f"""mission_repair: {mission_repair.text}""")

                    # comment_repair = table[x].find_all('div', class_="div_journal_opis")
                    comment_repair = td_class_all[1]
                    print(f"comment_repair: {comment_repair.text}")
                    # Комментария может не быть, поэтому делаем проверку
                    # Старый вариант, до обновления Юзера
                    # if len(comment_repair) > 0:
                    #     comment_repair = comment_repair[0].text
                    # else:  # Если коммента нет создаем пустую строку
                    #     comment_repair = " "
                    try:
                        # comment_repair = comment_repair.split("<br/>")
                        # comment_repair = comment_repair.get_text('/n', strip="True")
                        description = comment_repair.text
                        print(f"""description232: {comment_repair.text}""")
                    except AttributeError:
                        description = "Описания нет"

                    print(f"""description123: {description}""")

                    # Тестируем добавление всех комментариев
                    user_comm = url.url_link_comment + one_repair_id
                    one_comment = get_one_comment(user_comm)
                    # print(one_comment)

                    one_repair_text = f"{mission_repair.text}\n\n{address_msg}\n\n" \
                                      f"{description}\n\n{repair_link}\n\n{one_comment}"

                    answer.append(one_repair_text)

                    x += 1

                answer.append(f"Всего ремонтов: {x}")

            answer.reverse()

            return answer
        else:
            print("error")
    except:
        create_sessions()
        return ("Произошла ошибка сессии, бот залогинится снова, "
                "попробуйте выполнить запрос позже, "
                "возможно программа даже не сломалась.")


def get_one_comment(url1):
    html = session.get(url1)
    answer = ["test"]  # Ответ боту
    if html.status_code == 200:
        soup = BeautifulSoup(html.text, 'lxml')
        soup = soup.get_text()
        soup = soup.strip()
        return soup
    return "no comment"


# test_save()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
