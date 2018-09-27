import datetime
import json
import os


img_folder = "Interface"

class User:

   current_user = None
   user_folder = "User"

   def __init__(self, name, rank, history):
      self.name = name
      self.rank = rank
      self.history = history

   def update_rank(self):
      self.outrank()
      if self.penance_applies:
         self.be_outranked()
      self.save()

   def outrank(self):
      if self.rank > 1:
         self.rank -= 1

   def be_outranked(self):
      if self.rank < 50:
         self.rank += 1

   def add_entry(self, message):
      self.history.append(Entry(message, Date.get_today()))
      self.update_rank()

   def load_user(username):
      with open(os.path.join(User.user_folder, username + ".json")) as  file:
         dictionary = json.load(file)
      name = dictionary["name"]
      rank = dictionary["rank"]
      history = Entry.load_entries(dictionary)
      User.current_user = User(name, rank, history)

   def load_new_user(username):
      name = username
      rank = 50
      history = []
      User.current_user = User(name, rank, history)
      User.current_user.save()

   def save(self):
      dictionary = {}
      dictionary["name"] = self.name
      dictionary["rank"] = self.rank
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
         return True
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

   def not_used_username(username):
      if User.user_exists(username):
         return False
      else:
         return True

   def well_written_username(username):
      if User.valid_username(username):
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

   def get_rank(self):
      return str(self.rank)

   # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
   def add_past_entry(self, message, day, month):
      self.history.append(Entry(message, Date.get_today()))
      self.sort_entries()
      self.reset_rank()
      self.save()

   def reset_rank(self):
      chrono_entries = self.history[::-1]
      rank = 50
      for i in range(0, len(chrono_entries)):
         if i == 0:
            rank -= 1
         else:
            previous = chrono_entries[i - 1]
            if not Date.limit_days_since(chrono_entries[i].date, previous.date):
               rank += 1
      self.rank = rank

   def sort_entries(self):
      self.history = sorted(self.history, key=get_date)[::-1]


class Entry:

   entry_width = 45

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
      paragraphs = self.message.split("\n")
      corrected = []
      for p in paragraphs:
         corrected.append(to_paragraph(p))
      return str(self.date) + "\n" + "\n".join(corrected)

   def __str__(self):
      text = str(self.date) + ";" + self.message
      return text


class Date:

   penance = 3

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

   def is_day(day):
      if day > 0 and day < 32:
         return True
      else:
         return False

   def is_month(month):
      if month > 0 and month < 13:
         return True
      else:
         return False

   def is_a_date(self, day, month):
      if day <= Date.days_per_month(month):
         return True
      else:
         return False

   def __str__(self):
      day_str = str(self.day)
      month_str = str(self.month)
      if self.day < 10:
         day_str = "0" + day_str
      if self.month < 10:
         month_str = "0" + month_str
      text = day_str + "/" + month_str
      return text

   def __lt__(self, other): #self happened more recently than "other"
      if other.month < self.month:
         return True
      elif other.month > self.month:
         return False
      else:
         if other.day < self.day:
            return True
         elif other.day > self.day:
            return False
         else:
            print("why am I comparing equal dates? {0} == {1}".format(str(self), str(other)))
            return True


def to_paragraph(text):
   entry_width = Entry.entry_width
   words = text.split(" ")
   lines = []
   current_line = ""
   for word in words:
      if len(current_line + " " + word) <= entry_width:
         if len(current_line) == 0:
            current_line = word
         else:
            current_line += " " + word

      else:
         if len(current_line) == 0:
            current_line = word
            lines.append(current_line)
            current_line = ""
         else:
            lines.append(current_line)
            current_line = word

      if word == words[-1]:
         lines.append(current_line)

   spaced_message = "\n".join(lines)

   return spaced_message

def get_date(entry):
   return entry.date