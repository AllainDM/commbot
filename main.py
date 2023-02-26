from datetime import datetime
import os
import time

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
import requests

from bs4 import BeautifulSoup

import parser
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


# # Кнопка ссылка
# urlkb = InlineKeyboardMarkup(row_width=1)
# urlButton = InlineKeyboardButton(text='Кировский', callback_data="address_1")
# urlButton2 = InlineKeyboardButton(text='Адмиралтейский', callback_data="address_2")
# urlkb.add(urlButton, urlButton2)


# @dp.callback_query_handler(Text(startswith="address_"))
# async def www_call(callback: types.CallbackQuery):
#     res = int(callback.data.split("_")[1])
#     print(res)
#     # bot.send_message(message.chat.id, f"Ответ: Центральный")
#     # if res == 1:
#     #     echo_mess_button(1)
#     # if f"{callback.from_user.id}" not in answ:
#     echo_mess_button(callback.from_user.id, res)
#     # await callback.answer()


# def echo_mess_button(message, num):
#     answer = []
#     if num == 1:
#         answer = get_html(url.url_link_kirov)
#     elif num == 2:
#         answer = get_html(url.url_link_admiral)
    # elif message == "3" or message == "Центр":
    #     await bot.send_message(message.chat.id, f"Ответ: Центральный")
    #     answer = get_html(url.url_link_central)
    # elif message == "4" or message == "Парфеновская":
    #     await bot.send_message(message.chat.id, f"Ответ: Парфеновская")
    #     answer = get_html(url.url_link_parf)
    # elif message == "5" or message == "Измайловский":
    #     await bot.send_message(message.chat.id, f"Ответ: Измайловский")
    #     answer = get_html(url.url_link_izmail)
    # elif message == "6" or message == "Фрунзенский":
    #     await bot.send_message(message.chat.id, f"Ответ: Фрунзенский")
    #     answer = get_html(url.url_link_frunz)
    # elif message == "7" or message == "Малая":
    #     await bot.send_message(message.chat.id, f"Ответ: Малая Митрофаньевская")
    #     answer = get_html(url.url_link_mitrof)
    # elif message == "8" or message == "Московский":
    #     await bot.send_message(message.chat.id, f"Ответ: Московский")
    #     answer = get_html(url.url_link_moscow)
    # elif message == "9" or message == "Петроградка":
    #     await bot.send_message(message.chat.id, f"Ответ: Петроградский")
    #     answer = get_html(url.url_link_petr)
    # elif message == "10" or message == "Васька":
    #     await bot.send_message(message.chat.id, f"Ответ: Василеостровский")
    #     answer = get_html(url.url_link_vas)
    # else:
    #     # await bot.send_message(message.chat.id, reply_markup=urlkb)
    #     await message.answer("Ссылки", reply_markup=urlkb)

    # try:
    #     if len(answer) > 0:
    #         # await bot.send_message(message.chat.id, f"Ответ: {mes}")
    #         for i in answer:
    #             # await bot.send_message(message.chat.id, f"Ответ: {answer[x]}")
    #             # await bot.send_message(message, i)
    #             await bot.send_message(message.chat.id, i)
    #             # send_telegram(mes[x])
    #     else:
    #         print(f"{datetime.now()}: Ремонтов нет")
    # except:
    #     print(f"{datetime.now()}: Ошибка с получением ответа от парсера")
    #     await bot.send_message(message.chat.id, f"Ответ: Ошибка с получением ответа от парсера")
    #     # await bot.send_message(message, f"Ответ: Ошибка с получением ответа от парсера")


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


def get_one_comment(url1):
    html = session.get(url1)
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
