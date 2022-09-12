from dataclasses import dataclass
from pickletools import read_uint1
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
            "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("db.json", scope)
opener = gspread.authorize(creds)
sheet = opener.open("DSA-BOOTCAMP")

def rows(work):
    wks = sheet.worksheet(work)
    return len(wks.get_all_records())

def allRec(work):
    wks = sheet.worksheet(work)
    return wks.get_all_records()

def addUser(name, fname, email, pswd):
    wks = sheet.worksheet("Sheet2")
    n = rows("Sheet2")
    n += 2
    dt = datetime.now()
    dt.strftime("%d-%m-%Y %H:%M:%S")
    
    wks.update_cell(n, 1, name)
    wks.update_cell(n, 2, fname)
    wks.update_cell(n, 3, email)
    wks.update_cell(n, 4, pswd)
    wks.update_cell(n, 5, str(dt))

def check_username(username):
    wks = sheet.worksheet("Sheet2")
    data = wks.get_all_records()

    for i in data:
        if i['username'] == username:
            return str(i['password'])
    return False

def getName(username):
    wks = sheet.worksheet("Sheet2")
    data = wks.get_all_records()

    for i in data:
        if i['username'] == username:
            return [str(i['full name']), str(i['email'])]
    return False

def check_mail(mail):
    wks = sheet.worksheet("Sheet2")
    data = wks.get_all_records()

    for i in data:
        if i['email'] == mail:
            return True
    return False

    print(data)