# -*- coding: utf-8 -*-
import re
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import *
from tkinter import messagebox
import os


def get_protocol():
    with open('test/ЦУП.115') as file:
        data = []
        for line in file.readlines():
            if not re.findall('^t=|[dMhms]', line):
                data[-1][1] += line.rstrip()
            if re.findall(r'd:(\d+)', line):
                day = re.findall(r'd:(\d+)', line)[0]
            if re.findall(r'M:(\d+)', line):
                month = re.findall(r'M:(\d+)', line)[0]
            if re.findall(r'h:(\d+)', line):
                hour = re.findall(r'h:(\d+)', line)[0]
            if re.findall(r'm:(\d+)', line):
                minute = re.findall(r'm:(\d+)', line)[0]
            if re.findall(r's:(\d+)', line):
                second = re.findall(r's:(\d+)', line)[0]
            if re.findall(r'^t=([^,]+),(.+)$', line):
                station = re.findall(r'^t=([^,]+),(.+)$', line)[0][0]
                impulse = re.findall(r'^t=([^,]+),(.+)$', line)[0][1]
                data.append([station])
                data[-1].append('{} {}-{} {}:{}:{} --- {}'.format(station, month, day, hour, minute, second, impulse))

    with open('test/result', 'a') as file:
        print('================================================================================\n', file=file)
        print('<СТАНЦИЯ> <ДД-ММ> <ЧЧ:ММ:СС> --- <СПИСОК ИМПУЛЬСОВ>\n', file=file)
        sdata = sorted(data)
        station = ''
        for line in sdata:
            if not line[0] in station:
                print('================================================================================\n', file=file)
                station = line[0]
            print(line[1], file=file)


class App:
    def __init__(self, root):
        self.root = root
        self.root.bind('<F1>', self.top_level_about)
        self.root.bind('<Control-q>', self.close)
        self.menu()
        self.countrycodes = (
        'ar', 'au', 'be', 'br', 'ca', 'cn', 'dk', 'fi', 'fr', 'gr', 'in', 'it', 'jp', 'mx', 'nl', 'no', 'es', 'se',
        'ch')
        self.countrynames = ('Argentina', 'Australia', 'Belgium', 'Brazil', 'Canada', 'China', 'Denmark', \
                        'Finland', 'France', 'Greece', 'India', 'Italy', 'Japan', 'Mexico', 'Netherlands', 'Norway',
                        'Spain', \
                        'Sweden', 'Switzerland')
        self.cnames = StringVar(value=self.countrynames)
        self.populations = {'ar': 41000000, 'au': 21179211, 'be': 10584534, 'br': 185971537, \
                       'ca': 33148682, 'cn': 1323128240, 'dk': 5457415, 'fi': 5302000, 'fr': 64102140, 'gr': 11147000, \
                       'in': 1131043000, 'it': 59206382, 'jp': 127718000, 'mx': 106535000, 'nl': 16402414, \
                       'no': 4738085, 'es': 45116894, 'se': 9174082, 'ch': 7508700}

        # Names of the gifts we can send
        self.gifts = {'card': 'Greeting card', 'flowers': 'Flowers', 'nastygram': 'Nastygram'}

        self.gift = StringVar()
        self.sentmsg = StringVar()
        self.statusmsg = StringVar()
        self.elements()

    def menu(self):
        self.root.option_add('*tearOff', False)
        menubar = Menu(self.root)
        self.root.config(menu=menubar)

        file = Menu(menubar)
        about = Menu(menubar)

        menubar.add_cascade(menu=file, label=u'Файл')
        menubar.add_cascade(menu=about, label=u'?')

        file.add_command(label=u'Выйти', command=self.close, accelerator="Ctrl+Q")

        about.add_command(label=u'О программе', command=self.top_level_about, accelerator="F1")

    def close(self, event=None):
        self.root.destroy()

    def elements(self):
        c = ttk.Frame(self.root)
        c.pack(fill=BOTH)
        self.lbox = Listbox(c, listvariable=self.cnames, height=10)
        vsb = ttk.Scrollbar(c, orient=VERTICAL,
            command=self.lbox.yview)
        vsb.pack(fill=Y, side=RIGHT)
        self.lbox.configure(yscrollcommand=vsb.set)
        self.lbox.pack(fill=BOTH)

        c2 = ttk.Frame(self.root)
        c2.pack(fill=BOTH)
        add = ttk.Button(c2, text='Добавить')
        remove = ttk.Button(c2, text='Удалить')
        go = ttk.Button(c2, text='Запустить')

        add.pack(side=LEFT)
        remove.pack(side=LEFT)
        go.pack(side=LEFT)
        c.grid_columnconfigure(0, weight=1)
        c.grid_rowconfigure(0, weight=1)

        self.lbox.bind('<Double-1>', lambda event, text='Удалить': message(text))

        # Colorize alternating lines of the listbox
        for i in range(0, len(self.countrynames), 2):
            self.lbox.itemconfigure(i, background='#ccc')

    def top_level_about(self, event=None):
        win = Toplevel(self.root)
        win.resizable(0, 0)
        center(win, 220, 115, 0)
        win.iconbitmap(os.getcwd() + os.path.sep + u'icon.ico')
        win.title(u'О программе')

        frame = Frame(win)
        frame.pack()

        label1 = Label(frame, text=u'Программа анализирует и\nсортирует файлы протокола.')
        label2 = Label(frame, text=u'Автор © Манжак С.С.')
        label3 = Label(frame, text=u'Версия v' + self.root.version + u' Win7 32')

        label1.grid(row=0, column=0, pady=10)
        label2.grid(row=1, column=0)
        label3.grid(row=2, column=0)

        win.focus_set()
        win.grab_set()
        win.wait_window()


def message(text):
    messagebox.showwarning(title=u'Сообщение', message=text)


def center(root, width, height, offset):
    x = root.winfo_screenwidth() / 2 - width / 2 + offset
    y = root.winfo_screenheight() / 2 - height / 2 + offset
    root.geometry('{}x{}+{}+{}'.format(width, height, round(x), round(y)))


def main():
    root = Tk()
    root.version = '0.0.1'
    root.resizable(0, 0)
    center(root, 300, 300, 0)
    root.title(u'Анализ протоколов')
    root.iconbitmap(os.getcwd() + os.path.sep + 'icon.ico')
    app = App(root)
    root.mainloop()


if __name__ == '__main__':
    main()
