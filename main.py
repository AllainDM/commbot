from datetime import datetime, timedelta
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
import to_exel


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
    elif message.text == "000" or message.text == "улицы":
        await bot.send_message(message.chat.id, f"Наши улицы в московском районе: {to_exel.moscow}")
        await bot.send_message(message.chat.id, f"Наши улицы во фрунзенском районе: {to_exel.frunze}")
        await bot.send_message(message.chat.id, f"Наши улицы в кировском районе: {to_exel.kirov}")
        await bot.send_message(message.chat.id, f"И весь список в трех районах: {to_exel.all_street}")
    elif message.text == "0" or message.text == "тест":
        print("Дата")
        date_now = datetime.now()
        start_day = date_now - timedelta(7)
        date_now = date_now.strftime("%d.%m.%Y")
        start_day = start_day.strftime("%d.%m.%Y")
        name_table = f"{start_day} - {date_now}"
        print(start_day)
        print(date_now)
        await bot.send_message(message.chat.id, f"Ответ: Отчет за {name_table}")
        answer = get_html_users(url.url_link_test, date_now, start_day, name_table)
        try:
            exel = open(f"{name_table}.xls", "rb")
            await bot.send_document(message.chat.id, exel)
        except:
            await bot.send_document(message.chat.id, "Возможно найденный файл не найден")
    elif message.text == "00" or message.text == "вчера":  # Тут отчет за один день, предыдущий
        print("Дата")
        date_now = datetime.now()
        start_day = date_now - timedelta(1)
        date_now = start_day.strftime("%d.%m.%Y")
        start_day = start_day.strftime("%d.%m.%Y")
        name_table = f"{date_now}"
        print(start_day)
        print(date_now)
        await bot.send_message(message.chat.id, f"Ответ: Отчет за {name_table}")
        answer = get_html_users(url.url_link_test, date_now, start_day, name_table)
        try:
            exel = open(f"{name_table}.xls", "rb")
            await bot.send_document(message.chat.id, exel)
        except:
            await bot.send_document(message.chat.id, "Возможно найденный файл не найден")
    elif message.text == "00+1" or message.text == "сегодня":  # Тут отчет за один день, предыдущий
        print("Дата")
        date_now = datetime.now()
        date_now = date_now.strftime("%d.%m.%Y")
        start_day = date_now
        name_table = f"{date_now}"
        print(start_day)
        print(date_now)
        await bot.send_message(message.chat.id, f"Ответ: Отчет за {name_table}")
        answer = get_html_users(url.url_link_test, date_now, start_day, name_table)
        try:
            exel = open(f"{name_table}.xls", "rb")
            await bot.send_document(message.chat.id, exel)
        except:
            await bot.send_document(message.chat.id, "Возможно найденный файл не найден")
    elif message.text == "001" or message.text == "неделя1":  # Тут отчет за месяц, с первого по текущее число
        print("Дата")
        now = datetime.now()
        start_day = f"01.{now.month}.{now.year}"
        date_now = f"07.{now.month}.{now.year}"
        name_table = f"{start_day} - {date_now}"
        print(start_day)
        print(date_now)
        await bot.send_message(message.chat.id, f"Ответ: Отчет за {name_table}")
        answer = get_html_users(url.url_link_test, date_now, start_day, name_table)
        try:
            exel = open(f"{name_table}.xls", "rb")
            await bot.send_document(message.chat.id, exel)
        except:
            await bot.send_document(message.chat.id, "Возможно найденный файл не найден")
    elif message.text == "002" or message.text == "неделя2":  # Тут отчет за месяц, с первого по текущее число
        print("Дата")
        now = datetime.now()
        start_day = f"08.{now.month}.{now.year}"
        date_now = f"15.{now.month}.{now.year}"
        name_table = f"{start_day} - {date_now}"
        print(start_day)
        print(date_now)
        await bot.send_message(message.chat.id, f"Ответ: Отчет за {name_table}")
        answer = get_html_users(url.url_link_test, date_now, start_day, name_table)
        try:
            exel = open(f"{name_table}.xls", "rb")
            await bot.send_document(message.chat.id, exel)
        except:
            await bot.send_document(message.chat.id, "Возможно найденный файл не найден")
    elif message.text == "003" or message.text == "неделя3":  # Тут отчет за месяц, с первого по текущее число
        print("Дата")
        now = datetime.now()
        start_day = f"16.{now.month}.{now.year}"
        date_now = f"23.{now.month}.{now.year}"
        name_table = f"{start_day} - {date_now}"
        print(start_day)
        print(date_now)
        await bot.send_message(message.chat.id, f"Ответ: Отчет за {name_table}")
        answer = get_html_users(url.url_link_test, date_now, start_day, name_table)
        try:
            exel = open(f"{name_table}.xls", "rb")
            await bot.send_document(message.chat.id, exel)
        except:
            await bot.send_document(message.chat.id, "Возможно найденный файл не найден")
    elif message.text == "004" or message.text == "неделя4":  # Тут отчет за месяц, с первого по текущее число
        print("Дата")
        now = datetime.now()
        start_day = f"24.{now.month}.{now.year}"
        date_now = f"31.{now.month}.{now.year}"
        name_table = f"{start_day} - {date_now}"
        print(start_day)
        print(date_now)
        await bot.send_message(message.chat.id, f"Ответ: Отчет за {name_table}")
        answer = get_html_users(url.url_link_test, date_now, start_day, name_table)
        try:
            exel = open(f"{name_table}.xls", "rb")
            await bot.send_document(message.chat.id, exel)
        except:
            await bot.send_document(message.chat.id, "Возможно найденный файл не найден")
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

        return answer
    else:
        print("error")


def get_html_users(url3, date_now, start_day, name_table):
    # if date:
    #     pass
    url_link_test2 = f"http://us.gblnet.net/oper/?core_section=customer_list&filter_selector0=adr&" \
                    f"address_unit_selector0%5B%5D=421&address_unit_selector0%5B%5D=426&" \
                    f"address_unit_selector0%5B%5D=2267&address_unit_selector0%5B%5D=0&" \
                    f"filter_selector1=date_connect&date_connect1_value2=1&date_connect1_date1={start_day}&" \
                    f"date_connect1_date2={date_now}&filter_selector2=adr&address_unit_selector2%5B%5D=421&" \
                    f"address_unit_selector2%5B%5D=426&address_unit_selector2%5B%5D=2275&" \
                    f"address_unit_selector2%5B%5D=0&filter_selector3=adr&address_unit_selector3%5B%5D=421&" \
                    f"address_unit_selector3%5B%5D=426&address_unit_selector3%5B%5D=2261&" \
                    f"address_unit_selector3%5B%5D=0&filter_selector4=adr&address_unit_selector4%5B%5D=421&" \
                    f"address_unit_selector4%5B%5D=426&address_unit_selector4%5B%5D=2264&" \
                    f"address_unit_selector4%5B%5D=0&filter_selector5=adr&address_unit_selector5%5B%5D=421&" \
                    f"address_unit_selector5%5B%5D=426&address_unit_selector5%5B%5D=2276&" \
                    f"address_unit_selector5%5B%5D=0&filter_selector6=adr&address_unit_selector6%5B%5D=421&" \
                    f"address_unit_selector6%5B%5D=426&address_unit_selector6%5B%5D=2269&" \
                    f"address_unit_selector6%5B%5D=0&filter_selector7=adr&address_unit_selector7%5B%5D=421&" \
                    f"address_unit_selector7%5B%5D=426&address_unit_selector7%5B%5D=3215&" \
                    f"address_unit_selector7%5B%5D=0&filter_group_by="

    url_link_test = f"http://us.gblnet.net/oper/?core_section=customer_list&filter_selector0=adr&" \
                    f"address_unit_selector0%5B%5D=421&address_unit_selector0%5B%5D=426&" \
                    f"address_unit_selector0%5B%5D=2267&address_unit_selector0%5B%5D=0&filter_selector1=adr&" \
                    f"address_unit_selector1%5B%5D=421&address_unit_selector1%5B%5D=426&" \
                    f"address_unit_selector1%5B%5D=3215&address_unit_selector1%5B%5D=0&filter_selector2=adr&" \
                    f"address_unit_selector2%5B%5D=421&address_unit_selector2%5B%5D=426&" \
                    f"address_unit_selector2%5B%5D=2275&address_unit_selector2%5B%5D=0&filter_selector3=adr&" \
                    f"address_unit_selector3%5B%5D=421&address_unit_selector3%5B%5D=426&" \
                    f"address_unit_selector3%5B%5D=2261&address_unit_selector3%5B%5D=0&filter_selector4=adr&" \
                    f"address_unit_selector4%5B%5D=421&address_unit_selector4%5B%5D=426&" \
                    f"address_unit_selector4%5B%5D=2264&address_unit_selector4%5B%5D=0&filter_selector5=adr&" \
                    f"address_unit_selector5%5B%5D=421&address_unit_selector5%5B%5D=426&" \
                    f"address_unit_selector5%5B%5D=2276&address_unit_selector5%5B%5D=0&filter_selector6=adr&" \
                    f"address_unit_selector6%5B%5D=421&address_unit_selector6%5B%5D=426&" \
                    f"address_unit_selector6%5B%5D=2269&address_unit_selector6%5B%5D=0&filter_selector7=date_add&" \
                    f"date_add7_value2=1&date_add7_date1={start_day}&date_add7_date2={date_now}&filter_group_by="
    print(url_link_test)
    try:
        html = session.get(url_link_test)
        answer = ["Больше ничего нету"]  # Ответ боту
        list_users = []  # Тут храним что-то
        if html.status_code == 200:
            soup = BeautifulSoup(html.text, 'lxml')
            table = soup.find_all('tr', class_="cursor_pointer")
            to_exel.test_save(table, name_table)
            # print(table[0].text)
            # print(type(table[0].text))
            return answer
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
        return soup
    return "no comment"


# test_save()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
