from cmath import e
from logging import exception
from tkinter import*
from tkinter import messagebox
import datetime
import email
import imaplib
import traceback
import sys
import traceback
#import ssl

def show_settings():
    messagebox.showinfo('Проверка настроек', 
                        'Почта на которую приходят сообщения: ' + email_account.get() + '\n' + 
                        'Пароль от почты куда приходят сообщения: ' + email_password.get() + '\n' + 
                        'Хост (IMAP) либо IP: ' + host.get() + '\n' +
                        'Активность SSL протокола' + ssl.get() + '\n' +
                        'Наличие PORT' + port.get() + '\n' +
                        'Почта прогноза воды: ' + mail_whate.get() + '\n' +
                        'Почта прогноза погоды: ' + mail_weather.get() + '\n' +
                        'Почта прогноза метрологии: ' + mail_meteo.get() + '\n' +
                        'Путь для сохранения голосового файла: ' + path_to_save.get()
                        )
    check_connection(email_account.get(), email_password.get(), host.get(), ssl.get(), port.get())
    #вызываем функцию сохранения данных чтобы сделать get для полей Entry и записать файл в setting.txt 
    save_setting(email_account.get(), email_password.get(), host.get(), ssl.get(), port.get(), mail_whate.get(), mail_weather.get(), mail_meteo.get(), path_to_save.get())

def save_setting(email_account, email_password, host, ssl, port, mail_whate, mail_weather, mail_meteo, path_to_save):
    #проверяем подключение к почте
    
    
    settings_list = list()
    str_replace_putch = ''

    settings_list.append(email_account)
    settings_list.append(email_password)
    settings_list.append(host)
    settings_list.append(ssl)
    settings_list.append(port)
    settings_list.append(mail_whate)
    settings_list.append(mail_weather)
    settings_list.append(mail_meteo)
    settings_list.append(path_to_save)

    str_replace_putch = str(settings_list[8])
    str_replace_putch = str_replace_putch.replace('/', '\\')
    settings_list[8]  = str_replace_putch

    print(type(settings_list[8]))
    print(settings_list[8])

    print(path_to_save)
    #записываем в файл найстроки
    settings_list = str(settings_list) 
    settings_file = open('setiing.txt', 'w', encoding = 'utf-8')
    settings_file.write(settings_list)
    settings_file.close()
    
    #print(settings_list)
    return settings_list

def reset_settings():
    #открываем дефолтный файл
    str_def_file = open('default_settings.txt', 'r', encoding = 'utf-8').read()
    def_file_list = list()

    #удаляем и строки все ненужнын символы
    str_def_file = str_def_file.replace("[", '')
    str_def_file = str_def_file.replace("'", '')
    str_def_file = str_def_file.replace("]", '')
    str_def_file = str_def_file.replace(",", '')

    #делаем из строки список элементов
    str_def_file = str_def_file.split(" ")
    def_file_list = str_def_file

    #отчищаем все поля
    email_account_entry.insert  (0, 1)
    email_password_entry.insert (1, 1)
    host_entry.insert           (2, 1)
    ssl_entry.insert            (3, 1)
    port_entry.insert           (4, 1)
    mail_whate_entry.insert     (5, 1)
    mail_weather_entry.insert   (6, 1)
    mail_meteo_entry.insert     (7, 1)
    path_to_save_entry.insert   (8, 1)

    email_account_entry.delete  (0, last = END)
    email_password_entry.delete (0, last = END)
    host_entry.delete           (0, last = END)
    ssl_entry.delete            (0, last = END)
    port_entry.delete           (0, last = END)
    mail_whate_entry.delete     (0, last = END)
    mail_weather_entry.delete   (0, last = END)
    mail_meteo_entry.delete     (0, last = END)
    path_to_save_entry.delete   (0, last = END)

    #вставляем все дефолтные поля из списка
    email_account_entry.insert  (0, def_file_list[0])
    email_password_entry.insert (1, def_file_list[1])
    host_entry.insert           (2, def_file_list[2])
    ssl_entry.insert            (3, def_file_list[3])
    port_entry.insert           (4, def_file_list[4])
    mail_whate_entry.insert     (5, def_file_list[5])
    mail_weather_entry.insert   (6, def_file_list[6])
    mail_meteo_entry.insert     (7, def_file_list[7])
    path_to_save_entry.insert   (8, def_file_list[8])
    #print(def_file_list[8])
    #print('настройки сброшены')

def check_connection(email_account, email_password, host, ssl, port):
    if ssl == 'yes' and port.isnumeric():
        PORT = int(port)
        mail = imaplib.IMAP4_SSL(host, PORT)
    else:
        mail = imaplib.IMAP4(host)
        print(mail)
    
    try:
        mail.login(email_account, email_password)
        print(  'соединение с почтой успешно установлено host = ' + host + '\n' +
                'получатель писем email_account = ' + email_account + '\n' + 
                'пароль получателя писем email_password = ' + email_password + '\n' +
                'наличие ssl = ' + ssl + '\n' +
                'порт port = ' + port + '\n')
        messagebox.showinfo('Проверка подключения', 'Проверка настроек прошла успешно')
    except Exception:
        print(  'не удалось подключиться к почте перепроверьте логин, пароль и хост \n' +
                'попробуйте убрать ssl и port и подключитесь без них  \n')
        messagebox.showerror('Проверка подключения', 'вы ввели не верные параметры перепроверьте их')
    #finally:
        #mail.close()

root = Tk()
root.title('Интерфейс голорилки')
x = 5
y = 5 

name_string_list = list()

email_account  = StringVar()
email_password = StringVar()
host           = StringVar()
ssl            = StringVar()
port           = StringVar()
mail_whate     = StringVar()
mail_weather   = StringVar()
mail_meteo     = StringVar()
path_to_save   = StringVar()

email_account_lable  = Label(text = 'Email получателя:',                                    font = 'Times-New-Roman 14')
email_password_lable = Label(text = 'Пароль получателся:',                                  font = 'Times-New-Roman 14')
host_lable           = Label(text = 'Host:',                                                font = 'Times-New-Roman 14')
ssl_lable            = Label(text = 'Ssl (yes/no):',                                        font = 'Times-New-Roman 14')
port_lable           = Label(text = 'Ssl POTR (993/465/no):',                               font = 'Times-New-Roman 14')
mail_whate_lable     = Label(text = 'Email гедрологов:',                                    font = 'Times-New-Roman 14')
mail_weather_lable   = Label(text = 'Email синоптиков:',                                    font = 'Times-New-Roman 14')
mail_meteo_lable     = Label(text = 'Email метеорологов:',                                  font = 'Times-New-Roman 14')
path_to_save_lable   = Label(text = 'Путь записи голоса пример(d:|folder_1|folder_2|):',    font = 'Times-New-Roman 14')

email_account_lable.grid    (row = 0, column = 0, sticky='w')
email_password_lable.grid   (row = 1, column = 0, sticky='w')
host_lable.grid             (row = 2, column = 0, sticky='w')
ssl_lable.grid              (row = 3, column = 0, sticky='w')
port_lable.grid             (row = 4, column = 0, sticky='w')
mail_whate_lable.grid       (row = 5, column = 0, sticky='w')
mail_weather_lable.grid     (row = 6, column = 0, sticky='w')
mail_meteo_lable.grid       (row = 7, column = 0, sticky='w')
path_to_save_lable.grid     (row = 8, column = 0, sticky='w')

email_account_entry  = Entry(textvariable = email_account, bd = 5, width = 40)
email_password_entry = Entry(textvariable = email_password, bd = 5, width = 40)
host_entry           = Entry(textvariable = host, bd = 5, width = 40)
ssl_entry            = Entry(textvariable = ssl, bd = 5, width = 40)
port_entry           = Entry(textvariable = port, bd = 5, width = 40)
mail_whate_entry     = Entry(textvariable = mail_whate, bd = 5, width = 40)
mail_weather_entry   = Entry(textvariable = mail_weather, bd = 5, width = 40)
mail_meteo_entry     = Entry(textvariable = mail_meteo, bd = 5, width = 40)
path_to_save_entry   = Entry(textvariable = path_to_save, bd = 5, width = 40)

email_account_entry.grid    (row = 0, column = 1, padx = x, pady = y)
email_password_entry.grid   (row = 1, column = 1, padx = x, pady = y)
host_entry.grid             (row = 2, column = 1, padx = x, pady = y)
ssl_entry.grid              (row = 3, column = 1, padx = x, pady = y)
port_entry.grid             (row = 4, column = 1, padx = x, pady = y)
mail_whate_entry.grid       (row = 5, column = 1, padx = x, pady = y)
mail_weather_entry.grid     (row = 6, column = 1, padx = x, pady = y)
mail_meteo_entry.grid       (row = 7, column = 1, padx = x, pady = y)
path_to_save_entry.grid     (row = 8, column = 1, padx = x, pady = y)

#открываем файл с настройками для чтения и переводим все данные в строку
str_settings_r = open('setiing.txt', 'r', encoding = 'utf-8').read()
#print(str_settings_r)
setting_list_r = list()

#удаляем и строки все ненужнын символы
str_settings_r = str_settings_r.replace("[", '')
str_settings_r = str_settings_r.replace("'", '')
str_settings_r = str_settings_r.replace("]", '')
str_settings_r = str_settings_r.replace(",", '')

#делаем из строки список элементов
str_settings_r = str_settings_r.split(" ")
setting_list_r = str_settings_r

email_account_entry.insert  (0, setting_list_r[0])
email_password_entry.insert (1, setting_list_r[1])
host_entry.insert           (2, setting_list_r[2])
ssl_entry.insert            (3, setting_list_r[3])
port_entry.insert           (4, setting_list_r[4])
mail_whate_entry.insert     (5, setting_list_r[5])
mail_weather_entry.insert   (6, setting_list_r[6])
mail_meteo_entry.insert     (7, setting_list_r[7])
path_to_save_entry.insert   (8, setting_list_r[8])

save_button = Button(text = 'Сохранить настройки', command = show_settings)
save_button.grid(rows = 9, column = 1, padx = x, pady = y, sticky = 'w')

reset_button = Button(text = 'Сбросить настройки', command = reset_settings)
reset_button.grid(rows = 9, column = 1, padx = x, pady = y, sticky = 'w')

'''check_button = Button(text = 'Проверка настроек', command = check_connection)
check_button.grid(rows = 9, column = 1, padx = x, pady = y, sticky = 'w')'''

root.mainloop()