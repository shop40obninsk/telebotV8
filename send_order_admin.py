import DB_WORKER
def new_order(bot,call,chat_id,delivery_id,order_list,total):
    DBC = DB_WORKER.DataBase("Data_base_catalog.db")
    DBO = DB_WORKER.DataBase("Data_base_orders.db")
    DBU = DB_WORKER.DataBase("Data_base_Users.db")
    name = call.message.chat.username
    url = "https://t.me/" + name
    S = f"{chat_id} {name} {url}\n"
    for i in order_list:
        type_id = i[0]
        manufacturer = i[1]
        good_id = i[2]
        taste_id = i[3]
        count = i[4]
        price = i[5]
        type_name=DBC.get_filter("types","type",type_id)[0][1]
        manufacturer_name=DBC.get_filter("manufacturer","id",manufacturer)[0][1]
        good_name=DBC.get_filter("goods","id",good_id)[0][2]
        taste_name=DBC.get_filter("tastes","id",taste_id)[0][1]
        S+=f"__________________________\n" \
          f"{type_name}\n" \
          f"{manufacturer_name}\n" \
          f"{good_name}\n" \
          f"{taste_name}\n" \
          f"{count} шт\n" \
          f"{price}₽\n"
    S+=f"###########################\n" \
       f"Тип доставки: {DBO.get_filter('delivery','id',delivery_id)[0][1]}\n" \
       f"Всего на сумму: {total}₽"
    for i in DBU.get("admin_id"):
        if int(i[2])==int(delivery_id) or int(i[2])==0:
            bot.send_message(str(i[1]), S)

    print("@@@@@@@@@@@@@@@@@@@@@@@@@@ ORDER @@@@@@@@@@@@@@@@@@@@@@@@@")
    print(S)
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    DBC.close()
    DBO.close()
    DBU.close()