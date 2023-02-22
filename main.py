from datetime import datetime
import os
import time

from aiogram import Bot, Dispatcher, executor, types
import requests

from bs4 import BeautifulSoup

import parser
import config


session = requests.Session()

bot = Bot(token=config.BOT_API_TOKEN)
dp = Dispatcher(bot)

url_login = "http://us.gblnet.net/oper/"

url_with_filter = "http://us.gblnet.net/oper/?core_section=task_list&filter_selector0=task_state&task_state0_value=" \
                  "1&filter_selector1=task_staff&employee_find_input=&employee_id1=877"

url_link_repair = "http://us.gblnet.net/oper/?core_section=task&action=show&id="

url_link_comment = "http://us.gblnet.net/oper/?core_section=task&action=comment_list&id="

url_link_kirov = "http://us.gblnet.net/oper/?core_section=task_list&filter_selector0=task_state&task_state0_value=" \
                 "1&filter_selector1=task_staff&employee_find_input=&employee_id1=877&filter_selector2=" \
                 "adr&address_unit_selector2%5b%5d=421&address_unit_selector2%5b%5d=426&address_unit_selector2%5b%5d=" \
                 "2264&address_unit_selector2%5b%5d=0"

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
    if message.text == "1":
        await bot.send_message(message.chat.id, f"Ответ: Кировский")
        # answer = parser.bot_start(url_link_kirov)
        answer = get_html(url_link_kirov)
    elif message.text == "2":
        await bot.send_message(message.chat.id, f"Ответ: Тоже кировский")
        # answer = parser.bot_start(url_link_kirov)
        answer = get_html(url_link_kirov)

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


def get_html(url):
    html = session.get(url)
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
                repair_link = url_link_repair + one_repair_id
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
                # comment_repair.appe
                # Комментария может не быть, поэтому делаем проверку
                if len(comment_repair) > 0:
                    # print(f"""comment_repair: {comment_repair}""")
                    # print(f"""comment_repair: {comment_repair[0]}""")
                    # print(f"""comment_repair: {comment_repair[0].text}""")
                    comment_repair = comment_repair[0].text
                else:  # Если коммента нет создаем пустую строку
                    comment_repair = " "

                # Тестируем добавление всех комментариев
                user_comm = url_link_comment + one_repair_id
                one_comment = get_one_comment(user_comm)
                print(one_comment)

                one_repair_text = f"{mission_repair.text}\n\n{address_repair_text}\n\n" \
                                  f"{comment_repair}\n\n{repair_link}\n\n{one_comment}"

                answer.append(one_repair_text)

                x += 1

            answer.append(f"Всего ремонтов: {x}")

        answer.reverse()

        print(list_repairs_id)
        return answer
        # return "ok"
    else:
        print("error")


def get_one_comment(url):
    html = session.get(url)
    answer = ["test"]  # Ответ боту
    if html.status_code == 200:
        soup = BeautifulSoup(html.text, 'lxml')
        soup = soup.get_text()
        soup = soup.strip()
        print(soup)
        return soup
    return "no comment"


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
