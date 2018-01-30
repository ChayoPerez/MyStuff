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
      self.user = None
      self.menu = Menu(self)
      self.sign_in_window = EnterName(self)

      self.setWindowTitle('Activity Manager')
      self.setGeometry(100, 100, 300, 300)
      self.init_gui()

   def keyPressEvent(self, event):
      key_code = event.key()
      if key_code == 16777220:
         if self.sign_in_window.active:
            self.sign_in_window.press_enter()

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
      self.title = QLabel("Bienvenido a ActivityManager!", self.main_window)
      font = QFont()
      font.setPointSize(10)
      self.title.setFont(font)
      self.title.move(15, 10)

      self.sign_in_msg = QLabel("Nombre de usuario:", self.main_window)
      font = QFont()
      font.setPointSize(8)
      self.sign_in_msg.setFont(font)
      self.sign_in_msg.move(20, 50)
      self.sign_in_box = QLineEdit(self.main_window)
      self.sign_in_box.setFixedWidth(200)
      self.sign_in_box.move(20, 80)
      self.button_sign_in = QPushButton("ENTER", self.main_window)
      self.button_sign_in.clicked.connect(self.enter_username)
      font = QFont()
      font.setPointSize(6)
      self.button_sign_in.setFont(font)
      self.button_sign_in.move(20, 115)

      self.new_acc_msg = QLabel("Crea un nuevo usuario:", self.main_window)
      font = QFont()
      font.setPointSize(8)
      self.new_acc_msg.setFont(font)
      self.new_acc_msg.move(20, 165)
      self.new_acc_box = QLineEdit(self.main_window)
      self.new_acc_box.setFixedWidth(200)
      self.new_acc_box.move(20, 195)
      self.button_new_acc = QPushButton("ENTER", self.main_window)
      self.button_new_acc.clicked.connect(self.enter_new_account)
      font = QFont()
      font.setPointSize(6)
      self.button_new_acc.setFont(font)
      self.button_new_acc.move(20, 230)

      self.objects.append(self.title)
      self.objects.append(self.sign_in_msg)
      self.objects.append(self.sign_in_box)
      self.objects.append(self.button_sign_in)
      self.objects.append(self.new_acc_msg)
      self.objects.append(self.new_acc_box)
      self.objects.append(self.button_new_acc)

      self.hide()

   def show(self):
      super().show()

   def process_new_username(self, username):
      if User.valid_new_username(username):
         User.load_new_user(username)
         self.main_window.user = User.current_user
         self.main_window.enter_main_menu()
      else:
         pass

   def process_old_username(self, username):
      if User.valid_old_username(username):
         User.load_user(username)
         self.main_window.user = User.current_user
         self.main_window.enter_main_menu()
      else:
         pass

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


class Menu (WindowManager):

   def init_gui(self):

      self.title = QLabel("Menu", self.main_window)
      font = QFont()
      font.setPointSize(10)
      self.title.setFont(font)
      self.title.move(15, 10)

      self.instruction = QLabel("To register your progress enter a comment\nbellow and hit SUBMIT!", self.main_window)
      font = QFont()
      font.setPointSize(7)
      self.instruction.setFont(font)
      self.instruction.move(15, 50)

      self.enter_text = QTextEdit(self.main_window)
      self.enter_text.setFixedWidth(264)
      self.enter_text.setFixedHeight(100)
      self.enter_text.move(15, 100)

      font = QFont()
      font.setPointSize(6)

      self.submit_button = QPushButton("Submit", self.main_window)
      self.submit_button.clicked.connect(self.submit)
      self.submit_button.setFont(font)
      self.submit_button.move(90, 210)

      self.edit_button = QPushButton("Submit", self.main_window)
      self.edit_button.setText("Edit")
      self.edit_button.clicked.connect(self.edit)
      self.edit_button.setFont(font)
      self.edit_button.move(90, 210)
      self.edit_button.hide()

      self.open_history_button = QPushButton("View History", self.main_window)
      self.open_history_button.clicked.connect(self.open_history)
      self.open_history_button.setFont(font)
      self.open_history_button.move(90, 250)

      self.notice = QLabel("Entry already posted.", self.main_window)
      self.notice.setStyleSheet('color: red')
      self.notice.move(130, 14)
      self.notice.hide()

      self.level = QLabel("Lvl: ?", self.main_window)
      self.level.setFixedWidth(100)
      self.level.move(220, 260)

      self.objects.append(self.title)
      self.objects.append(self.instruction)
      self.objects.append(self.enter_text)
      self.objects.append(self.submit_button)
      self.objects.append(self.open_history_button)

      self.hide()

   def set(self):
      self.hide()
      self.open = self.main_window.user.is_box_open()
      if self.level.text() == "Lvl: ?":
         self.level.setText("Lvl " + self.main_window.user.get_level())
      if not self.open:
         self.enter_text.setText(self.main_window.user.get_last_entry())
         if not (self.notice in self.objects):
            self.objects.remove(self.submit_button)
            self.objects.append(self.notice)
            self.objects.append(self.edit_button)
            self.level.setText("Lvl " + self.main_window.user.get_level())
      self.show()

   def submit(self):
      print("submit")
      text = self.enter_text.toPlainText()
      self.main_window.user.add_entry(text)
      self.set()

   def edit(self):
      print("edit")
      text = self.enter_text.toPlainText()
      self.main_window.user.edit_last_entry(text)
      self.set()

   def open_history(self):
      print("open history")
      self.main_window.open_history()

 
class HistoryViewer (QWidget):

   def __init__(self):
      super().__init__()
      self.setWindowTitle('History')
      self.setGeometry(100, 100, 300, 300)
      self.entries = User.current_user.history[::-1]
      self.init_gui()

   def init_gui(self):
      self.title = QLabel("History", self)
      font = QFont()
      font.setPointSize(10)
      self.title.setFont(font)
      self.title.move(15, 10)
      self.title.show()
      self.show()

      self.prev_button = QPushButton("<<", self)
      self.prev_button.move(30, 250)
      self.prev_button.show()

      self.next_button = QPushButton(">>", self)
      self.next_button.move(150, 250)
      self.next_button.show()

      self.labels = []
      horizontal_border = 15
      vertical_difference = 6

      last_border = 10 + self.title.height() + 10
      font = QFont()
      font.setPointSize(6)

      for entry in self.entries:
         label = QLabel(entry.text(), self)
         label.setFont(font)
         label.resize(label.sizeHint())
         label.move(horizontal_border, last_border + vertical_difference)
         label.show()

         # print(last_border, label.height())
         
         last_border += label.height() + vertical_difference

      def set_page(self):
         pass

      def fix_pages(self):
         pass

      def next(self):
         pass

      def prev(self):
         pass


if __name__ == '__main__':
   def hook(type, value, traceback):
      print(type)
      print(traceback)
   sys.__excepthook__ = hook

   app = QApplication(sys.argv)
   main_window = MainWindow()
   sys.exit(app.exec_())