from telebot import types
def Keyboard_Generator(buttons,X=None):
    if X==None:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for i in buttons:
            button = types.KeyboardButton(text=i)
            keyboard.add(button)
        return keyboard
    else:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_list=[]
        j=0
        f=0
        for i in buttons:
            button_list.append(i)
            j += 1
            if j>=X[f]:
                keyboard.add(*[types.KeyboardButton(name) for name in button_list])
                button_list=[]
                j=0
                f+=1
        if j!=0:
            keyboard.add(*[types.KeyboardButton(name) for name in button_list])
        return keyboard


def Inline_Keyboard_Generator(buttons,X=None):
    if X==None:
        keyboard = types.InlineKeyboardMarkup()
        for i in buttons:
            button = types.InlineKeyboardButton(i[0], callback_data=i[1])
            keyboard.add(button)
        return keyboard

    else:
        keyboard = types.InlineKeyboardMarkup()
        button_list=[]
        j=0
        f=0
        for i in buttons:
            button_list.append(i)
            j += 1
            if j>=X[f]:
                print(button_list)
                keyboard.add(*[types.InlineKeyboardButton(name[0], callback_data=name[1]) for name in button_list])
                button_list=[]
                j=0
                f+=1
        if j!=0:
            keyboard.add(*[types.InlineKeyboardButton(name[0], callback_data=name[1]) for name in button_list])
        return keyboard