import datetime, time, multiprocessing, sqlite3
from sqlite3 import Error
from selenium.webdriver.common.keys import Keys
from registration2 import init, get_term, get_career, show_all, search_button, page_end, driver

conn = sqlite3.connect("/Users/nadiabey/PycharmProjects/classRegistration/fall21.db")
driver.implicitly_wait(10)


def start(term, career):
    init()
    get_term(term)
    get_career(career)
    show_all()


def depttable(dept):
    table = """ CREATE TABLE IF NOT EXISTS {} (
        section_type text,
        section_number text,
        class_number integer,
        open_seats integer,
        total_seats integer,
        reserved text,
        percent numeric,
        timestamp text
        );""".format(dept)
    if conn is not None:
        try:
            c = conn.cursor()
            c.execute(table)
        except Error as e:
            print(e)
    else:
        print("Error - cannot make connection")


def deptinsert(dept, vals):
    add = """ INSERT INTO {} values(?,?,?,?,?,?,?,?)""".format(dept)
    cur = conn.cursor()
    cur.execute(add, vals)
    conn.commit()
    return cur.lastrowid


def num_search(y):
    temp = []
    for item in y:
        if "Class Number" in item:
            index = item.rfind('r')
            num = item[index + 1:]
            section = item[0:item.find(',')]
            temp.append(section.split(" Section ")[0]) # index 0
            temp.append(section.split(" Section ")[1]) # index 1
            temp.append(num) # index 2

        if "seats" in item:
            # reserved and waitlist use rfind because 'seats' is present multiple times
            if "reserved" in item:
                if "Closed" not in item:
                    avail = int(item[item.find('d,') + 3:item.find('of') - 1])
                    total = int(item[item.find('of') + 3:item.rfind('seats') - 1])
                    temp.append(avail) # index 3
                    temp.append(total) # index 4
                else:
                    avail = int(item[item.rfind('d,') + 3:item.find('of') - 1])
                    total = int(item[item.find('of') + 3:item.rfind('seats') - 1])
                    temp.append(avail)
                    temp.append(total)
                temp.append("Yes") # index 5
            elif "waitlist" in item:
                avail = int(item[item.find('e.') + 3:item.rfind('of') - 1])
                total = int(item[item.rfind('of') + 3:item.rfind('seats') - 1])
                temp.append(avail)
                temp.append(total)
                temp.append("No")
            else:
                avail = int(item[item.find(',') + 2:item.find('of') - 1])
                total = int(item[item.find('of') + 3:item.find('seats') - 1])
                temp.append(avail)
                temp.append(total)
                temp.append("No")
            try:
                percent = ((total - avail) / total * 100) # index 6
                temp.append(percent)
            except ZeroDivisionError:
                percent = 9999
                temp.append(percent)
            finally:
                temp.append(str(datetime.datetime.now())) # index 7
    return temp


def department(dept):
    try:
        name = dept[0:dept.index("-") - 1]
    except ValueError:   # for strings without hyphens keep same one (i.e. mech engineering)
        name = dept
    if "&" in name:
        name = name.replace("&","")  # remove extra symbol to avoid sql syntax error
    subject = driver.find_element_by_xpath("/html/body/div[1]/main/div/form/div/div[4]/div/div/div/input")
    subject.clear()
    subject.send_keys(dept)
    subject.send_keys(Keys.ARROW_DOWN)
    subject.send_keys(Keys.RETURN)
    search_button()
    print(name)
    begin = time.time()
    page_end()
    data = [x.text for x in driver.find_elements_by_xpath("//span[contains(@class, 'sr-only')]")]
    classes = num_search(data)
    values = []
    for y in [classes[x:x+8] for x in range(0, len(classes), 8)]:
        values.append((y[0],y[1],y[2],y[3],y[4],y[5],y[6],y[7]))
    depttable(name)
    for x in values:
        deptinsert(name, x)
    end = time.time()
    print(name, end - begin)


def run(term, career, dept):
    start(term, career)
    department(dept)


if __name__ == '__main__':
    fall = [x[:-1] for x in open('fall21dept.txt', 'r').readlines()]
    print("start time:", str(datetime.datetime.now()))
    first = time.time()
    pool = multiprocessing.Pool()
    pool.starmap(run, [("2021 Fall Term", "Undergraduate", x) for x in fall])
    pool.close()
    driver.quit()
    last = time.time()
    print("end time:", str(datetime.datetime.now()))
    print("time elapsed:", last - first, "seconds")