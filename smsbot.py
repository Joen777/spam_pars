
from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError
import configparser
import os, sys
import csv
import time
from pathlib import Path



def spam_message():#Текст отправки сообщение
    if Path('./text.md').is_file():
        md_str = ''
        with open(r"./text.md", "r", encoding="utf-8") as file:
            for line in file:
                md_str += line
        return md_str
    elif Path('./text.txt').is_file():
        txt_str = ''
        with open(r"./text.txt", "r", encoding="utf-8") as file:
            for line in file:
                txt_str += line
        return txt_str
    else:
        print('[ERROR] Текстовый файл не найден!')


re="\033"
gr="\033"
cy="\033"
SLEEP_TIME = 30
spam_msg = spam_message()


class main():

    def banner():

        print(f"Запустіть smsbot")

    def send_sms():
        try:
            cpass = configparser.RawConfigParser()
            cpass.read('config.data')
            api_id = cpass['cred']['id']
            api_hash = cpass['cred']['hash']
            phone = cpass['cred']['phone']
        except KeyError:
            os.system('clear')
            main.banner()
            print(re+"[!] run python3 setup.py first !!\n")
            sys.exit(1)

        client = TelegramClient(phone, api_id, api_hash)

        client.connect()
        if not client.is_user_authorized():
            client.send_code_request(phone)
            os.system('clear')
            main.banner()
            client.sign_in(phone, input(gr+'[+] Введите код: '+re))

        os.system('clear')
        main.banner()
        input_file = sys.argv[1]
        users = []
        with open(input_file, encoding='UTF-8') as f:
            rows = csv.reader(f, delimiter=",", lineterminator="\n")
            next(rows, None)
            for row in rows:
                user = {}
                user['username'] = row[0]
                user['id'] = int(row[1])
                user['access_hash'] = int(row[2])
                user['name'] = row[3]
                users.append(user)
        print(gr+"[1]Відправити смс по ідентифікатору користувача\n[2] відправити смс по імені користувача ")
        mode = int(input(gr+"Input : "+re))

        message = spam_msg

        for user in users:
            if mode == 2:
                if user['username'] == "":
                    continue
                receiver = client.get_input_entity(user['username'])
            elif mode == 1:
                receiver = InputPeerUser(user['id'],user['access_hash'])
            else:
                print(re+"[!]Неверный режим. Вихід.")
                client.disconnect()
                sys.exit()
            try:
                print(gr+"[+] Відправка повідомлення на:", user['name'])
                client.send_message(receiver, message.format(user['name']))
                print(gr+"[+] Ожидание {} секунд".format(SLEEP_TIME))
                time.sleep(30)
            except PeerFloodError:
                print(re+"[!] Получение помилки флуда из телеграммы. \n[!] Скрипт зараз зупиняється. \n[!]Повторіть спробу через некоторое время..")
                client.disconnect()
                sys.exit()
            except Exception as e:
                print(re+"[!] Помилка:", e)
                print(re+"[!] Спроба продовжити...")
                continue
        client.disconnect()
        print("Зроблений. Повідомлення надіслано всім користувачам.")


main.send_sms()

