import datetime, json, os, time

user_data_dir = "saved_data/users/"

def streak_to_rank(streak):
    return int(9.02 * (streak ** 0.625))

def rank_to_streak(rank):
    return ((1/9.02) * rank) ** 1.6

users = {} # save users with their user_id
class User():
    def __init__(self, user_id, name="", streak=0):
        self.user_id = user_id
        self.name = name
        self.start_time = datetime.datetime.now() - datetime.timedelta(days=streak)
        self.streak = streak
        self.rank = 0
    
    # save
    def save_all(self):
        self.save_name()
        self.save_start_time()
        self.save_rank()

    def save_name(self):
        with open(user_data_dir + str(self.user_id) + '.json', 'w') as file:
            json.dump(self.name, file)
    
    def save_start_time(self):
        with open(user_data_dir + str(self.user_id) + '_start_time.json', 'w') as file:
            json.dump(str(self.start_time), file)  # Convert datetime to string before saving
    
    def save_rank(self):
        with open(user_data_dir + str(self.user_id) + '_rank.json', 'w') as file:
            json.dump(self.rank, file)
    
    # load
    def load_all(self):
        self.load_name()
        self.load_start_time()
        self.load_rank()

    def load_name(self):
        try:
            with open(user_data_dir + str(self.user_id) + '.json', 'r') as file:
                self.name = json.load(file)
        except FileNotFoundError:
            print(f"No name file found for user {self.user_id}.") # TODO: add function

    def load_start_time(self):
        try:
            with open(user_data_dir + str(self.user_id) + '_start_time.json', 'r') as file:
                start_time_str = json.load(file)
                self.start_time = datetime.datetime.fromisoformat(start_time_str)  # Convert ISO string back to datetime
        except FileNotFoundError:
            print(f"No start_time file found for user {self.user_id}.")

    def load_rank(self):
        try:
            with open(user_data_dir + str(self.user_id) + '_rank.json', 'r') as file:
                self.rank = json.load(file)
        except FileNotFoundError:
            print(f"No rank file found for user {self.user_id}.")
    

    def update(self):
        self.streak = (datetime.datetime.now() - self.start_time).total_seconds() / (60 * 60 * 24)
        self.rank = streak_to_rank(self.streak)


def add_user(user_id, name="", streak=0):
    new_user = User(user_id=user_id, name=name, streak=streak)
    # new_user.load_all()
    # if not user_id in users:
    #     users[user_id] = new_user
    # else:
    #     bot.error_message(f"User already exists: {user_id}.")
    users[user_id] = new_user

def save_all_users():
    for user_id, user, in users.items():
        user.save_all()

def load_all_users():
    for filename in os.listdir(user_data_dir):
        if filename.endswith(".json") and "_start_time" not in filename and "_rank" not in filename:
            user_id = int(filename.replace(".json", ""))
            new_user = User(user_id=user_id)
            new_user.load_all()
            users[user_id] = new_user

def update_all_users():
    for user_id, user, in users.items():
        user.update()


def start_updating(interval_seconds=60*60):
    while True:
        update_all_users()
        save_all_users()
        time.sleep(interval_seconds)