import DB_WORKER
def send_message(bot,message,text,keyboard=None,call=None):
    if call is None:
        chat_id = message.chat.id
    else:
        chat_id = call.message.chat.id
    return bot.send_message(chat_id,text, reply_markup=keyboard).message_id

def replace_message(bot,message,text,keyboard=None,call=None):
    if call is None:
        chat_id = message.chat.id
        message_id=message.message_id
    else:
        chat_id = call.message.chat.id
        message_id=call.message.message_id

    bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text=text,
        reply_markup=keyboard,
        parse_mode='Markdown'
    )

def send_photo_video_message(bot,message,text,path,keyboard=None,call=None):
    if call == None:
        chat_id = message.chat.id
    else:
        chat_id = call.message.chat.id
    if path[-4:]!=".mp4":
        print("photo",path)
        bot.send_photo(chat_id, photo=open(path, 'rb'), caption=text, reply_markup=keyboard)
    else:
        print("video",path)
        bot.send_video(chat_id=chat_id,data=open(path, 'rb'),caption=text, reply_markup=keyboard,supports_streaming=True)


def add_in_Data_Base_message_id(message,call=None):
    if call == None:
        chat_id = message.chat.id
        message_id = message.message_id
    else:
        chat_id = call.message.chat.id
        message_id = call.message.message_id
    DB=DB_WORKER.DataBase("Data_base_Users.db")
    DB.add("messages_id",["chat_id","message_id"],[chat_id,message_id])


def delete_buttons(bot,message,call=None):
    if call == None:
        chat_id = message.chat.id
        message_id = message.message_id
    else:
        chat_id = call.message.chat.id
        message_id = call.message.message_id
    bot.edit_message_reply_markup(chat_id,message_id=message_id)

def delete_message(bot,message,call=None,message_id=None):
    if call is None:
        chat_id = message.chat.id
        if message_id is None:
            message_id = message.message_id
    else:
        chat_id = call.message.chat.id
        if message_id is None:
            message_id = call.message.message_id
    bot.delete_message(chat_id, message_id)

def delete_messages(bot,message,message_id,count,call=None):
    if call is None:
        chat_id=message.chat.id
    else:
        chat_id=call.message.chat.id
    for i in range(message_id - count, message_id):
        bot.delete_message(chat_id, i)