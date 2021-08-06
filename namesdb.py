import sqlite3, datetime, multiprocessing, time
from sqlite3 import Error
from selenium.webdriver.common.keys import Keys
from registration2 import driver


def start(term, career):
    """
    open dukehub landing page and navigate to public class search
    """
    driver.get(
        "https://dukehub.duke.edu/psc/CSPRD01/EMPLOYEE/SA/s/WEBLIB_HCX_GN.H_SPRINGBOARD.FieldFormula.IScript_Main"
        "?&institution=DUKEU")
    catalog = driver.find_element_by_xpath("/html/body/div/main/div/div/div[4]/div/button")
    catalog.click()
    iframe = driver.find_element_by_xpath("/html/body/div[1]/iframe")
    driver.switch_to.frame(iframe)
    t = driver.find_element_by_xpath("/html/body/div[1]/main/div/form/div/div[2]/div/div/div/input")
    t.clear()
    t.send_keys(term)
    t.send_keys(Keys.ARROW_DOWN)
    t.send_keys(Keys.RETURN)
    time.sleep(4)
    c = driver.find_element_by_xpath("/html/body/div[1]/main/div/form/div/div[3]/div/div/div/input")
    c.clear()
    c.send_keys(career)
    c.send_keys(Keys.ARROW_DOWN)
    c.send_keys(Keys.RETURN)
    closed = driver.find_element_by_xpath("/html/body/div[1]/main/div/form/div/div[22]/label/span[1]/span[1]/input")
    closed.click()


def get_class(x):
    """
    search for class number and return name
    """
    classNumber = driver.find_element_by_xpath("/html/body/div[1]/main/div/form/div/div[7]/div/div/div/input")
    classNumber.clear()
    classNumber.send_keys(x)
    search = driver.find_element_by_xpath("/html/body/div[1]/main/div/form/div/div[20]/button")
    search.click()
    time.sleep(4)
    details = [x.text for x in
               driver.find_elements_by_xpath("//div[contains(@class, 'MuiGrid-root MuiGrid-container')]")]
    cn = driver.find_element_by_xpath("/html/body/div[1]/main/div/form/div/div[7]/div/div/div/input")
    for i in range(len(str(x))):
        cn.send_keys(Keys.BACKSPACE)
    try:
        findtopic = details[1].split("\n")
        topic = findtopic[14]
        nt = findtopic[0].split(" | ")
        className = nt[0]
        dept = nt[1].split(" ")[0]
        catnum = nt[1].split(" ")[1]
        return className, dept, catnum, topic, x
    except IndexError:
        return "not found", "NA", "NA", "NA", x


def get_numbers(dept):
    conn1 = sqlite3.connect("/Users/nadiabey/PycharmProjects/classRegistration/fall21.db")
    cur = conn1.cursor()
    cur.execute("""SELECT class_number from {}""".format(dept))
    nums = cur.fetchall()  # list of tuples
    conn1.close()
    return [x[0] for x in nums]


def classtable():
    table = """ CREATE TABLE IF NOT EXISTS courses (
    course_name text,
    department text,
    catalog_num text,
    topic text,
    course_number integer
    );"""
    conn2 = sqlite3.connect("/Users/nadiabey/PycharmProjects/classRegistration/classes.db")
    if conn2 is not None:
        try:
            c = conn2.cursor()
            c.execute(table)
            conn2.close()
        except Error as e:
            print(e)
    else:
        print("Error - cannot make connection")


def addtodb(vals):
    conn2 = sqlite3.connect("/Users/nadiabey/PycharmProjects/classRegistration/classes.db")
    add = """ INSERT INTO courses values(?,?,?,?,?)"""
    cur = conn2.cursor()
    for x in vals:
        cur.execute(add, x)
    conn2.commit()
    conn2.close()
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
        dept = subj[0:subj.index("-") - 1]
    except ValueError:
        dept = subj
    if "&" in dept:
        dept = dept.replace("&", "")
    print(dept, "started at", datetime.datetime.now())
    names(dept)
    print(dept, "ended at", datetime.datetime.now())


def main(listy):
    pool = multiprocessing.Pool()
    pool.starmap(find, [("2021 Fall Term", "Undergraduate", x) for x in listy])
    pool.close()
    driver.quit()


if __name__ == '__main__':
    fall = [x[:-1] for x in open('fall21dept.txt', 'r').readlines()]
    main(fall)
    #testlist = ['AAAS -']
    #for x in testlist:
    #    find("2021 Fall Term", "Undergraduate", x)
