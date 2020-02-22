import tkinter as tk
from tkinter import ttk
import sqlite3
import socket
import pickle
from win10toast import *


class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.obj = {}
        self.init_main()
        self.db = db
        self.view_records()

    def init_main(self):
        toolbar = tk.Frame(bg="#d7d8e0", bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        self.add_img = tk.PhotoImage(file="img/line2.png")
        btn_open_dialog = tk.Button(toolbar, text='добавить встречу', command=self.open_dialog,
                                    bg='#d7d8e0', bd=0, compound=tk.TOP, image=self.add_img)
        btn_open_dialog.pack(side=tk.LEFT)

        self.tree = ttk.Treeview(self, columns=('ID', 'FIO', 'question', 'time'), height=15,
                                 show='headings')
        self.tree.column('ID', width=50, anchor=tk.CENTER)
        self.tree.column('FIO', width=220, anchor=tk.CENTER)
        self.tree.column('question', width=100, anchor=tk.CENTER)
        self.tree.column('time', width=110, anchor=tk.CENTER)

        self.tree.heading('ID', text='Номер')
        self.tree.heading('FIO', text='ФИО')
        self.tree.heading('question', text='Вопрос')
        self.tree.heading('time', text='Время')

        self.tree.pack()

    def send_data(self, FIO, question, time):
        self.obj[1] = FIO
        self.obj[2] = question
        self.obj[3] = time
        data = pickle.dumps(obj)
        sock.send(data)
        print(self.obj)

    def records(self, FIO, question, time):
        self.send_data(FIO, question, time)
        self.db.insert_data(FIO, question, time)
        self.view_records()

    def view_records(self):
        self.db.c.execute('''SELECT * FROM line''')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def open_dialog(self):
        Child()


class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    def destroy_window(self):
        self.view.records(self.entry_FIO.get(),self.entry_time.get(),self.entry_question.get())
        self.destroy()

    def init_child(self):
        self.title('Добавить в очередь встреч')
        self.geometry("400x220+400+300")
        self.resizable(False, False)

        label_FIO = tk.Label(self, text='ФИО')
        label_FIO.place(x=50, y=50)

        self.entry_FIO = ttk.Entry(self)
        self.entry_FIO.place(x=200, y=50)

        label_question = tk.Label(self, text='Вопрос')
        label_question.place(x=50, y=80)

        self.entry_question = ttk.Entry(self)
        self.entry_question.place(x=200, y=80)

        label_time = tk.Label(self, text='Время')
        label_time.place(x=50, y=110)

        self.entry_time = ttk.Entry(self)
        self.entry_time.place(x=200, y=110)

        btn_cancel = ttk.Button(self, text='закрыть', command=self.destroy)
        btn_cancel.place(x=300, y=170)

        self.btn_ok = ttk.Button(self, text='Добавить', command=self.destroy_window)
        self.btn_ok.place(x=220, y=170)
        '''self.btn_ok.bind('<Button-1>', lambda event: self.view.records(self.entry_FIO.get(), self.entry_time.get(),
                                                                       self.entry_question.get()))'''

        self.grab_set()
        self.focus_set()


class DB:
    def __init__(self):
        self.conn = sqlite3.connect('line.db')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS line (id integer primary key, FIO text, question text, 
        time text)''')
        self.conn.commit()

    def insert_data(self, FIO, question, time):
        self.c.execute(''' INSERT INTO line(FIO,question,time) VALUES (?, ?, ?)''', (FIO, question, time))
        self.conn.commit()


if __name__ == "__main__":
    sock = socket.socket()
    '''Работать будет на 2х компах , если через cmd найдем ipv4 нашего роутера и присоединимся к серверу в
        локальной сети по ip (Windows: ipconfig /all, OSX/Linux: ifconfig)'''
    '''у меня было 192.168.1.42'''
    sock.connect(('192.168.1.42', 5000))
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title("Очередь приема")
    root.geometry("650x450+300+200")
    root.resizable(False, False)
    obj = app.obj
    print('App started')
    root.mainloop()
