from pykeepass import PyKeePass, create_database
from pykeepass.exceptions import CredentialsError
from pathlib import Path
import string
import random
import uuid
import os


path = Path('media/dbs/').absolute()


def create_db(password):
    filename = f"{uuid.uuid4()}.kdbx"
    file = os.path.join(path, filename)
    create_database(filename=file, password=password)
    return file


def open_file(db_path, pwd_db):
    try:
        pyk = PyKeePass(filename=db_path, password=pwd_db)
        return pyk
    except FileNotFoundError or CredentialsError:
        return False


def change_file_password(db_path, pwd_db, password):
    pyk = open_file(db_path, pwd_db)
    pyk.password = password
    pyk.save()


def add_password(db_path, pwd_db, title, username, password, url):
    pyk = open_file(db_path, pwd_db)
    entry = find_password(pyk, title)
    if not entry:
        pyk.add_entry(title=title, username=username, password=password, url=url, destination_group=pyk.root_group)
        pyk.save()


def password_update(db_path, pwd_db, title, new_title, username, password, url):
    pyk = open_file(db_path, pwd_db)
    entry = find_password(pyk, title)
    entry.title = new_title
    entry.username = username
    entry.password = password
    entry.url = url
    pyk.save()


def delete_password(db_path, pwd_db, title):
    pyk = open_file(db_path, pwd_db)
    entry = pyk.find_entries(title=title, first=True)
    pyk.delete_entry(entry=entry)
    pyk.save()


def find_password(pyk, title):
    try:
        pwd = pyk.find_entries(title=title, first=True)
        print(pwd)
        if pwd:
            return pwd
        return None
    except AttributeError:
        return None


def check_pwd(pwd):
    if len(pwd) < 3:
        password = random_pwd(int(pwd))
        return password
    else:
        return pwd


def random_pwd(length):
    characters = string.ascii_letters + string.digits
    amount = int(length)
    result_str = ''.join(random.choice(characters) for i in range(amount))
    return result_str


def validate_pwd(title, pwd):
    if title == "":
        return False
    if pwd == "":
        return False
    return True
