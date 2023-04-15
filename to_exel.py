import xlrd
import xlwt

# Наши улицы в "совместных" районах
moscow = [" Смоленская ул.", " Киевская ул."]
frunze = [" Тосина ул.", " Тамбовская ул."]
kirov = [" Канонерский о-в", " Шотландская ул.", " Двинская ул.", " Оборонная ул.",
           " Севастопольская ул.", " Турбинная ул.", " Гладкова ул."]

all_street = [" Канонерский о-в", " Шотландская ул.", " Двинская ул.", " Оборонная ул.",
              " Севастопольская ул.", " Турбинная ул.", " Гладкова ул.",
              " Тосина ул.", " Тамбовская ул.",
              " Смоленская ул.", " Киевская ул."]


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
            one_list_tiera.append(pact.rstrip())  # Номер договора
            one_list_tiera.append(address[3][1:-4])  # Улица
            one_list_tiera.append(address_dom)  # Дом
            one_list_tiera.append(address_kv[-1])  # Квартира
            one_list_tiera.append(soname[0])  # Мастер
            one_list_tiera.append(address[2][1:-4])  # Район

            table_list_tiera.append(one_list_tiera)

        else:  # Остальное видимо относится к ЭтХоуму
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
    ws.write(num_string, 0, "Версия 009")

    # ws.write(2, 2, xlwt.Formula("A3+B3"))

    wb.save(f'{name_table}.xls')