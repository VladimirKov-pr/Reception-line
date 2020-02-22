import tkinter as tk
from tkinter import ttk
import sqlite3
import socket
import pickle
import threading
from tkinter import messagebox as mb
from datetime import date


class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.obj = obj
        self.db = db

        self.view_records()

    def refresh_table(self):
        self.view_records()

    def init_main(self):
        toolbar = tk.Frame(bg="#d7d8e0", bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        self.add_img = tk.PhotoImage(file="img/line2.png")
        btn_open_dialog = tk.Button(toolbar, text='добавить встречу', command=self.open_dialog,
                                    bg='#d7d8e0', bd=0, compound=tk.TOP, image=self.add_img)
        btn_open_dialog.pack(side=tk.LEFT)

        self.update_img = tk.PhotoImage(file='img/edit.png')

        btn_edit_dialog = tk.Button(toolbar, text='Редактировать', bg='#d7d8e0', bd=0, image=self.update_img,
                                    compound=tk.TOP, command=self.open_update_dialog)
        btn_edit_dialog.pack(side=tk.LEFT)

        self.delete_img = tk.PhotoImage(file='img/delete.png')
        btn_delete_dialog = tk.Button(toolbar, text='Удалить', bg='#d7d8e0', bd=0, image=self.delete_img,
                                      compound=tk.TOP, command=self.delete_records)
        btn_delete_dialog.pack(side=tk.RIGHT)

        self.refresh_qeueue = tk.PhotoImage(file='img/file.png')
        btn_Refresh = tk.Button(toolbar, bg='#d7d8e0', text='Обновление Очереди', bd=0, image=self.refresh_qeueue,
                                compound=tk.TOP,
                                command=self.view_records)
        btn_Refresh.pack(side=tk.LEFT)

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

    def records(self, FIO, question, time):
        self.db.insert_data(FIO, question, time)
        self.view_records()

    def update_record(self, FIO, question, time):
        self.db.c.execute('''UPDATE line SET FIO=?, question=?, time=? WHERE ID=?''',
                          (FIO, question, time, self.tree.set(self.tree.selection()[0], '#1'),))
        self.db.conn.commit()
        self.view_records()

    def view_records(self):
        self.db.c.execute('''SELECT * FROM line''')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def delete_records(self):
        for selection_item in self.tree.selection():
            self.db.c.execute('''DELETE FROM line WHERE id=?''', (self.tree.set(selection_item, '#1'),))
        self.db.conn.commit()
        self.view_records()

    def open_update_dialog(self):
        Update()

    def open_dialog(self):
        Child()


class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    def destroy_window(self):
        self.view.records(self.entry_FIO.get(), self.entry_question.get(), self.entry_time.get())
        self.destroy()

    def only_numbers(self, char):
        return char.isdigit()

    def init_child(self):
        self.title('Добавить в очередь встреч')
        self.geometry("400x220+400+300")
        self.resizable(False, False)
        d = date.fromordinal(730920)  # 730920th day after 1. 1. 0001

        label_FIO = tk.Label(self, text='ФИО')
        label_FIO.place(x=50, y=50)

        self.entry_FIO = ttk.Entry(self)
        self.entry_FIO.place(x=200, y=50)

        '''label_helper = ttk.Label(self, text='autoformated data for today. change it if you want')
        label_helper.place(x=40, y=250)'''

        label_question = tk.Label(self, text='Вопрос')
        label_question.place(x=50, y=80)

        self.entry_question = ttk.Entry(self)
        self.entry_question.place(x=200, y=80)

        label_time = tk.Label(self, text='Время')
        label_time.place(x=50, y=110)

        validation = self.register(self.only_numbers)
        self.entry_time = ttk.Entry(self, validate="key", validatecommand=(validation, '%S'))
        self.entry_time.place(x=200, y=110)
        self.entry_time.insert(0, str(d.today()) + '-')

        btn_cancel = ttk.Button(self, text='закрыть', command=self.destroy)
        btn_cancel.place(x=300, y=170)

        self.btn_ok = ttk.Button(self, text='Добавить', command=self.destroy_window)
        self.btn_ok.place(x=220, y=170)
        '''self.btn_ok.bind('<Button-1>', lambda event: self.view.records(self.entry_FIO.get(),
                                                                       self.entry_time.get(),
                                                                       self.entry_question.get()))'''

        self.grab_set()
        self.focus_set()


class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app

    def destroy_window(self):
        self.view.update_record(self.entry_FIO.get(), self.entry_question.get(), self.entry_time.get())
        self.destroy()

    def init_edit(self):
        self.title('Редактирование')
        btn_edit = ttk.Button(self, text='Редактировать', command=self.destroy_window)
        btn_edit.place(x=205, y=170)
        '''btn_edit.bind('<Button-1>', lambda event: self.view.update_record(self.entry_FIO.get(),
                                                                       self.entry_question.get(),
                                                                       self.entry_time.get()))'''
        self.btn_ok.destroy()


class DB:
    def __init__(self):
        self.conn = sqlite3.connect('line.db')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS line (id integer primary key, FIO text, question text, 
        time text)''')
        self.conn.commit()

    def insert_data(self, FIO, question, time):
        conn = sqlite3.connect('line.db')
        conn.commit()
        self.c.execute(''' INSERT INTO line(FIO,question,time) VALUES (?, ?, ?)''', (FIO, question, time))
        self.conn.commit()


class DB2:
    def insert_data(self, FIO, question, time):
        conn = sqlite3.connect('line.db')
        c = conn.cursor()
        c.execute(''' INSERT INTO line(FIO,question,time) VALUES (?, ?, ?)''', (FIO, question, time))
        conn.commit()
        conn.close()


class Receive(threading.Thread):
    def __init__(self, app, db2):
        threading.Thread.__init__(self)
        self.db = db2
        self.app = app

    def run(self):
        sock = socket.socket()
        sock.connect(('192.168.1.42', 5000))
        while 1:
            print('connected')
            try:
                data = sock.recv(4096)
                if data == '{}':
                    print('no data')
                print('All data: {}'.format(data))
                obj = pickle.loads(data)
                print(obj)
                self.db.insert_data(obj[1], obj[2], obj[3])
                mb.askyesno(title="Предупреждение ", message="Добавлена запись!. Обновите бд")
            except OSError:
                pass


if __name__ == "__main__":
    obj = {}
    root = tk.Tk()
    db = DB()
    db2 = DB2()
    app = Main(root)

    app.pack()
    root.title("Очередь приема")
    root.geometry("650x450+300+200")
    root.resizable(False, False)
    print('App started')
    # root.after(10000, app.view_records())
    recv_data = Receive(app, db2)
    my_thread = recv_data.start()
    root.mainloop()
