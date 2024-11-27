import threading
import user_manager, bot

# load user data
user_manager.load_all_users()

# start bot thread
stats_thread = threading.Thread(target=bot.start_polling)
stats_thread.start()

# start user thread
stats_thread = threading.Thread(target=user_manager.start_updating, args=(60*60,))
stats_thread.start()