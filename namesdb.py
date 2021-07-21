import sqlite3, datetime, multiprocessing
from sqlite3 import Error
from class_name import get_class
from registrationdb import start
from registration2 import driver

conn1 = sqlite3.connect("/Users/nadiabey/PycharmProjects/classRegistration/fall21.db")
conn2 = sqlite3.connect("/Users/nadiabey/PycharmProjects/classRegistration/fallclasses.db")
driver.implicitly_wait(10)


def get_numbers(dept):
    cur = conn1.cursor()
    cur.execute("""SELECT class_number from {}""".format(dept))
    nums = cur.fetchall()  # list of tuples
    return [x[0] for x in nums]


def classtable():
    table = """ CREATE TABLE IF NOT EXISTS courses (
    course_name text
    topic text
    course_number integer
    );"""
    if conn2 is not None:
        try:
            c = conn2.cursor()
            c.execute(table)
        except Error as e:
            print(e)
    else:
        print("Error - cannot make connection")


def addtodb(vals):
    add = """ INSERT INTO courses values(?,?,?)"""
    cur = conn2.cursor()
    cur.execute(add, vals)
    conn2.commit()
    return cur.lastrowid


def names(dept):
    classes = []
    for x in get_numbers(dept):
        item = get_class(x)
        classes.append(item)
    classtable()
    addtodb(classes)


def find(term, career, subj):
    start(term, career)
    try:
        dept = subj[0:subj.index("-")-1]
    except ValueError:
        dept = subj
    if "&" in dept:
        dept = dept.replace("&","")
    print(dept, "started at", datetime.datetime.now())
    names(dept)
    print(dept, "ended at", datetime.datetime.now())


if __name__ == '__main__':
    fall = [x[:-1] for x in open('fall21dept.txt', 'r').readlines()]
    pool = multiprocessing.Pool()
    pool.starmap(find, [("2021 Fall Term", "Undergraduate", x) for x in fall])
    pool.close()
    driver.quit()