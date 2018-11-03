# -*- coding: utf-8 -*-
import re
import os
try:
    from Tkinter import *
    import tkFileDialog
    import tkMessageBox as messagebox
except ImportError:
    from tkinter import *
    from tkinter.filedialog import *
    from tkinter import messagebox


def get_protocol(paths):
    data = []
    for path in paths:
        try:
            with open(path) as file:
                lines = file.readlines()
                if not re.findall('d:\d+,M:\d+,h:\d+,m:\d+,s:\d+,', lines[0]):
                    messagebox.showwarning('Предупреждение',
                                           'Файл ' + path.split('/')[-1] + ' не является протоколом.')
                    continue
                for line in lines:
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
        except Exception as err:
            messagebox.showwarning('Предупреждение',
                                   'Не могу прочитать файл ' + path.split('/')[-1] + '.\nОшибка: ' + str(err))
            continue
    if not data:
        return False

    save = asksaveasfilename(initialdir=os.getcwd(),
                             title='Сохранить результат',
                             initialfile='result',
                             filetypes=[('all files', '.*'), ('text files', '.txt')],
                             defaultextension='.txt')
    if save:
        with open(save, 'w') as file:
            print('================================================================================\n', file=file)
            print('<СТАНЦИЯ> <ДД-ММ> <ЧЧ:ММ:СС> --- <СПИСОК ИМПУЛЬСОВ>\n', file=file)
            sdata = sorted(data)
            station = ''
            for line in sdata:
                if not line[0] in station:
                    print('================================================================================\n', file=file)
                    station = line[0]
                print(line[1], file=file)
        return save


class App:
    def __init__(self, root):
        self.root = root
        self.root.bind('<F1>', self.top_level_about)
        self.root.bind('<Control-q>', self.close)
        self.root.bind('<Control-z>', self.add_file)
        self.menu()
        self.elements()

    def menu(self):
        self.root.option_add('*tearOff', False)
        menubar = Menu(self.root)
        self.root.config(menu=menubar)

        file = Menu(menubar)
        about = Menu(menubar)

        menubar.add_cascade(menu=file, label=u'Файл')
        menubar.add_cascade(menu=about, label=u'?')

        file.add_command(label=u'Добавить файл', command=self.add_file, accelerator="Ctrl+Z")
        file.add_separator()
        file.add_command(label=u'Выйти', command=self.close, accelerator="Ctrl+Q")

        about.add_command(label=u'О программе', command=self.top_level_about, accelerator="F1")

    def close(self, event=None):
        self.root.destroy()

    def elements(self):
        c = Frame(self.root)
        c.pack(fill=BOTH, expand=1, padx=5, pady=5)
        self.lbox = Listbox(c, height=10)
        vsb = Scrollbar(c, orient=VERTICAL, command=self.lbox.yview)
        vsb.pack(fill=Y, side=RIGHT)
        hsb = Scrollbar(c, orient=HORIZONTAL, command=self.lbox.xview)
        hsb.pack(fill=X, side=BOTTOM)
        self.lbox.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.lbox.pack(fill=BOTH)

        c2 = Frame(self.root)
        c2.pack(fill=BOTH, expand=1, padx=30, pady=10)

        add = Button(c2, text='Добавить файл', command=self.add_file)
        remove = Button(c2, text='Удалить файл', command=self.remove_file)
        self.run = Button(c2, text='Запустить обработку', command=self.run_parse)

        add.pack(fill=X)
        remove.pack(fill=X, pady=10)
        self.run.pack(fill=X, ipady=10)

        c.grid_columnconfigure(0, weight=1)
        c.grid_rowconfigure(0, weight=1)

        self.lbox.bind('<Double-1>', lambda event: self.remove_file())

    def add_file(self, event=None):
        path = askopenfilename(initialdir=os.getcwd())
        if '' != path.strip():
            self.lbox.insert(END, path)
        for i in range(0, len(self.lbox.get(0, END)), 2):
            self.lbox.itemconfigure(i, background='#ccc')

    def remove_file(self):
        if not self.lbox.get(0, END):
            messagebox.showwarning('Сообщение', 'Вы не добавили файлы для обработки.')
            return
        if not self.lbox.curselection():
            messagebox.showinfo('Сообщение', 'Файл для удаления из списка не выбран.')
            return
        MsgBox = messagebox.askquestion('Удалить файл', 'Вы уверены, что хотите удалить файл из списка?',
                                        icon='warning')
        if MsgBox == 'yes':
            self.lbox.delete(ANCHOR)

    def run_parse(self):
        if not self.lbox.get(0, END):
            messagebox.showwarning('Сообщение', 'Добавьте файлы протоколов для обработки.')
        else:
            self.run.configure(text=u'Обработка...')
            self.run.update()
            result = get_protocol(self.lbox.get(0, END))
            if result:
                messagebox.showinfo('Сообщение', 'Протокол обработан и сохранен по адресу\n' + str(result))
            self.run.configure(text=u'Запустить обработку')
            self.run.update()

    def top_level_about(self, event=None):
        win = Toplevel(self.root)
        win.resizable(0, 0)
        center(win, 220, 120, 0)
        win.iconbitmap(os.getcwd() + os.path.sep + u'icon.ico')
        win.title(u'О программе')

        frame = Frame(win)
        frame.pack()

        label1 = Label(frame, text=u'Программа анализирует и\nсортирует данные из\nфайлов протоколов.')
        label2 = Label(frame, text=u'Автор © Манжак С.С.')
        label3 = Label(frame, text=u'Версия v' + self.root.version + u' Win 32')

        label1.grid(row=0, column=0, pady=10)
        label2.grid(row=1, column=0)
        label3.grid(row=2, column=0)

        win.focus_set()
        win.grab_set()
        win.wait_window()


def center(root, width, height, offset):
    x = root.winfo_screenwidth() / 2 - width / 2 + offset
    y = root.winfo_screenheight() / 2 - height / 2 + offset
    root.geometry('{}x{}+{}+{}'.format(width, height, round(x), round(y)))


def main():
    root = Tk()
    root.version = '0.0.2'
    root.resizable(0, 0)
    center(root, 250, 340, 0)
    root.title(u'Анализ протоколов')
    root.iconbitmap(os.getcwd() + os.path.sep + 'icon.ico')
    app = App(root)
    root.mainloop()


if __name__ == '__main__':
    main()
