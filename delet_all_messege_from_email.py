import datetime
import email
import imaplib
import ssl

#Кодировки текста писем и файлов
default_charset = 'koi8-r'
coir = 'koi8-r'
cp = 'cp1251'
ut8 = 'utf-8'
ut16 = 'utf-16'

#открываем файл с настройками и превращаем его содержимое в строку
str_settings = open('setiing.txt', 'r', encoding = ut8).read()

#удаляем и строки все ненужнын символы
str_settings = str_settings.replace ("[", ''
                                    ).replace("'", ''
                                    ).replace("]", ''
                                    ).replace(",", ''
                                    ).replace("|", '\\'
                                    ).split(" ")

#переменные для подлкючения к почте
EMAIL_ACCOUNT   = str_settings[0].strip()
PASSWORD        = str_settings[1].strip()
HOST            = str_settings[2].strip()
SSL             = str_settings[3].strip()
PORT            = str_settings[4].strip()

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
except:
    print('подключение к почте было прервано') 
    quit()

x = 0
email_from = ''
list_email_from = list()
for x in range(i):
    #получаем все сообщение с почты
    latest_email_uid = data[0].split()[x]
    result, email_data = mail.fetch(latest_email_uid, "(RFC822)")

    encod = default_charset
    raw_email = email_data[0][1]
    raw_email_string = raw_email.decode(encoding = encod)
    email_message = email.message_from_string(raw_email_string)
    encod = email_message.get_content_charset()

    # находим от кого пришло письмо и записываем отправителя в список
    email_from = str(email.header.make_header(email.header.decode_header(email_message['From'])))
    list_email_from.append(email_from)
    print('собщение' + str(x) + ' от кого: ' + email_from)

    #удаляем сообщение с почты
    mail.store(latest_email_uid, '+FLAGS', '\\Deleted')

file = open('delet_log.txt', 'a+', encoding=ut8)    
file.write( '\nдата и время удаления сообщений: ' + str(datetime.datetime.now()) +
            '\nколичество удалённых сообщений: ' + str(x) +
            '\nот кого были удалённые сообщения: ' + str(list_email_from))
file.close()

mail.close()