import telebot, time
import user_manager

# instantiate the bot
bot = telebot.TeleBot('7101327062:AAEvtuszotRYX88OyPiTlsD0ljvT9DeMlZw')

# Handle the '/start' command
@bot.message_handler(commands=['start', 'save', 'load', 'send', 'list_users'])
def send_welcome(message):
    user_id = message.from_user.id
    
    if message.text == "/start":
        if not user_id in user_manager.users:
            bot.send_message(message.chat.id, "Малой, я вижу ты еще не в системе. Пора это исправить. Пиши !add 1 [твое имя] [твой стрик на данный момент]\nЕсли есть вопросы по командам пиши !add 0")
        else:
            bot.send_message(message.chat.id, "Ты в системе, пиши !add 0")
    elif message.text == "/save" and user_id == 1246641675:
        user_manager.save_all_users()
    elif message.text == "/load" and user_id == 1246641675:
        user_manager.load_all_users()
    elif message.text.split()[0] == "/send":
        bot.send_message(int(message.text.split()[1]), " ".join(message.text.split()[2:]))
    elif message.text == "/list_users" and user_id == 1246641675:
        user_manager.update_all_users()
        sorted_users = sorted(user_manager.users.values(), key=lambda user: user.streak, reverse=True)
        leaderboard = ""
        for i in range(min(32, len(user_manager.users))):
            _user = sorted_users[i]
            leaderboard += f"{i+1} | {_user.name} | id: {int(_user.user_id)}\n"
        bot.send_message(message.chat.id, leaderboard)
        
    


# !add
@bot.message_handler(content_types=['text'])
def send_message(message):
    user_id = message.from_user.id
    message_compontents = message.text.split()
    if message_compontents[0] == "!add" and len(message_compontents) > 1:
        if message_compontents[1] == "0":
            bot.send_message(message.chat.id, "!add 0 - информация по командам\n!add 1 - вход в систему, или ресет аккаунта\n!add 2 - посмотреть стрик и ранк\n!add 3 - лидерборд\n!add 4 - сменить имя")
        
        elif message_compontents[1] == "1" and len(message_compontents) == 4 and message_compontents[3].isdigit():
            user_manager.add_user(user_id=user_id, name=message_compontents[2], streak=int(message_compontents[3]))
            bot.send_message(message.chat.id, "Пиши !add 2")
        
        elif message_compontents[1] == "2" and user_id in user_manager.users:
            send_user_stats(message.chat.id, user_id)

        elif message_compontents[1] == "3" and user_id in user_manager.users:
            send_leaderboard(message.chat.id)
        
        elif message_compontents[1] == "4"  and len(message_compontents) == 3 and user_id in user_manager.users:
            user_manager.users[user_id].name = message_compontents[2]
            bot.send_message(message.chat.id, "Обновлено")

def send_user_stats(chat_id, user_id):
    _user = user_manager.users[user_id]
    _user.update()
    percentage_to_next_rank = (_user.streak - user_manager.rank_to_streak(_user.rank)) / (user_manager.rank_to_streak(_user.rank + 1) - user_manager.rank_to_streak(_user.rank))
    bar = f"|{"█" * int(10*percentage_to_next_rank)}{"░"*int(10*(1-percentage_to_next_rank))}| - {percentage_to_next_rank*100:.0f}%"
    caption = f"{_user.name}\nСтрик: {_user.streak:.2f}\nРанк: {_user.rank}\n{bar}"
    with open('ranks/' + str(_user.rank) + '.png', 'rb') as photo:
        bot.send_photo(chat_id, photo, caption=caption)

def send_leaderboard(chat_id):
    user_manager.update_all_users()
    sorted_users = sorted(user_manager.users.values(), key=lambda user: user.streak, reverse=True)
    leaderboard = ""
    for i in range(min(32, len(user_manager.users))):
        _user = sorted_users[i]
        leaderboard += f"{i+1} | {_user.name} | стрик: {int(_user.streak)} | ранк: {_user.rank}/150\n"
    bot.send_message(chat_id, leaderboard)

def error_message(text):
    bot.send_message(1246641675, text)

# Start the bot (polling)
def start_polling():
    try:
        bot.polling(none_stop=True, timeout=120)  # Start polling only once
    except Exception as e:
        error_message(str(e))
        bot.stop_polling()
        time.sleep(10)  # Sleep for a while before restarting polling
        start_polling()  # Restart polling when an error occurs
