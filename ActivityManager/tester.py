import json
import os

class Entry:

   entries = []

   def __init__(self, date, text):
      self.date = date
      self.text = text
      Entry.entries.append(self)

   def __str__(self):
      return self.date + ";" + self.text

dictionary = {}
dictionary["name"] = "a"
dictionary["rank"] = 43

e1 = Entry("22/01", "Insanity y demas cosas interesantes osea tu ya sabesInsanity y demas Insanity y demas cosas interesantes osea tu ya sabescosas interesantes osea tu ya sabesInsanity y demas cosas interesantes osea tu ya sabesInsanity y demas cosas interesantes osea tu ya sabes") # +1
e2 = Entry("23/01", "Patinaje y demas cosas interesantes osea tu ya sabes") # +1
e3 = Entry("24/01", "Insanity y demas cosas interesantes osea tu ya sabes") # +1
e4 = Entry("25/01", "Patinaje y demas cosas interesantes osea tu ya sabes y demas cosas interesantes osea tu ya sabes") # +1
e5 = Entry("29/01", "Patinaje y demas cosas interesantes osea tu ya sabes\n\nInsanity y demas cosas interesantes osea tu ya sabes") # +1 -1
e6 = Entry("30/01", "Insanity y demas cosas interesantes osea tu ya sabes") # +1
e7 = Entry("31/01", "Patinaje ydemascosasinteresantesoseatuya sabes") # +1
e8 = Entry("01/02", "Patinaje:\ny demas cosas interesantes osea tu ya sabesPatinaje y demas cosas interesantes osea tu ya sabesPatinaje y demas cosas interesantes osea tu ya sabes") # +1
# 7
e9 = Entry("02/02", "Patinaje y demas cosas interesantes osea tu ya sabesPatinaje y demas cosas interesantes osea tu ya sabesPatinaje y demas cosas interesantes osea tu ya sabesPatinaje y demas cosas interesantes osea tu ya sabesPatinaje y demas cosas interesantes osea tu ya sabesPatinaje y demas cosas interesantes osea tu ya sabesPatinaje y demas cosas interesantes osea tu ya sabesPatinaje y demas cosas interesantes osea tu ya sabesPatinaje y demas cosas interesantes osea tu ya sabes") # +1
e10 = Entry("03/02", "Patinaje y demas cosas interesantes osea tu ya sabesPatinaje y demas cosas interesantes osea tu ya sabesPatinaje y demas cosas interesantes osea tu ya sabes") # +1
#e11 = Entry("04/02", "Patinaje y demas cosas interesantes osea tu ya sabesPatinaje y demas cosas interesantes osea tu ya sabes") # +1
#e12 = Entry("05/02", "Patinaje y demas cosas interesantes osea tu ya sabes") # +1
#e13 = Entry("06/02", "Patinaje y demas cosas interesantes osea tu ya sabesPatinaje y demas cPatinaje y demas cosas interesantes osea tu ya sabesosas interesantes osea tu ya sabesPatinaje y demas cosas interesantes osea tu ya sabes") # +1

dictionary["n"] = len(Entry.entries)

for i in range(0, len(Entry.entries)):
   dictionary[str(i)] = str(Entry.entries[i])

with open(os.path.join("User", dictionary["name"] + ".json"), "w") as file:
    json.dump(dictionary, file)


"""
def to_paragraph(text):
   entry_width = 30
   words = text.split(" ")
   lines = []
   current_line = ""
   print(words)
   for word in words:
      print(current_line)
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
            print(word)
            lines.append(current_line)
            current_line = word

      if word == words[-1]:
         lines.append(current_line)

   print(lines)
   spaced_message = "\n".join(lines)

   return spaced_message

def to_text(text):
   paragraphs = text.split("\n")
   corrected = []
   for p in paragraphs:
      corrected.append(to_paragraph(p))
   return "date\n" + "\n".join(corrected)

#a = to_paragraph("hola como estas aqui todo bien loco que me cuentas.\nTodo super interesante\nMe gusta\nasdfghjklñzxcvbnmqwertyuiop1234567890")
#print(a)

b = to_text("hola como estas aqui todo bien loco que me cuentas.\nTodo super interesante\nMe gusta\nasdfghjklñzxcvbnmqwertyuiop1234567890")
print(b)
"""