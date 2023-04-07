from datetime import datetime
import os
import time

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
import requests
import xlrd
import xlwt

from bs4 import BeautifulSoup

import parser
import config
import url
import exel as ex


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


@dp.message_handler()  # commands=['Кировский']
async def echo_mess(message: types.Message):
    answer = []
    if message.text == "1" or message.text == "Кировский":
        await bot.send_message(message.chat.id, f"Ответ: Кировский")
        answer = get_html(url.url_link_kirov)
    elif message.text == "2" or message.text == "Адмирал":
        await bot.send_message(message.chat.id, f"Ответ: Адмиралтейский")
        answer = get_html(url.url_link_admiral)
    elif message.text == "3" or message.text == "Центр":
        await bot.send_message(message.chat.id, f"Ответ: Центральный")
        answer = get_html(url.url_link_central)
    elif message.text == "4" or message.text == "Парфеновская":
        await bot.send_message(message.chat.id, f"Ответ: Парфеновская")
        answer = get_html(url.url_link_parf)
    elif message.text == "5" or message.text == "Измайловский":
        await bot.send_message(message.chat.id, f"Ответ: Измайловский")
        answer = get_html(url.url_link_izmail)
    elif message.text == "6" or message.text == "Фрунзенский":
        await bot.send_message(message.chat.id, f"Ответ: Фрунзенский")
        answer = get_html(url.url_link_frunz)
    elif message.text == "7" or message.text == "Малая":
        await bot.send_message(message.chat.id, f"Ответ: Малая Митрофаньевская")
        answer = get_html(url.url_link_mitrof)
    elif message.text == "8" or message.text == "Московский":
        await bot.send_message(message.chat.id, f"Ответ: Московский")
        answer = get_html(url.url_link_moscow)
    elif message.text == "9" or message.text == "Петроградка":
        await bot.send_message(message.chat.id, f"Ответ: Петроградский")
        answer = get_html(url.url_link_petr)
    elif message.text == "10" or message.text == "Васька":
        await bot.send_message(message.chat.id, f"Ответ: Василеостровский")
        answer = get_html(url.url_link_vas)
    elif message.text == "11" or message.text == "Мой":
        await bot.send_message(message.chat.id, f"Ответ: Старый Адмирал")
        # Запустим функцию отсортируюущие не нужные мне улицы
        pre_answer = get_html(url.url_link_admiral)
        answer = get_old_admiral(pre_answer)
    elif message.text == "12" or message.text == "Мой2":
        await bot.send_message(message.chat.id, f"Ответ: Тестовый Кировский")
        # Запустим функцию отсортируюущие не нужные мне улицы
        pre_answer = get_html(url.url_link_kirov)
        answer = get_old_admiral(pre_answer)
    elif message.text == "13" or message.text == "мои":
        await bot.send_message(message.chat.id, f"Ответ: Выставленные на меня")
        # Запустим функцию отсортируюущие не нужные мне улицы
        answer = get_html(url.url_link_my)
    elif message.text == "14" or message.text == "гончар":
        await bot.send_message(message.chat.id, f"Ответ: Гончар")
        # Запустим функцию отсортируюущие не нужные мне улицы
        answer = get_html(url.url_link_vas_petr)
    elif message.text == "15" or message.text == "тест15":
        await bot.send_message(message.chat.id, f"Ответ: тестим ексель")
        exel = open("example.xls", "rb")
        await bot.send_document(message.chat.id, exel)
    elif message.text == "0" or message.text == "тест":
        await bot.send_message(message.chat.id, f"Ответ: тестим ексель")
        answer = get_html_users(url.url_link_test)
        # answer2 = get_html_users(url.url_link_test2)
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
    # await message.answer(message.text)
    # await message.reply(message.text)  # Ответ с цитатой пользователя
    # В этом варианте сообщение приходит пользователю, если он ранее писал боту, иначе ошибка
    # await bot.send_message(message.chat.id, f"Ответ: НЕТ")


def get_old_admiral(all_answer):
    answer = []
    print("start")
    for i in all_answer:
        if i.find("Парфеновская") != -1:
            print("Двинская")
        elif i.find("Измайловский") != -1:
            print("Канонерский")
        else:
            answer.append(i)
    print(len(answer))
    answer.append(f"Всего ремонтов в выбранном районе: {len(answer)}")
        # return all_answer
    return answer


def get_html(url2):
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
                td_class_all = table[x].find_all('td', class_="")
                # print(td_class_all)
                td_class_div_center_all = table[x].find_all('td', class_="div_center")
                data_repair = td_class_div_center_all[1]  # Пока не используем
                # print(f"""data_repair_all: {data_repair}""")
                # print(f"""data_repair: {data_repair}""")

                address_repair = td_class_all[0]
                address_repair_text = address_repair.text.strip()
                # print(f"""address_repair: {address_repair.text}""")
                # print(f"""address_repair: {address_repair}""")

                mission_repair = td_class_all[1].b
                # print(f"""mission_repair: {mission_repair.text}""")

                comment_repair = table[x].find_all('div', class_="div_journal_opis")
                # print(comment_repair)
                # Комментария может не быть, поэтому делаем проверку
                if len(comment_repair) > 0:
                    comment_repair = comment_repair[0].text
                else:  # Если коммента нет создаем пустую строку
                    comment_repair = " "

                # Тестируем добавление всех комментариев
                user_comm = url.url_link_comment + one_repair_id
                one_comment = get_one_comment(user_comm)
                # print(one_comment)

                one_repair_text = f"{mission_repair.text}\n\n{address_repair_text}\n\n" \
                                  f"{comment_repair}\n\n{repair_link}\n\n{one_comment}"

                answer.append(one_repair_text)

                x += 1

            answer.append(f"Всего ремонтов: {x}")

        answer.reverse()

        # print(list_repairs_id)
        return answer
        # return "ok"
    else:
        print("error")


def get_html_users(url3):
    print(url3)
    try:
        html = session.get(url3)
        answer = ["Больше ничего нету"]  # Ответ боту
        list_users = []  # Тут храним что-то
        if html.status_code == 200:
            # soup = BeautifulSoup(html.text, 'lxml')
            # table = soup.find_all('tr', class_="cursor_pointer")

            # print(table)
            return answer
            # return "ok"
        else:
            print("error")
    except requests.exceptions.TooManyRedirects as e:
        print(f'{url3} : {e}')


def get_one_comment(url1):
    html = session.get(url1)
    answer = ["test"]  # Ответ боту
    if html.status_code == 200:
        soup = BeautifulSoup(html.text, 'lxml')
        soup = soup.get_text()
        soup = soup.strip()
        # print(soup)
        return soup
    return "no comment"


def test_save(table):
    # font0 = xlwt.Font()
    # font0.name = 'Times New Roman'
    # font0.colour_index = 2
    # font0.bold = True

    # style0 = xlwt.XFStyle()
    # style0.font = font0

    # style1 = xlwt.XFStyle()
    # style1.num_format_str = 'D-MMM-YY'

    wb = xlwt.Workbook()
    ws = wb.add_sheet('A Test Sheet')

    ws.write(0, 0, 'Test')
    # ws.write(0, 0, 'Test', style0)
    # ws.write(1, 0, datetime.now(), style1)
    # ws.write(1, 0, datetime.now(), style1)
    ws.write(2, 0, 1)
    ws.write(2, 1, 1)
    ws.write(2, 2, xlwt.Formula("A3+B3"))

    wb.save('example.xls')


# test_save()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
