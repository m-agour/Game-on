import json
import datetime

class System:
    def __init__(self):
        self.evaluated = False
        self.user = "Demon Phrixus"
        self.password = "dma"
        self.database_file = "Database.json"
        self.history_file = "history.json"
        self.min_points = 10
        self.today_points = 0
        self.in_progress_tasks = []
        self.completed_tasks = []
        self.bought_rewards = []
        self.finished = False
        self.initialized = False
        self.locked = False
        self.credit = 0
        self.date = str(datetime.date.today())
        self.tasks = json.load(open("tasks.json"))
        self.rewards = json.load(open("store.json"))

    def load_database(self):
        data = json.load(open(self.database_file))
        for i in data.keys():
            if i not in ["tasks", "rewards"]:
                self.__dict__[i] = data[i]

    def save_to_database(self):
        d = self.__dict__.copy()
        json.dump(d, open(self.database_file, "w"))

    def save_today(self):
        with open(self.history_file) as history_file:
            history = json.load(history_file)
            d = self.__dict__.copy()
            history[str(datetime.datetime.now())[:19]] = d
            json.dump(history, open(self.history_file, "w"))

    def can_buy(self, something):
        return True if self.credit >= self.rewards[something] else False

    def buy(self, something):
        self.bought_rewards.append(something)
        self.credit -= self.rewards[something]
        return f"Bought {something} successfully!"

    def register_task(self, task):
        self.in_progress_tasks.append(task)
        tmp = 0
        for i in self.in_progress_tasks:
            tmp += self.tasks[i]
        if tmp >= self.min_points:
            self.initialized = True

    def finished_task(self, task):
        if self.initialized:
            self.completed_tasks = self.in_progress_tasks.pop(task)
            return True
        else:
            return False

    def is_new_day(self):
        self.save_to_database()
        # if not self.in_progress_tasks and self.initialized:
        #     self.finished = True
        #     #     do something
        # else:
        #     self.finished = False

        if self.date != str(datetime.date.today()):

            return True

        else:
            return False

    def new_day(self):
        self.date = str(datetime.date.today())
        self.save_today()
        self.evaluate_day()
        self.initialized = False
        self.locked = False
        self.save_to_database()

    def evaluate_day(self):
        collected = 0
        for i in self.completed_tasks:
            collected += self.tasks[i]
        self.completed_tasks = []
        self.in_progress_tasks = []

        day_sum = collected - self.min_points
        print(day_sum)
        if day_sum >= 0:
            # success
            self.credit += 3 + day_sum
        else:
            self.credit += day_sum
            if self.credit < 0:
                self.credit = 0

    def get_tasks_list(self):
        return list(self.tasks.keys())

    def get_items_list_price(self):
        return list(map(lambda x, y: "(" + str(y) + ")" + "  " + x, self.tasks.keys(), self.tasks.values()))

    def get_rewards_list_price(self):
        return list(map(lambda x, y: "(" + str(y) + ")" + "  " + x, self.rewards.keys(), self.rewards.values()))

    def get_rewards_list(self):
        return list(self.rewards.keys())

    def get_in_progress_credits(self):
        return sum([self.tasks[i] for i in self.in_progress_tasks])

    def get_completed_credits(self):
        return sum([self.tasks[i] for i in self.completed_tasks])

