import sys
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QLineEdit, QPushButton, QTextEdit
from PyQt5.QtCore import QCoreApplication, Qt, QSize, pyqtSignal, pyqtSlot, QObject
from PyQt5.QtGui import QPixmap, QFont, QIcon
from SystemModule import User
from SystemModule import img_folder
import os


class MainWindow (QWidget):

   def __init__(self):
      super().__init__()
      self.setWindowTitle('Activity Manager')
      self.setGeometry(100, 100, 480, 500)

      self.user = None
      self.menu = Menu(self)
      self.sign_in_window = EnterName(self)
      self.init_gui()

   def keyPressEvent(self, event):
      key_code = event.key()
      if key_code == 16777220:
         if self.sign_in_window.active:
            self.sign_in_window.press_enter()

   def mousePressEvent(self, event):
      x = event.pos().x()
      y = event.pos().y()
      if self.menu.active:
         self.menu.press_mouse(x, y)

   def init_gui(self):
      self.show()
      self.sign_in_window.show()

   def enter_main_menu(self):
      self.sign_in_window.hide()
      self.menu.set()

   def close_app(self):
      pass

   def open_history(self):
      self.history_viewer = HistoryViewer()


class WindowManager:

   def __init__(self, main_window):
      self.main_window = main_window
      self.objects = []
      self.active = False
      self.init_gui()

   def init_gui(self):
      pass

   def width(self):
      return self.main_window.width()

   def show(self):
      self.active = True
      for obj in self.objects:
         obj.show()

   def hide(self):
      self.active = False
      for obj in self.objects:
         obj.hide()


class EnterName (WindowManager):

   def init_gui(self):
      self.title = QLabel("Welcome to ActivityManager!", self.main_window)
      font = QFont()
      font.setPointSize(17)
      self.title.setFont(font)
      self.title.move(15, 10)

      self.sign_in_msg = QLabel("Username:", self.main_window)
      font = QFont()
      font.setPointSize(12)
      self.sign_in_msg.setFont(font)
      self.sign_in_msg.move(20, 60)
      self.sign_in_box = QLineEdit(self.main_window)
      font = QFont()
      font.setPointSize(10)
      self.sign_in_box.setFont(font)
      self.sign_in_box.setFixedWidth(280)
      self.sign_in_box.move(20, 100)
      self.button_sign_in = QPushButton("ENTER", self.main_window)
      self.button_sign_in.clicked.connect(self.enter_username)
      font = QFont()
      font.setPointSize(8)
      self.button_sign_in.setFont(font)
      self.button_sign_in.setFixedHeight(self.sign_in_box.height())
      self.button_sign_in.move(335, 100)

      self.new_acc_msg = QLabel("Create new account:", self.main_window)
      font = QFont()
      font.setPointSize(12)
      self.new_acc_msg.setFont(font)
      self.new_acc_msg.move(20, 143)
      self.new_acc_box = QLineEdit(self.main_window)
      font = QFont()
      font.setPointSize(10)
      self.new_acc_box.setFont(font)
      self.new_acc_box.setFixedWidth(280)
      self.new_acc_box.move(20, 183)
      self.button_new_acc = QPushButton("ENTER", self.main_window)
      self.button_new_acc.clicked.connect(self.enter_new_account)
      font = QFont()
      font.setPointSize(8)
      self.button_new_acc.setFont(font)
      self.button_new_acc.setFixedHeight(self.new_acc_box.height())
      self.button_new_acc.move(335, 183)

      calendar_img = QPixmap(os.path.join("Interface", "calendar.png"))
      calendar_img = calendar_img.scaled(300, 300, Qt.KeepAspectRatio)
      self.calendar_label = QLabel(self.main_window)
      self.calendar_label.setPixmap(calendar_img)
      self.calendar_label.move(80, 210)

      self.objects.append(self.title)
      self.objects.append(self.sign_in_msg)
      self.objects.append(self.sign_in_box)
      self.objects.append(self.button_sign_in)
      self.objects.append(self.new_acc_msg)
      self.objects.append(self.new_acc_box)
      self.objects.append(self.button_new_acc)
      self.objects.append(self.calendar_label)

      self.hide()

   def process_new_username(self, username):
      if not User.not_used_username(username):
         self.error = ExistentUserError()
         print("ya usado")
      elif not User.well_written_username(username):
         self.error = InvalidNameError()
         print("no es valido")
      else:
         User.load_new_user(username)
         self.main_window.user = User.current_user
         self.main_window.enter_main_menu()

   def process_old_username(self, username):
      if User.valid_old_username(username):
         print("usuario valido")
         User.load_user(username)
         self.main_window.user = User.current_user
         self.main_window.enter_main_menu()
      else:
         self.error = InexistentUserError()
         print("no hay un usuario llamado asi")

   def enter_new_account(self):
      print("new")
      username = self.new_acc_box.text()
      print(username)
      self.process_new_username(username)

   def enter_username(self):
      print("old")
      username = self.sign_in_box.text()
      print(username)
      self.process_old_username(username)

   def press_enter(self):
      print("enter was pressed")
      new_username = self.new_acc_box.text()
      old_username = self.sign_in_box.text()
      if new_username == "" and old_username != "":
         self.process_old_username(old_username)
      elif new_username != "" and old_username == "":
         self.process_new_username(new_username)
      else:
         print("invalid enter")


class ErrorMessage (QWidget):

   def __init__(self):
      super().__init__()
      self.setWindowTitle('Error')
      self.setGeometry(100, 100, 300, 200)
      self.init_gui()

   def init_gui(self):
      self.message = QLabel(self)
      self.message.move(20, 20)
      font = QFont()
      font.setPointSize(10)
      self.message.setFont(font)

      self.close_button = QPushButton("Close", self)
      self.close_button.clicked.connect(self.close_window)
      self.close_button.move(give_position(self.width(), self.close_button.width()), 135)
      self.close_button.show()
      self.show()

   def close_window(self):
      self.close()

   def keyPressEvent(self, event):
      key_code = event.key()
      if key_code == 16777220:
         self.close_window()


class InvalidNameError (ErrorMessage):

   def init_gui(self):
      super().init_gui()
      self.message.setText("This username is not valid.\nUsernames can only contain\nletters (a-z).")
      self.message.resize(self.message.sizeHint())


class InexistentUserError (ErrorMessage):

   def init_gui(self):
      super().init_gui()
      self.message.setText("That username does not\nexist!")
      self.message.resize(self.message.sizeHint())


class ExistentUserError (ErrorMessage):

   def init_gui(self):
      super().init_gui()
      self.message.setText("Unfortunately, that\nusername is already taken!")
      self.message.resize(self.message.sizeHint())


class Menu (WindowManager):

   valid_entry_length = 100

   def init_gui(self):

      self.title = QLabel("Menu", self.main_window)
      font = QFont()
      font.setPointSize(17)
      self.title.setFont(font)
      self.title.move(15, 10)

      self.info_img = QPixmap(os.path.join("Interface", "Info_icon.png"))
      self.info_img = self.info_img.scaled(25, 25, Qt.KeepAspectRatio)
      self.more_information = QLabel(self.main_window)
      self.more_information.setPixmap(self.info_img)
      self.more_information.move(110, 20)

      self.instruction = QLabel("To register your progress enter a comment\nbellow and hit SUBMIT!", self.main_window)
      font = QFont()
      font.setPointSize(10)
      self.instruction.setFont(font)
      self.instruction.setFixedWidth(445)
      self.instruction.move(15, 65)

      calendar_img = QPixmap(os.path.join("Interface", "calendar.png"))
      calendar_img = calendar_img.scaled(75, 75, Qt.KeepAspectRatio)
      calendar_icon = QIcon()
      calendar_icon.addPixmap(calendar_img)
      self.change_date_button = QPushButton(self.main_window)
      self.change_date_button.clicked.connect(self.change_date)
      self.change_date_button.setIcon(calendar_icon)
      self.change_date_button.resize(self.change_date_button.sizeHint())
      self.change_date_button.move(15, 121)

      self.enter_text = MyTextEditor(self)
      self.enter_text.setFont(font)
      self.enter_text.setFixedWidth(445)
      self.enter_text.setFixedHeight(175)
      self.enter_text.move(15, 165)

      font = QFont()
      font.setPointSize(11)

      self.submit_button = QPushButton("Submit", self.main_window)
      self.submit_button.clicked.connect(self.submit)
      self.submit_button.setFont(font)
      self.submit_button.resize(self.submit_button.sizeHint())
      self.submit_button.move(give_position(self.width(), self.submit_button.width()), 370)

      self.edit_button = QPushButton("Submit", self.main_window)
      self.edit_button.setText("Edit")
      self.edit_button.clicked.connect(self.edit)
      self.edit_button.setFont(font)
      self.edit_button.resize(self.edit_button.sizeHint())
      self.edit_button.move(give_position(self.width(), self.edit_button.width()), 370)
      self.edit_button.hide()

      self.open_history_button = QPushButton("  View History  ", self.main_window)
      self.open_history_button.clicked.connect(self.open_history)
      self.open_history_button.setFont(font)
      self.open_history_button.resize(self.open_history_button.sizeHint())
      self.open_history_button.move(give_position(self.width(), self.open_history_button.width()), 430)

      font = QFont()
      font.setPointSize(13)
      self.notice = QLabel("Entry already posted.", self.main_window)
      self.notice.setStyleSheet('color: red')
      self.notice.setFont(font)
      self.notice.move(150, 14)
      self.notice.hide()

      font = QFont()
      font.setPointSize(12)
      self.rank = QLabel("Rank #", self.main_window)
      self.rank.setFont(font)
      self.rank.setFixedWidth(300)
      self.rank.move(17, 430)

      font = QFont()
      font.setPointSize(10)
      self.char_count = QLabel("0/" + str(Menu.valid_entry_length), self.main_window)
      self.char_count.setFont(font)
      self.char_count.move(405, 347)
      # que cambie de posicion según crece el primer numero

      self.objects.append(self.title)
      self.objects.append(self.more_information)
      self.objects.append(self.instruction)
      self.objects.append(self.enter_text)
      self.objects.append(self.submit_button)
      self.objects.append(self.open_history_button)
      self.objects.append(self.rank)
      self.objects.append(self.char_count)
      self.objects.append(self.change_date_button)

      self.hide()

   def set(self):
      self.hide()
      self.open = self.main_window.user.is_box_open()
      if self.rank.text() == "Rank #":
         self.rank.setText("Rank #" + self.main_window.user.get_rank())
      if not self.open:
         self.enter_text.setText(self.main_window.user.get_last_entry())
         self.set_char_count()
         if not (self.notice in self.objects):
            self.objects.remove(self.submit_button)
            self.objects.append(self.notice)
            self.objects.append(self.edit_button)
            self.rank.setText("Rank #" + self.main_window.user.get_rank())
      self.show()

   def set_char_count(self):
      text = self.enter_text.toPlainText()
      self.char_count.setText(str(len(text)) + "/" + str(Menu.valid_entry_length))
      self.char_count.resize(self.char_count.sizeHint())
      if len(text) <= Menu.valid_entry_length:
         self.char_count.setStyleSheet('color: black')
      else:
         self.char_count.setStyleSheet('color: red')

   def press_key(self):
      text = self.enter_text.toPlainText()
      #print(text, len(text))
      if len(text) <= Menu.valid_entry_length:
         self.enter_text.setStyleSheet('color: black')
      else:
         self.enter_text.setStyleSheet('color: red')
      self.set_char_count()

   def submit(self):
      print("submit")
      text = self.enter_text.toPlainText()
      if len(text) <= Menu.valid_entry_length:
         self.main_window.user.add_entry(text)
         self.set()
      else:
         print("too long!")

   def edit(self):
      print("edit")
      text = self.enter_text.toPlainText()
      if len(text) <= Menu.valid_entry_length:
         self.main_window.user.edit_last_entry(text)
         self.set()
      else:
         print("too long!")

   def open_history(self):
      print("open history")
      self.main_window.open_history()

   def open_info(self):
      print("info requested")
      self.info = Info()

   def change_date(self):
      self.selector = SelectDate(self)

   def press_mouse(self, x, y):
      info_x = self.more_information.x()
      info_y = self.more_information.y()
      #print(info_x, info_y)
      width = self.info_img.width()
      if x >= info_x and x < (info_x + width) and y >= info_y and y < (info_y + width):
         self.open_info()
      else:
         pass


class Info (QWidget):

   def __init__(self):
      super().__init__()
      self.setWindowTitle('More information')
      self.setGeometry(100, 100, 300, 400)
      self.init_gui()

   def init_gui(self):

      font = QFont()
      font.setPointSize(10)
      text = "this it\nso much\ninfo i can't belive it"
      self.information = QLabel(text, self)
      self.information.setFont(font)
      self.information.resize(self.information.sizeHint())
      self.information.move(20, 20)
      self.information.show()

      self.close_button = QPushButton("Close", self)
      self.close_button.clicked.connect(self.close_window)
      self.close_button.move(give_position(self.width(), self.close_button.width()), 300)
      self.close_button.show()

      self.show()


   def close_window(self):
      self.close()

   def keyPressEvent(self, event):
      key_code = event.key()
      if key_code == 16777220:
         self.close_window()


class SelectDate(QWidget):

   def __init__(self, manager):
      super().__init__()
      self.setWindowTitle('Select Date')
      self.setGeometry(100, 100, 120, 120)
      self.manager = manager
      self.init_gui()

   def init_gui(self):
      self.day_text = QLabel("Day:", self)
      self.day_text.move(10, 10)
      self.day_text.show()

      self.day_box = DayEditor(self)
      self.day_box.setFixedWidth(65)
      self.day_box.move(65, 10)
      self.day_box.show()

      self.month_text = QLabel("Month:", self)
      self.month_text.move(10, 40)
      self.month_text.show()

      self.month_box = MonthEditor(self)
      self.month_box.setFixedWidth(65)
      self.month_box.move(65, 40)
      self.month_box.show()

      self.select_button = QPushButton("Select", self)
      self.select_button.resize(self.select_button.sizeHint())
      print(self.width())
      print(self.select_button.width())
      print(give_position(self.width(), self.select_button.width()))
      self.select_button.move(give_position(self.width(), self.select_button.width()), 80)
      self.select_button.clicked.connect(self.select_date)
      self.select_button.show()

      self.show()

   def select_date(self):
      print("date selected")
      self.close()

   def keyPressEvent(self, event):
      key_code = event.key()
      if key_code == 16777220:
         self.select_date()

   def is_a_date_selected(self):
      return True


class DayEditor (QLineEdit):
   
   def __init__(self, widget):
      super().__init__(widget)
      self.widget = widget

   def keyPressEvent(self,e):
      #print('key pressed')
      super().keyPressEvent(e)

class MonthEditor (QLineEdit):
   
   pass

class MyTextEditor(QTextEdit):

   def __init__(self, window_manager):
      super().__init__(window_manager.main_window)
      self.window_manager = window_manager

   def keyPressEvent(self,e):
      #print('key pressed')
      super().keyPressEvent(e)
      self.window_manager.press_key()
 

class HistoryViewer (QWidget):

   horizontal_border = 15
   vertical_difference = 12

   def __init__(self):
      super().__init__()
      self.setWindowTitle('History')
      self.setGeometry(100, 100, 550, 800)
      self.entries = User.current_user.history[::-1]
      self.pages = []
      self.current_page = 1
      self.init_gui()

   def init_gui(self):
      self.title = QLabel("History", self)
      font = QFont()
      font.setPointSize(17)
      self.title.setFont(font)
      self.title.move(15, 10)
      self.title.show()
      self.show()

      self.prev_button = QPushButton("<<", self)
      self.prev_button.clicked.connect(self.prev)
      self.prev_button.move(280, 750)
      #self.prev_button.show()

      self.next_button = QPushButton(">>", self)
      self.next_button.clicked.connect(self.next)
      self.next_button.move(400, 750)
      #self.next_button.show()

      self.labels = []
      font = QFont()
      font.setPointSize(10)

      for entry in self.entries:
         label = QLabel(entry.text(), self)
         label.setFont(font)
         label.resize(label.sizeHint())
         self.labels.append(label)

      self.load_pages()
      self.set_page()

   def load_pages(self):
      for i in range(0, len(self.labels)):
         current = self.labels[i]
         if len(self.pages) == 0:
            new = Page(self)
            self.pages.append(new)
         if self.pages[len(self.pages) - 1].enough_space(current):
            self.pages[len(self.pages) - 1].add(current)
         else:
            new = Page(self)
            self.pages.append(new)
            self.pages[len(self.pages) - 1].add(current)

   def set_page(self):
      for label in self.labels:
         label.hide()

      last_border = 10 + self.title.height() + 10
      entries = self.pages[self.current_page - 1].get_entries()
      for entry in entries:
         entry.move(HistoryViewer.horizontal_border, last_border + HistoryViewer.vertical_difference)
         entry.show()
         last_border += entry.height() + HistoryViewer.vertical_difference

      if self.current_page > 1:
         self.prev_button.show()
      else:
         self.prev_button.hide()
      if self.current_page < len(self.pages):
         self.next_button.show()
      else:
         self.next_button.hide()

   def next(self):
      if self.current_page < len(self.pages):
         self.current_page += 1
         self.set_page()

   def prev(self):
      if self.current_page > 1:
         self.current_page -= 1
         self.set_page()

   def keyPressEvent(self, event):
      print("se apretó algo")
      key_code = event.key()
      print(key_code)


class Page:

   max_border = 725

   def __init__(self, viewer):
      self.entries = []
      self.viewer = viewer

   @property
   def height(self):
      x = 10 + self.viewer.title.height() + 10
      for entry in self.entries:
         x += entry.height() + HistoryViewer.vertical_difference
      return x

   def get_entries(self):
      return self.entries

   def enough_space(self, new_label):
      if len(self.entries) == 0:
         return True
      label_height = new_label.height()
      if self.height + label_height <= Page.max_border:
         return True
      else:
         return False

   def add(self, label):
      self.entries.append(label)


def give_position(window_width, object_width):
   half_window = window_width//2
   half_obj = object_width//2
   #print(window_width)
   #print(object_width)
   #print(half_window)
   #print(half_obj)
   #print(half_window - half_obj)
   return half_window - half_obj


if __name__ == '__main__':
   def hook(type, value, traceback):
      print(type)
      print(traceback)
   sys.__excepthook__ = hook

   app = QApplication(sys.argv)
   main_window = MainWindow()
   sys.exit(app.exec_())