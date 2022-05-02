import numpy, datetime
import sqlite3, random, requests, string, time
import threading

def user_exists(user_id):
    try:
        with sqlite3.connect("data.db") as con:
            cur = con.cursor()
            result = cur.execute('SELECT * FROM `users` WHERE `id` = ?', (user_id,)).fetchall()
            return bool(len(result))
    except:
        return False

def create_user(user_id):
    money = float(prj_info(3))    
    time = datetime.date.today()
    
    try:
        with sqlite3.connect("data.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO `users` (`id`, `date`, `refers`, `balance`, `refer`) VALUES(?,?,?,?,?)", (user_id, time, 0, money, None))
    except:
        pass
    

def update_refers(user_id, refer_id):
    try:
        with sqlite3.connect("data.db") as con:
            cur = con.cursor()
            result = cur.execute('SELECT * FROM `users` WHERE `id` = ?', (refer_id,)).fetchall()
            for row in result:
                cur.execute("UPDATE `users` SET `refers` = ? WHERE `id` = ?", (row[2]+1, refer_id))
                coin = prj_info(0)
                balance = float(row[3]) + float(coin)
            cur.execute("UPDATE `users` SET `balance` = ? WHERE `id` = ?", (balance, refer_id))
            cur.execute("UPDATE `users` SET `refer` = ? WHERE `id` = ?", (refer_id, user_id))
    except:
        pass


def amount_users():
    try:
        with sqlite3.connect("data.db") as con:
            cur = con.cursor()
            cur.execute("SELECT COUNT (*) FROM users")
            amount_users = cur.fetchone()[0]
        return amount_users
    except:
        pass


def update_balance(user_id):
    try:
        with sqlite3.connect("data.db") as con:
            cur = con.cursor()
            cur.execute("UPDATE `users` SET `balance` = ? WHERE `id` = ?", (0, user_id))
    except:
        pass



def user_info(user_id, info):
    try:
        with sqlite3.connect("data.db") as con:
            cur = con.cursor()
            result = cur.execute("SELECT * FROM `users` WHERE `id` = ?", (user_id,)).fetchall()
            for row in result:
                return row[info]
    except:
        pass

def prj_info(info):
    try:
        with sqlite3.connect("data.db") as con:
            cur = con.cursor()
            result = cur.execute('SELECT * FROM `settings`', ()).fetchall()
            for row in result:
                return row[info]
    except:
        pass

def links():
    try:
        array = []
        with sqlite3.connect("data.db") as con:
            cur = con.cursor()
            result = cur.execute('SELECT * FROM `channel`', ()).fetchall()
            for row in result:
                array.append(
                    f"{row[0]}:{row[1]}")

            return array
    except:
        pass