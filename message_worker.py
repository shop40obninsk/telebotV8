import DB_WORKER
import tele_keyboards
import Sender_message_telegram
import send_order_admin

def keyboard_goods_gen(key,tastes,id_manufacturer,id_good):
    DB=DB_WORKER.DataBase("Data_base_catalog.db")
    mass=[]
    for i in tastes:
        command = str(key) + str(id_manufacturer) + "|" + str(id_good) + "|" + str(i)
        mass.append([str(DB.get_filter("tastes","id",str(i))[0][1]),command])
    DB.close()
    print(mass)
    return mass

def add_order(chat_id,delivery_id,order_list,total):
    order_list_str=""
    for i in order_list:
        type=i[0]
        manufacturer=i[1]
        good_id=i[2]
        taste_id=i[3]
        count=i[4]
        price=i[5]
        order_list_str+=f"{type}|{manufacturer}|{good_id}|{taste_id}|{count}|{price}&"
    order_list_str=order_list_str[:-1]
    print(order_list_str)
    DB=DB_WORKER.DataBase("Data_base_orders.db")
    DB.add("Orders",["chat_id","delivery_id","order_list","total"],[chat_id,delivery_id,order_list_str,total])
    DB.close()


def add_in_Users_Base(chat_id,name):
    url = "https://t.me/" + name
    DB=DB_WORKER.DataBase("Data_base_Users.db")
    if not DB.check_in_base("Users","chat_id",str(chat_id)):
        DB.add("Users",["chat_id","name","url"],[int(chat_id),str(name),str(url)])
    DB.close()

def main_command_worker(bot,message,text):
    keyboard = tele_keyboards.Keyboard_Generator(["Эллектронки", "Испарители", "Жижи", "/Поделиться", "/Корзина"],X=[1, 2, 2])
    Sender_message_telegram.send_message(bot, message, "👇", keyboard=keyboard)
    DB = DB_WORKER.DataBase("Data_base_catalog.db")
    buttons=[]
    type=DB.get_filter("types","name",str(text))[0][0]
    print(type)
    for i in DB.get_filter("manufacturer","type",type):
        buttons.append([str(i[1]),"M"+str(i[0])])
    keyboard=tele_keyboards.Inline_Keyboard_Generator(buttons)
    Sender_message_telegram.send_message(bot,message,"Выбери производителя: ",keyboard=keyboard)
    DB.close()


def inline_buttons_worker(bot,call,text):
    print(text)
    DB = DB_WORKER.DataBase("Data_base_catalog.db")
    if "M" in text:
        code = text.replace("M", "")
        print("M",code)
        manufacturer = DB.get_filter("manufacturer", "id", str(code))[0]
        id_manufacturer, name_manufacturer, type_manufacturer = manufacturer[0], manufacturer[1], manufacturer[2]
        goods = DB.get_filter("goods", "id_manufacturer", str(id_manufacturer))
        goods_plus_tastes_id = []
        for i in goods:
            tastes = []
            for j in DB.get_filter("goods_tastes", "id_good", str(i[0])):
                tastes.append(j[1])
            goods_plus_tastes_id.append([i, tastes])

        buttons_mass=[]
        for i in goods_plus_tastes_id:
            id_good = i[0][0]
            id_manufacturer = i[0][1]
            name_good = i[0][2]
            price_good = i[0][5]
            print(id_good, id_manufacturer, name_good, price_good)
            buttons_mass.append([f"{name_good} {price_good}₽",f"Y{id_good}"])
        print(buttons_mass)
        keyboard=tele_keyboards.Inline_Keyboard_Generator(buttons_mass)
        Sender_message_telegram.delete_message(bot,None,call=call)
        Sender_message_telegram.send_message(bot, None, "Выбери модель", call=call, keyboard=keyboard)

    if "Y" in text:
        Sender_message_telegram.delete_message(bot,None,call=call)
        code=text.replace("Y","")
        print(code)
        goods=DB.get_filter("goods","id",str(code))
        goods_plus_tastes_id=[]
        for i in goods:
            tastes=[]
            for j in DB.get_filter("goods_tastes", "id_good", str(i[0])):
                tastes.append(j[1])
            goods_plus_tastes_id.append([i,tastes])
        #print(goods_plus_tastes_id)

        for i in goods_plus_tastes_id:
            id_good=i[0][0]
            id_manufacturer=i[0][1]
            name_good=i[0][2]
            description_good=i[0][3]
            picture_video_good=str(i[0][4])
            price_good=i[0][5]
            tastes_good=i[1]
            print(id_good,id_manufacturer,name_good,description_good,picture_video_good,tastes_good,price_good)

            buttons=keyboard_goods_gen("G", tastes_good, id_manufacturer, id_good)
            buttons.append(["Назад к моделям", f"M{id_manufacturer}"])
            keyboard=tele_keyboards.Inline_Keyboard_Generator(buttons)
            output_string=str(name_good)+" "+str(price_good)+"₽"+"\n"+str(description_good)

            if picture_video_good!=None:
                Sender_message_telegram.send_photo_video_message(bot,None,output_string,picture_video_good.replace("\\","/"),call=call,keyboard=keyboard)
            else:
                Sender_message_telegram.send_message(bot,None,output_string,call=call,keyboard=keyboard)

    elif "G" in text:
        # [taste,id_manufacturer,id_good]
        chat_id = call.message.chat.id
        text=list(map(int, text.replace("G","").split("|")))
        print("Заказ",text,chat_id)

        User_DB = DB_WORKER.DataBase("Data_base_Users.db")

        type_good=DB.get_filter("manufacturer","id",text[0])[0][2]
        manufacturer_id=text[0]
        good_id=text[1]
        taste_id=text[2]
        print(chat_id, type_good, manufacturer_id, good_id, taste_id)

        a,f=User_DB.check_in_base_basket("basket",chat_id, type_good, manufacturer_id, good_id, taste_id)
        if a:
            print("Update good")
            User_DB.update_in_base("basket","number",str(f[0]),"count", f[6]+1)
        else:
            print("Add in basket")
            User_DB.add("basket",
                        ["chat_id","type","manufacturer_id","good_id","taste_id","count"],
                        [chat_id,type_good,manufacturer_id,good_id,taste_id,1])
        a, f = User_DB.check_in_base_basket("basket", chat_id, type_good, manufacturer_id, good_id, taste_id)
        User_DB.close()
        name=DB.get_filter("goods","id",good_id)[0]
        taste=DB.get_filter("tastes","id",taste_id)[0]
        manufacturer=DB.get_filter("manufacturer","id",manufacturer_id)[0]
        Sender_message_telegram.send_message(bot, None, f"✅{manufacturer[1]} {name[2]} {taste[1]} Добавлено в корзину. \nВ корзине {f[6]} шт этого товара", call=call)

    elif "D" in text:
        try:
            DB=DB_WORKER.DataBase("Data_base_Users.db")
            count_new=int(DB.get_filter("basket","number",text.replace("D",""))[0][6])
            if count_new==1:
                DB.delete_row("basket",["number"],[text.replace("D","")])
            DB.update_in_base("basket","number",text.replace("D",""),"count",count_new-1)
        except:
            pass
        DBU = DB_WORKER.DataBase("Data_base_Users.db")
        chat_id = call.message.chat.id
        count_in_basket=len(DBU.get_filter("basket", "chat_id", str(chat_id)))
        print(count_in_basket)
        id=Sender_message_telegram.send_message(bot,None,"Корзина изменена",call=call)
        try:
            Sender_message_telegram.delete_messages(bot, None,id, count_in_basket+3, call=call)
        except:
            pass
        basket(bot,call.message)

    elif "L" in text:
        delivery_id = text.replace("L", "")
        print(delivery_id)
        chat_id = call.message.chat.id
        numbers=[]
        order_list=[]
        total = 0
        DBU = DB_WORKER.DataBase("Data_base_Users.db")
        if DBU.get_filter("basket", "chat_id", str(chat_id)) != []:
            for i in DBU.get_filter("basket", "chat_id", str(chat_id)):
                numbers.append(i[0])
                type = i[2]
                manufacturer = i[3]
                good_id = i[4]
                taste_id = i[5]
                count = i[6]
                price = DB.get_filter("goods", "id", good_id)[0][5]
                total += int(count) * int(price)
                order_list.append([type,manufacturer,good_id,taste_id,count,price])

            add_order(chat_id,delivery_id,order_list,total)
            send_order_admin.new_order(bot,call,chat_id,delivery_id,order_list,total)
            for i in numbers:
                DBU.delete_row("basket",["number"],[str(i)])
            DBU.close()
            Sender_message_telegram.delete_message(bot,None,call=call)
            keyboard = tele_keyboards.Keyboard_Generator(
                ["Эллектронки", "Испарители", "Жижи", "/Поделиться", "/Корзина"], X=[1, 2, 2])
            Sender_message_telegram.send_message(bot,None,"""Спасибо за заказ, ждем вас снова! 
Не забывайте делиться ботом с друзьями 🥰 
С Новым годом! 🎄🎊""",call=call,keyboard=keyboard)

        else:
            Sender_message_telegram.send_message(bot, call.message, "Корзина пуста")


    DB.close()

def basket(bot,message):
    chat_id=message.chat.id
    total=0
    DBC=DB_WORKER.DataBase("Data_base_catalog.db")
    DBU=DB_WORKER.DataBase("Data_base_Users.db")
    status=True
    if DBU.get_filter("basket", "chat_id", str(chat_id))!=[]:
        for i in DBU.get_filter("basket","chat_id",str(chat_id)):
            if status:
                s = "Товары в вашей корзине: \n"
                status=False
            else:
                s=""
            number=i[0]
            chat_id=i[1]
            type=i[2]
            manufacturer=i[3]
            good_id=i[4]
            taste_id=i[5]
            count=i[6]
            type_name=DBC.get_filter("types","type",type)[0][1]
            manufacturer_name=DBC.get_filter("manufacturer","id",manufacturer)[0][1]
            good_name=DBC.get_filter("goods","id",good_id)[0][2]
            taste_name=DBC.get_filter("tastes","id",taste_id)[0][1]
            price=DBC.get_filter("goods","id",good_id)[0][5]

            s+=f"{type_name}: {manufacturer_name} {good_name} {taste_name} {price}₽ {count}шт.\n"

            keyboard = tele_keyboards.Inline_Keyboard_Generator([["Удалить", f"D{number}"]])
            Sender_message_telegram.send_message(bot,message,s,keyboard=keyboard)
            total+=int(count)*int(price)
    else:
        Sender_message_telegram.send_message(bot, message, "Корзина пуста")

    keyboard=tele_keyboards.Keyboard_Generator(["/Купить","Эллектронки","Испарители","Жижи","/Поделиться","/Корзина"],X=[1, 2, 2,1])
    Sender_message_telegram.send_message(bot, message, f"К оплате {total}₽", keyboard=keyboard)

    DBU.close()
    DBC.close()

def buy(bot,message):
    chat_id = message.chat.id
    total = 0
    DBC = DB_WORKER.DataBase("Data_base_catalog.db")
    DBU = DB_WORKER.DataBase("Data_base_Users.db")
    if DBU.get_filter("basket", "chat_id", str(chat_id)) != []:
        for i in DBU.get_filter("basket", "chat_id", str(chat_id)):
            chat_id = i[1]
            good_id = i[4]
            count = i[6]
            price = DBC.get_filter("goods", "id", good_id)[0][5]
            total += int(count) * int(price)

        print("buy", chat_id)
        DBO = DB_WORKER.DataBase("Data_base_orders.db")
        buttons = []
        for i in DBO.get("delivery"):
            buttons.append([i[1],f"L{i[0]}"])
        keyboard = tele_keyboards.Inline_Keyboard_Generator(buttons)
        Sender_message_telegram.send_message(bot, message, f"Ваш заказ на сумму: {total}₽\nКуда поштового голубя отправить?", keyboard=keyboard)
        DBO.close()

    else:
        Sender_message_telegram.send_message(bot, message, "Корзина пуста")
    DBC.close()
    DBU.close()
