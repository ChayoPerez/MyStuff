import datetime
import json
import os


img_folder = "Interface"

class User:

   current_user = None
   user_folder = "User"

   def __init__(self, name, level, history):
      self.name = name
      self.level = level
      self.history = history

   def update_level(self):
      self.level_up()
      if self.penance_applies:
         self.level_down()
      self.save()

   def level_up(self):
      if self.level > 1:
         self.level -= 1

   def level_down(self):
      if self.level < 50:
         self.level += 1

   def add_entry(self, message):
      self.history.append(Entry(message, Date.get_today()))
      self.update_level()

   def load_user(username):
      with open(os.path.join(User.user_folder, username + ".json")) as  file:
         dictionary = json.load(file)
      name = dictionary["name"]
      level = dictionary["level"]
      history = Entry.load_entries(dictionary)
      User.current_user = User(name, level, history)

   def load_new_user(username):
      name = username
      level = 50
      history = []
      User.current_user = User(name, level, history)
      User.current_user.save()

   def save(self):
      dictionary = {}
      dictionary["name"] = self.name
      dictionary["level"] = self.level
      dictionary["n"] = len(self.history)
      for i in range(0, len(self.history)):
         dictionary[str(i)] = str(self.history[i])
      with open(os.path.join(User.user_folder, self.name + ".json"), "w") as file:
         json.dump(dictionary, file)

   @property
   def penance_applies(self):
      if len(self.history) > 1:
         now = self.history[len(self.history) - 1]
         previous = self.history[len(self.history) - 2]
         if Date.limit_days_since(previous.date, now.date):
            return True
         else:
            return False
      else:
         return False

   def user_exists(username):
      if (username + ".json") in os.listdir(os.path.join(User.user_folder)):
         print("exists")
         return True
      print("does not exist")
      return False

   def valid_username(username):
      if username.isalpha():
         return True
      else:
         return False

   def valid_old_username(username):
      if User.user_exists(username):
         User.load_user(username)
         return True
      else:
         return False

   def valid_new_username(username):
      if User.user_exists(username):
         return False
      elif User.valid_username(username):
         User.load_new_user(username)
         return True
      else:
         return False

   def is_box_open(self):
      if len(self.history) > 0:
         last_entry = self.history[len(self.history) - 1]
         if last_entry.was_this_today():
            return False
         else:
            return True
      else:
         return True

   def get_last_entry(self):
      last_entry = self.history[len(self.history) - 1]
      return last_entry.message

   def edit_last_entry(self, new_message):
      print("edit_last_entry")
      self.history[len(self.history) - 1].message = new_message

   def get_level(self):
      return str(self.level)


class Entry:

   def __init__(self, message, date):
      self.message = message
      self.date = date

   def was_this_today(self):
      return self.date.is_today()

   def convert_to_Entry(text):
      info = text.split(";")
      date_text = info[0]
      date = Date.convert_to_Date(date_text)
      message = info[1]
      return Entry(message, date)

   def load_entries(dictionary):
      history = []
      n = int(dictionary["n"])
      for i in range(0, n):
         history.append(Entry.convert_to_Entry(dictionary[str(i)]))
      return history

   def text(self):
      return str(self.date) + "\n" + self.message

   def __str__(self):
      text = str(self.date) + ";" + self.message
      return text


class Date:

   penance = 2

   def __init__(self, day, month):
      self.month = month
      self.day = day

   def is_today(self):
      today = Date.get_today()
      if self.day == today.day and self.month == today.month:
         return True
      else:
         return False

   def convert_to_Date(text):
      numbers = text.split("/")
      day = int(numbers[0])
      month = int(numbers[1])
      return Date(day, month)

   def get_today():
      today = datetime.datetime.today()
      day = today.day
      month = today.month
      return Date(day, month)

   def days_per_month(month):
      if month == 2:
         return 28
      elif month in [1, 3, 5, 7, 8, 10, 12]:
         return 31
      elif month in [4, 6, 9, 11]:
         return 30

   def limit_days_since(date1, date2):
      if date1.month == date2.month:
         if date2.day > date1.day + Date.penance:
            return True
         else:
            return False
      elif date1.month + 1 < date2.month:
         return True
      elif date1.month + 1 == date2.month:
         month1_days = Date.days_per_month(date1.month)
         days_difference = month1_days - date1.day + date2.day
         if days_difference > Date.penance:
            return True
         else:
            return False

   def __str__(self):
      text = str(self.day) + "/" + str(self.month)
      return text