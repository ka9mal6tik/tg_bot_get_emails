import poplib
import email
from datetime import datetime
from email.header import decode_header
from email.utils import parsedate_to_datetime
from config import *


def check_email() -> dict:
    count = 0
    info_message = {}
    mail = poplib.POP3_SSL(pop3_server)
    mail.user(username)
    mail.pass_(password)
    numMessages = len(mail.list()[1])
    print(numMessages)
    list = []
    for i in range(1, numMessages):
        if count == 10:
            break
        for j in mail.retr(i)[1]:
            if j.decode().startswith('Reply-To: '):
                print(j.decode())
                list.append(i)
                info_message[str(i)] = j.decode()
                count += 1
                break

    mail.quit()
    return info_message


def check_email_body(id_email: str) -> str:
    length = 3_000
    mail = poplib.POP3_SSL(pop3_server)
    mail.user(username)
    mail.pass_(password)
    text_mail = ""
    length_count = 0
    for i in mail.retr(int(id_email))[1]:
        text_mail += i.decode()
        length_count += len(i.decode())
        if length_count > length:
            break
    mail.quit()
    return text_mail


def delete_email_message(id_email: str) -> None:
    mail = poplib.POP3_SSL(pop3_server)
    mail.user(username)
    mail.pass_(password)
    mail.dele(int(id_email))
    mail.quit()
