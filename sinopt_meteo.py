from calendar import month
import datetime
from distutils.log import error
import email
from gettext import find
import imaplib
import ssl
from statistics import median
from gtts import gTTS 
import os
from playsound import playsound
import subprocess
from subprocess import Popen, PIPE
from time import sleep
import sys

#Кодировки текста писем и файлов
default_charset = 'koi8-r'
coir = 'koi8-r'
cp = 'cp1251'
ut8 = 'utf-8'
ut16 = 'utf-16'

# поределяем время день на сегодня и день на завтра
now = datetime.datetime.now() 
tomorrow = now + datetime.timedelta(days=1)

curent_time = int(now.strftime("%H"))       # час
minutes = int(now.strftime("%M"))           # минута
day = int(now.strftime("%d"))               # сегодняшний день
tomorrow_day = int(tomorrow.strftime("%d")) # завтрашний день
months = int(now.strftime("%m"))            # месяц
year = now.strftime("%Y")                   # год
str_mounths = ''

print('дата на завтра день:', tomorrow_day)
print('день: ' + str(day))
print('месяц: '+ str(months))
print('год: '+ str(year))
print("Текущее время: "+ str(curent_time))
print('Минуты: '+ str(minutes))

mounts_list = [ 'Января', 'Февраля', 
                'Марта', 'Апреля', 
                'Мая', 'Июня', 
                'Июля', 'Августа', 
                'Сентября', 'Октября', 
                'Ноября', 'Декабря' ]

day_list = ['первого', 'второго', 'третьего', 'четвёртого', 
            'пятого', 'шестого', 'седьмого', 'восьмого', 
            'девятого', 'десятого', 'одиннадцатого', 'двенадцатого', 
            'тринадцатого', 'четырнадцатого', 'пятнадцатого', 'шестнадцатого',
            'семнадцатого', 'восемнадцатого', 'девятнадцатого', 'двадцатого',
            'двадцать первого', 'двадцать второго', 'двадцать третьго','двадцать четвёртого', 
            'двадцать пятого', 'двадцать шестого', 'двадцать седьмого', 
            'двадцать восьмого', 'двадцать девятого', 'тридцатого', 'тридцать первого']

#переводим месяц из числа в строку
for i in range(len(mounts_list)):
    if months == i+1:
        str_mounths = mounts_list[i]    

str_tomorrow_day = ''
str_day = ''

#переводим даты из чисел в строку
for j in range(len(day_list)):
    if tomorrow_day == j:
        str_tomorrow_day = day_list[tomorrow_day-1]
    
        print('j:', j)
        print('next_day:', str_tomorrow_day)
    str_day = day_list[day-1]

print('текущий месяц: ', str_mounths)

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
EMAIL_GIDROLOG  = str_settings[5]
EMAIL_WEATHER   = str_settings[6]
EMAIL_METEO     = str_settings[7]
PATCH_TO_SAVE   = str_settings[8]

print('Адрес входящих писем:', EMAIL_ACCOUNT)
print('Пароль для почты входящих писем:', PASSWORD)
print('HOST для подлкючения:', HOST)
print('Запрос SSL:', SSL)
print('PORT для подключения:', PORT)
print('EMAIL гидрологов:', EMAIL_GIDROLOG)
print('EMAIL синоптиков:', EMAIL_WEATHER)
print('EMAIL метеорологов:', EMAIL_METEO)
print('Путь для сохранения файла голоса и текста:', PATCH_TO_SAVE)

#подключаемся к почте 
try: 
    if SSL == 'yes' and PORT.isnumeric():
        PORT = int(PORT)
        mail = imaplib.IMAP4_SSL(HOST, PORT)
    else:
        mail = imaplib.IMAP4(HOST)
        print(mail)
except:  
    print(  'не удалось записать голос по ряду причин возможно программа не смогла подключиться к интернету, ' + 
            'потому что он полное дно в гидромете, возможно вы сами сломали программу с чем и поздравляю ' + 
            'возможно на землю упал метеорит и уже никому нет дела до этой фигни ' + 
            'выберите наиболее понравившийся вам вариант и просто перезапустите программу LOL.')
    sleep(10)
    quit()

#удаляем старые записи файлов для создания новых
if os.path.isfile(PATCH_TO_SAVE + 'погода.wav'):
    #os.remove(PATCH_TO_SAVE + 'voise.mp3')
    #os.remove(PATCH_TO_SAVE + 'vois_text.txt')
    os.remove(PATCH_TO_SAVE + 'погода.wav')
    print('старый прогноз успешно удалён')
else:
    print('файлы не найдены в папке')

mail.login(EMAIL_ACCOUNT, PASSWORD)
mail.list()
mail.select('inbox')
result, data = mail.search(None, 'ALL') # (ALL/UNSEEN)

i = len(data[0].split())

print('Количество писем:', i)

#создаём переменные для содержимого писем от гидрологов, синоптиков, метеорологов
str_weather = ''
str_meteo = ''
text_to_speach = ''
times = ''

for x in range(i):
    #получаем все сообщение с почты
    latest_email_uid = data[0].split()[x]
    print('data[0]', data[0])
    print('latest_email_uid', latest_email_uid)
    print('latest_email_uid', type(latest_email_uid))
    
    result, email_data = mail.fetch(latest_email_uid, "(RFC822)")

    encod = default_charset
    raw_email = email_data[0][1]
    raw_email_string = raw_email.decode(encoding = encod)
    email_message = email.message_from_string(raw_email_string)
    encod = email_message.get_content_charset()
    print(encod)

    # Header Details
    date_tuple = email.utils.parsedate_tz(email_message['Date'])
    if date_tuple:
        local_date = datetime.datetime.fromtimestamp(email.utils.mktime_tz(date_tuple))
        local_message_date = "%s" %(str(local_date.strftime("%a, %d %b %Y %H:%M:%S")))
    email_from = str(email.header.make_header(email.header.decode_header(email_message['From'])))
    email_to = str(email.header.make_header(email.header.decode_header(email_message['To'])))
    subject = str(email.header.make_header(email.header.decode_header(email_message['Subject'])))

    print('собщение' + str(x) + ' от кого: ' + email_from)
    print('собщение' + str(x) + ' кому:'     + email_to)
    print('собщение' + str(x) + ' тема: '    + subject)
    if  curent_time == 6 and minutes >= 40:
        mail.store(latest_email_uid, '+FLAGS', '\\Deleted')
        print('удалены все сообщения за прошедший день')
    else: 
        for part in email_message.walk():
            if part.get_content_type() == "text/plain":
                charset = part.get_content_charset()
                body = part.get_payload(decode=True).decode(encoding = encod)
                file_name = "email_" + str(x) + ".txt"
                
                #проверяем записано ли уже в строку str_weather письмо если не записано то записывает иначе пропускаем блок синоптиков
                if str_weather == '':
                    print('синоптики 2')
                    if email_from.find(EMAIL_WEATHER) != -1:
                        print('синоптики 2.2')
                        print('найдена почта синоптиков\n')
                        # Формирование тела письма для синоптиков
                        serch_str_homel = 'ПО Г. ГОМЕЛЮ'
                        homel_start = body.find(serch_str_homel)
                        serch_str_warning = 'УРОВЕНЬ ОПАСНОСТИ)'
                        serch_str_warning_len = len(serch_str_warning)
                        serch_str_len = len(serch_str_homel)
                        print('Уровень опасности', body.find(serch_str_warning))

                        # проверяем текст письма на наличие предупреждений и удаляем ненужные элементы
                        if body.find(serch_str_warning) != -1:
                            str_weather = body[
                            body.find(serch_str_warning, homel_start) + serch_str_warning_len :
                            body.find('=', body.find(serch_str_homel))].replace('М/С', 'метров в секунду'
                            ).replace('\n', ''
                            ).replace('\r', ''
                            ).replace('\t', ''
                            ).replace('МИНСК ПОГОДА-', ''
                            ).replace('\b', '').strip().lower() + '. '
                            print('!!!!!найдено предупреждение от синоптиков!!!!')
                        else:
                            str_weather = body[
                            body.find(serch_str_homel, homel_start) + serch_str_len :
                            body.find('=', body.find(serch_str_homel))].replace('М/С', 'метров в секунду'
                            ).replace('МИНСК ПОГОДА-', ''
                            ).replace('\n', ''
                            ).replace('\r', ''
                            ).replace('\t', ''
                            ).replace('\b', ''
                            ).strip().lower() + '. '
                            print('!не найдено предупреждение от синоптиков!')
                        print('Сообщение от синоптиков:', str_weather)
                        mail.store(latest_email_uid, '+FLAGS', '\\Deleted')
                        print('удалено сообщение синоптиков')

                #проверяем записано ли уже в строку str_meteo письмо если не записано то записывает иначе пропускаем блок метео
                if str_meteo == '':
                    print('метеорологи 3')
                    if email_from.find(EMAIL_METEO) != -1:
                        print('метеорологи 3.3')
                        print('найдена почта метеорологов\n')

                        dict_on_replace = {'км' : 'киллометров', '_' : ' ', 'мм.рт.ст' : 'миллиметров ртутного столба.', 'норма' : 'нормы',
                                    'гПа': ' гекто паскалей', 'ум' : 'умеренный', 'умеренныйеренный' : 'умеренный', '%' : '%. ',
                                    'с-з' : 'северо-западный', 'с-в' : 'северо-восточный', 'ю-в' : 'юго-восточный', 'ю-з' : 'юго-западный',
                                    'с.з' : 'северо-западный', 'с.в' : 'северо-восточный', 'ю.в' : 'юго-восточный', 'c з' : 'северо-западный',
                                    'c в' : 'северо-восточный', 'ю в' : 'юго-восточный', 'ю з' : 'юго-западный', 'С з' : 'северо-западный',
                                    'С в' : 'северо-восточный', 'Ю в' : 'юго-восточный', 'Ю з' : 'юго-западный', 'С.з' : 'северо-западный',
                                    'С.в' : 'северо-восточный', 'Ю.в' : 'юго-восточный', 'Ю.з' : 'юго-западный', 'С-з' : 'северо-западный',
                                    'С-в' : 'северо-восточный', 'Ю-в' : 'юго-восточный', 'Ю-з' : 'юго-западный', 'с З' : 'северо-западный',
                                    'с В' : 'северо-восточный', 'ю В' : 'юго-восточный', 'ю З' : 'юго-западный', 'с.З' : 'северо-западный',
                                    'с.В' : 'северо-восточный', 'ю.В' : 'юго-восточный', 'ю.З' : 'юго-западный', 'с-З' : 'северо-западный',
                                    'с-В' : 'северо-восточный', 'ю-В' : 'юго-восточный', 'ю-З' : 'юго-западный', 'С З' : 'северо-западный',
                                    'С В' : 'северо-восточный', 'Ю В' : 'юго-восточный', 'Ю З' : 'юго-западный', 'С-З' : 'северо-западный',
                                    'С-В' : 'северо-восточный', 'С-В' : 'юго-восточный', 'С-З' : 'юго-западный', 'С.З' : 'северо-западный',
                                    'С.В' : 'северо-восточный', 'Ю.В' : 'юго-восточный', 'Ю.З' : 'юго-западный', 'СЗ' : 'северо-западный',
                                    'СВ' : 'северо-восточный', 'ЮВ' : 'юго-восточный', 'ЮЗ' : 'юго-западный', 'cЗ' : 'северо-западный',
                                    'cВ' : 'северо-восточный', 'юВ' : 'юго-восточный', 'юЗ' : 'юго-западный', 'Сз' : 'северо-западный',
                                    'Св' : 'северо-восточный', 'Юв' : 'юго-восточный', 'Юз' : 'юго-западный',
                                    '\n' : '', '\r' : '', '\t' : '', '\b' : '' }
                        str_meteo = body
                        for key, value in dict_on_replace.items():
                            str_meteo = str_meteo.replace(key, value)
                                    
                        str_meteo = str_meteo.replace(str_meteo[0 : (str_meteo.find(year) + len(year)) + 2], '' )
                        if str_meteo.find('нет') != -1:
                            str_meteo = str_meteo.replace('(Явления)', 'Явлений')
                            print('слово "НЕТ" найдено на позиции:', str_meteo.find('нет'))
                        print("Сообщение с метео: ", str_meteo)
                        mail.store(latest_email_uid, '+FLAGS', '\\Deleted')
                        print('удалено сообщение от метеорологов')
                        if times == '':
                            if curent_time >= 5 and curent_time < 7:
                                times += 'сегодня ' + str_day + ' ' + str_mounths + '. '
                                print(times)
                                print('формирование голоса на 06 часов:')
                            elif curent_time >= 7 and  curent_time < 10:
                                times += 'сегодня ' + str_day + ' ' + str_mounths + '. '
                                print(times)
                                print('формирование голоса на 09 часов:')
                            elif curent_time >= 10 and  curent_time < 18:
                                times += 'в ближайшие сутки ' + str_day + ' на ' + str_tomorrow_day + ' ' + str_mounths + '. '
                                print(times)
                                print('формирование голоса на 15 часов:')
            else:
                continue

# записываем время + проноз от гидрологов + синоптиков + прогоноз от метеорологов
output_file = open(PATCH_TO_SAVE + 'vois_text.txt', 'w',  encoding = ut16)
output_file.write("По данным Гомель облгидро мет " + times + str_weather + str_meteo)
output_file.close()
#открытие файла чтение текста и перевод в голос
voise_file = open(PATCH_TO_SAVE + 'vois_text.txt', "r", encoding = ut16).read()
language = 'ru'
speech = gTTS(text = voise_file, lang = language, slow = False)
speech.save(PATCH_TO_SAVE + "voise.mp3")

audi_decode = subprocess.Popen(['ffmpeg', '-i', PATCH_TO_SAVE + 'voise.mp3', 
                    PATCH_TO_SAVE + 'погода.wav'])
print('идёт процесс записи потерпите немного и не закрывайте окно PLEAS')   
#sleep(60)
#закрываем соединение по протоколу imap
mail.close()
#удаляем избыточные файлы из папки
    
