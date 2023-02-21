import requests
from datetime import datetime

from bs4 import BeautifulSoup

import config
import main
# from main import bot_answer

session = requests.Session()

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


def get_html(url):
    html = session.get(url_link_kirov)
    answer = ["test"]  # Ответ боту
    if html.status_code == 200:
        soup = BeautifulSoup(html.text, 'lxml')
        table = soup.find_all('tr', class_="cursor_pointer")
        print(table)

        return answer
    else:
        print("error")


def bot_start(url):
    return get_html(url)
