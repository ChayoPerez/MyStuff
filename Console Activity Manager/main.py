import datetime


class Manager:

   def __init__(self):
      self.menu_text1 = "Activity Manager\n---------------------------\nLevel:"
      self.menu_text2 = ""
      self.menu_text3 = "\nSelected Date:\n"
      self.menu_text4 = ""
      self.menu_text5 = "\nOptions:\n1) Change date\n2) Submit activity\n3) View history"
      self.date = None

   def start_menu(self):
      while True:
         print(self.menu_text1 + self.menu_text2 + self.menu_text3 + self.menu_text4 + self.menu_text5)
         answer = input()
         if answer == "1":
            print()
            self.update_date()
         elif answer == "2":
            print()
            self.submit_activity()
            self.update_level()
         elif answer == "3":
            print()
            self.view_history()

   def update_date(self):
      date = input("Update Date to (Ej: '08/10' day/month): ")
      if not Date.is_date(date):
         print("Invalid format.")
      elif not Date.is_valid_date(date):
         print("Invalid date.")
      else:
         self.date = Date(date)
         print("Date changed.")
      print("\n\n")

   def submit_activity(self):
      pass

   def update_level(self):
      pass

   def view_history(self):
      pass

class Date:

   def __init__(self):
      pass

   def is_date(text):
      if not ("/" in text):
         return False
      values = text.split("/")
      if len(values) != 2:
         return False
      for value in values:
         if len(value) != 2:
            return False
      return True

   def is_valid_date(text):
      return True


manager = Manager()
manager.start_menu()