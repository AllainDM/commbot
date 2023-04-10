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

# Наши улицы в "совместных" районах
moscow = [" Смоленская ул.", " Киевская ул."]
frunze = [" Тосина ул.", " Тамбовская ул."]
kirov = [" Канонерский о-в", " Шотландская ул.", " Двинская ул.", " Оборонная ул.",
           " Севастопольская ул.", " Турбинная ул.", " Гладкова ул."]

all_street = [" Канонерский о-в", " Шотландская ул.", " Двинская ул.", " Оборонная ул.",
              " Севастопольская ул.", " Турбинная ул.", " Гладкова ул.",
              " Тосина ул.", " Тамбовская ул.",
              " Смоленская ул.", " Киевская ул."]


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
        await bot.send_message(message.chat.id, f"Наши улицы в московском районе: {moscow}")
        await bot.send_message(message.chat.id, f"Наши улицы во фрунзенском районе: {frunze}")
        await bot.send_message(message.chat.id, f"Наши улицы в кировском районе: {kirov}")
        await bot.send_message(message.chat.id, f"И весь список в трех районах: {all_street}")
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
    elif message.text == "00" or message.text == "тест00":  # Тут отчет за один день, предыдущий
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
            test_save(table, name_table)
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


def test_save(table, name_table):
    # table = table.reverse()
    # Для разворота можно все сделать в виде списка внутри списка, который и развернуть
    table_list_et = []  # Список для Е телекома
    table_list_tiera = []  # Список для Тиеры
    table_list_at_home = []  # Список для ЭтХоума
    # pact = ''  # Номер договора, объявим заранее для видимости
    wb = xlwt.Workbook()
    ws = wb.add_sheet(f'{name_table}')
    num_string = 1  # Стартовый номер строки для екселя
    prev_date = "0"
    for i in table:
        # e_telecom = "ЕТ"
        brend = "ЕТ"
        one_list = []
        one_list_tiera = []
        one_list_at_home = []
        # Нужно найти элемент с фамилией мастера и номер договора.
        # 2: мастер, 3: номер договора
        td_class_all = i.find_all('td', class_="")
        # print(td_class_all[2].text)
        # print(td_class_all[3].text)
        pact = td_class_all[3].text
        soname = td_class_all[2].text
        soname = soname.split()
        # Без фамилии Тиера, а она нужна
        if not soname:
            soname = [" "]
        # print(soname[0])

        # Тут должна быть дата
        td_class_div_center = i.find_all('td', class_="div_center")
        # По длине даты можно отсортировать лишние задания
        date = td_class_div_center[-1].text
        date = date.split()
        if not date:
            # print(pact)
            if pact[0:2] == "40":
                # e_telecom = "Тиера"
                brend = "Тиера"
            else:
                continue
        elif len(date[0]) == 10:
            # print(f'Длинна в норме {date}: {len(date[0])} ')
            pass
        elif len(date[0]) == 17:
            if date[0][0:2] == "12":
                # e_telecom = "ЭтХоум"
                pact = date[0][0:7]
                date = date[0][7:]
                brend = "ЭтХоум"
            else:
                continue
        else:
            continue
        if not date and soname == " ":
            print("нет ни мастера ни даты")
            continue

        # В ссылках хранится адрес, ищем ссылки
        list_a = i.find_all('a')  # Ищем ссылки во всей таблице
        address = list_a[2].text
        # print(address)
        address = address.split(",")
        # print(address)
        # Отдельно надо разделить номер дома и квартиру
        # print(address)
        address_dom = address[4].split()
        address_dom = address_dom[0]
        if address_dom[-1].isdigit():
            address_dom = address_dom.replace("/", "к")
        else:
            address_dom = address_dom.replace("/", "")
        # print(address_dom[0])
        address_kv = address[-1].split()
        # print(address_kv[-1])

        # Вычеркнем лишние улицы из "совместных" районов
        # Нужен хелп по улицам, ответ бота при запросе. Сделать улицы переменными, может в массиве
        street_is_norm = True
        if " Московский р-н" in address or " Фрунзенский р-н" in address or " Кировский р-н" in address:
            # print(f"Улица {address[3][0:-4]} находится в Московском или Фрунзенском районе")
            for street in all_street:
                # print(street)
                # print(f"Проверяем улицу {street}")
                if street in address:
                    # print(f"Найдена улица {street}, она находится в Московском районе")
                    street_is_norm = True
                    break
                else:
                    # print(f"Найденная улица {street}, НЕЕЕЕЕЕЕЕЕЕ находится в Московском районе")
                    street_is_norm = False
        if not street_is_norm:
            continue

        if brend == "ЕТ":
            one_list.append(brend)  # Бренд
            one_list.append(date)  # Дата
            one_list.append(pact.rstrip())   # Номер договора
            one_list.append(address[3][1:-4])  # Улица
            one_list.append(address_dom)  # Дом
            one_list.append(address_kv[-1])  # Квартира
            one_list.append(soname[0])  # Мастер
            one_list.append(address[2][1:-4])  # Район

            table_list_et.append(one_list)

        elif brend == "Тиера":
            one_list_tiera.append(brend)  # Бренд
            one_list_tiera.append(date)  # Дата
            one_list_tiera.append(pact)  # Номер договора
            one_list_tiera.append(address[3][1:-4])  # Улица
            one_list_tiera.append(address_dom)  # Дом
            one_list_tiera.append(address_kv[-1])  # Квартира
            one_list_tiera.append(soname[0])  # Мастер
            one_list_tiera.append(address[2][1:-4])  # Район

            table_list_tiera.append(one_list_tiera)

        else:
            one_list_at_home.append(brend)  # Бренд
            one_list_at_home.append(date)  # Дата
            one_list_at_home.append(pact)  # Номер договора
            one_list_at_home.append(address[3][1:-4])  # Улица
            one_list_at_home.append(address_dom)  # Дом
            one_list_at_home.append(address_kv[-1])  # Квартира
            one_list_at_home.append(soname[0])  # Мастер
            one_list_at_home.append(address[2][1:-4])  # Район

            table_list_at_home.append(one_list_at_home)

    # Пока не переворачиваем, чтоб удобнее сравнивать
    table_list_et.reverse()
    table_list_tiera.reverse()
    table_list_at_home.reverse()
    for i in table_list_et:
        # Добавим дополнительный пробел если дата увеличилась
        if prev_date != i[1]:
            num_string += 1
            prev_date = i[1]
        ws.write(num_string, 0, i[0])  # Бренд
        ws.write(num_string, 1, i[1])  # Дата
        ws.write(num_string, 2, i[2])  # Номер договора
        ws.write(num_string, 3, i[3])  # Улица
        ws.write(num_string, 4, i[4])  # Дом
        ws.write(num_string, 5, i[5])  # Квартира
        ws.write(num_string, 6, i[6])  # Мастер
        ws.write(num_string, 7, i[7])  # Район
        num_string += 1

    num_string += 1
    for i in table_list_tiera:
        # Добавим дополнительный пробел если дата увеличилась
        if prev_date != i[1]:
            num_string += 1
            prev_date = i[1]
        ws.write(num_string, 0, i[0])  # Бренд
        ws.write(num_string, 1, i[1])  # Дата
        ws.write(num_string, 2, i[2])  # Номер договора
        ws.write(num_string, 3, i[3])  # Улица
        ws.write(num_string, 4, i[4])  # Дом
        ws.write(num_string, 5, i[5])  # Квартира
        ws.write(num_string, 6, i[6])  # Мастер
        ws.write(num_string, 7, i[7])  # Район
        num_string += 1

    num_string += 1
    for i in table_list_at_home:
        # Добавим дополнительный пробел если дата увеличилась
        if prev_date != i[1]:
            num_string += 1
            prev_date = i[1]
        ws.write(num_string, 0, i[0])  # Бренд
        ws.write(num_string, 1, i[1])  # Дата
        ws.write(num_string, 2, i[2])  # Номер договора
        ws.write(num_string, 3, i[3])  # Улица
        ws.write(num_string, 4, i[4])  # Дом
        ws.write(num_string, 5, i[5])  # Квартира
        ws.write(num_string, 6, i[6])  # Мастер
        ws.write(num_string, 7, i[7])  # Район
        num_string += 1

    num_string += 3
    ws.write(num_string, 0, "Версия 006")

    # ws.write(2, 2, xlwt.Formula("A3+B3"))

    wb.save(f'{name_table}.xls')


# test_save()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
