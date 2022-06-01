from time import sleep
import imaplib
import ssl
import os

#открываем файл с настройками и превращаем его содержимое в строку
str_settings = open('setiing.txt', 'r', encoding = 'utf-8').read()

#удаляем и строки все ненужнын символы
str_settings = str_settings.replace ("[", ''
                                    ).replace("'", ''
                                    ).replace("]", ''
                                    ).replace(",", ''
                                    ).replace("|", '\\'
                                    ).split(" ")

#переменные для подлкючения к почте
EMAIL_ACCOUNT   = str_settings[0]
PASSWORD        = str_settings[1]
HOST            = str_settings[2]
SSL             = str_settings[3]
PORT            = str_settings[4]

print('Адрес входящих писем:', EMAIL_ACCOUNT)
print('Пароль для почты входящих писем:', PASSWORD)
print('HOST для подлкючения:', HOST)
print('Запрос SSL:', SSL)
print('PORT для подключения:', PORT)

#подключаемся к почте 
try: 
    if SSL == 'yes' and PORT.isnumeric():
        PORT = int(PORT)
        mail = imaplib.IMAP4_SSL(HOST, PORT)
    else:
        mail = imaplib.IMAP4(HOST)
        print(mail)

    mail.login(EMAIL_ACCOUNT, PASSWORD)
    mail.list()
    mail.select('inbox')
    result, data = mail.search(None, 'ALL') # (ALL/UNSEEN)

    i = len(data[0].split())
    print('Количество писем:', i)
    #закрываем соединение по протоколу imap
    mail.close()
    print('соединение с почтой установлено')
    sleep(10)
except:  
    print(  'не удалось подлкючиться к почте попробуйте проверить настройки в графическом интерфейсе')
    sleep(10)    