import datetime
import os
import time
import multiprocessing
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")
chrome_driver = os.getcwd() + r"\\chromedriver.exe"
driver = webdriver.Chrome(r"/Users/nadiabey/PycharmProjects/classRegistration/chromedriver 2", options=chrome_options)


def init():
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


def get_term(x):
    """
    input given term (Fall 2021, etc)
    """
    term = driver.find_element_by_xpath("/html/body/div[1]/main/div/form/div/div[2]/div/div/div/input")
    term.clear()
    term.send_keys(x)
    term.send_keys(Keys.ARROW_DOWN)
    term.send_keys(Keys.RETURN)
    time.sleep(4)


def get_career(x):
    """
    input given career x (undergraduate, graduate, etc)
    """
    career = driver.find_element_by_xpath("/html/body/div[1]/main/div/form/div/div[3]/div/div/div/input")
    career.clear()
    career.send_keys(x)
    career.send_keys(Keys.ARROW_DOWN)
    career.send_keys(Keys.RETURN)


def show_all():
    """
    uncheck 'open classes only'
    """
    closed = driver.find_element_by_xpath("/html/body/div[1]/main/div/form/div/div[22]/label/span[1]/span[1]/input")
    closed.click()


def search_button():
    """
    click search
    """
    search = driver.find_element_by_xpath("/html/body/div[1]/main/div/form/div/div[20]/button")
    search.click()


def get_class(x):
    """
    search for class number and return name
    """
    classNumber = driver.find_element_by_xpath("/html/body/div[1]/main/div/form/div/div[7]/div/div/div/input")
    classNumber.clear()
    classNumber.send_keys(x)
    search_button()
    WebDriverWait(driver, 10).until(ec.visibility_of_all_elements_located)
    try:
        exist = driver.find_element_by_xpath("//span[contains(@role, 'alert')]")
    except NoSuchElementException:
        try:
            className = driver.find_element_by_xpath("//div[contains(@class, 'MuiGrid-root css-1veqt9o MuiGrid-item')]")
        except NoSuchElementException:
            return "name not found"
        else:
            return className.text
    else:
        try:
            if "We're sorry" in exist.text:
                print("Class", x, "has no results")
                o = open('class overflow.txt', 'a')
                o.write(x + "\n")
                o.close()
                return None
        except StaleElementReferenceException:
            WebDriverWait(driver, 10, ignored_exceptions=StaleElementReferenceException). \
                until(ec.presence_of_all_elements_located)
            exist = driver.find_element_by_xpath("//span[contains(@role, 'alert')]")
            if "We're sorry" in exist.text:
                print("Class", x, "has no results")
                o = open('class overflow.txt', 'a')
                o.write(x + "\n")
                o.close()
                return None
    finally:
        cn = driver.find_element_by_xpath("/html/body/div[1]/main/div/form/div/div[7]/div/div/div/input")
        for ch in x:
            cn.send_keys(Keys.BACKSPACE)


def page_end():
    """
    scroll to bottom of page to load all classes
    """
    try:
        driver.find_element_by_xpath("/html/body/div[1]/main/div/p/div/div[2]/span")
    except NoSuchElementException:
        ActionChains(driver).send_keys(Keys.END).perform()
        time.sleep(4)
        page_end()


def num_search(listy):
    """
    get info for class number
    """
    temp = []
    for item in listy:
        if "Class Number" in item:
            index = item.rfind('r')
            num = item[index + 1:]
            name = get_class(num)
            if type(name) is None:
                continue
            section = item[0:item.find(',')]
            temp.append(name)  # index 0
            temp.append(section)  # index 1
            temp.append(num)  # index 2

        if "seats" in item:
            # reserved and waitlist use rfind because 'seats' is present multiple times
            if "reserved" in item:
                avail = int(item[item.find('d,') + 3:item.find('of') - 1])
                total = int(item[item.find('of') + 3:item.rfind('seats') - 1])
                temp.append(avail)  # index 3
                temp.append(total)  # index 4
                temp.append("Yes")  # index 5
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
                temp.append((total - avail) / total * 100)  # index 6
                temp.append(str(datetime.datetime.now())) # index 7
            except ZeroDivisionError:
                temp.append("check")
                temp.append(str(datetime.datetime.now()))

    return temp


def input_subject(x):
    """
    x - department
    returns dictionary of lists
    """
    print(x)
    dept = driver.find_element_by_xpath("/html/body/div[1]/main/div/form/div/div[4]/div/div/div/input")
    dept.clear()
    dept.send_keys(x)
    dept.send_keys(Keys.ARROW_DOWN)
    dept.send_keys(Keys.RETURN)
    search_button()
    time.sleep(3)

    try:
        exist = driver.find_element_by_xpath("//span[contains(@role, 'alert')]")
        if "We're sorry" in exist.text:
            print(x, "has no results")
            o = open('dept overflow.txt', 'a')
            o.write(x + "\n")
            o.close()
            return None
    except NoSuchElementException:
        page_end()
        secNum = driver.find_elements_by_xpath("//span[contains(@class, 'sr-only')]")
        y = [z.text for z in secNum]
        before = time.time()
        info = num_search(y)
        names = info[0::8]
        sections = info[1::8]
        numbers = info[2::8]
        availability = info[3::8]
        totals = info[4::8]
        reserves = info[5::8]
        percent = info[6::8]
        times = info[7::8]

        rows = {'Class Name': names, 'Section': sections, 'Class Number': numbers, 'Open Seats': availability,
                'Total Seats': totals, 'Reserved Seats': reserves, 'Percent': percent, 'Timestamp': times}
        after = time.time()
        print(x, after - before)  # time elapsed
        return rows


def to_file(f, data):
    try:
        file = open(f)
        file.close()
    except IOError:
        # if file does not exist create it
        data.to_csv(f, index=False)
    else:
        # add to preexisting file
        data.to_csv(f, mode='a', index=False, header=False)


def run(x, y, z, f, t):
    """
    run all functions
    x - term
    y - career
    z - subject
    f - filename
    t - dept (d) or class (c)
    """
    init()
    get_term(x)
    get_career(y)
    show_all()
    if t == "c":
        name = get_class(z)
        if type(name) is None:
            pass
        else:
            classn = driver.find_elements_by_xpath("//span[contains(@class, 'sr-only')]")
            temp1 = [name]
            temp1.append(item for item in num_search(classn))
            temp2 = pd.DataFrame(temp1, columns=['Class Name', 'Section', 'Class Number', 'Open Seats',
                                                 'Total Seats', 'Reserved Seats', 'Percent', 'Timestamp'])
            to_file(f, temp2)
    elif t == "d":
        result = input_subject(z)
        if type(result) is None:
            pass
        else:
            df = pd.DataFrame(result)
            to_file(f, df)


if __name__ == '__main__':
    fallsubject = [x[:-1] for x in open('fall21dept.txt', 'r').readlines()]
    springsubject = [x[:-1] for x in open('spring21dept.txt', 'r').readlines()]
    term = '2021 Fall Term'
    career = 'Undergraduate'
    first = time.time()
    print("start time:", datetime.datetime.now())
    pool = multiprocessing.Pool()
    pool.starmap(run, [(term, career, x, x + " fall v6.csv", "d") for x in fallsubject])
    pool.close()

    if os.path.exists('dept overflow.txt') and os.stat('dept overflow.txt').st_size != 0:
        inc_dept = [x[:-1] for x in open('dept overflow.txt', 'r').readlines()]
        overflow = multiprocessing.Pool()
        overflow.starmap(run, [(term, career, x, x + " overflow.csv", "d") for x in inc_dept])
        overflow.close()
        clear = open('dept overflow.txt', 'w')
        clear.close()
    if os.path.exists('class overflow.txt') and os.stat('class overflow.txt').st_size != 0:
        inc_class = [x[:-1] for x in open('class overflow.txt', 'r').readlines()]
        overflow = multiprocessing.Pool()
        overflow.starmap(run, [(term, career, x, x + "overflow classes.csv", "c") for x in inc_class])
        clear = open('class overflow.txt', 'w')
        clear.close()

    driver.quit()
    last = time.time()
    print("end time:", datetime.datetime.now())
    print("time elapsed:", last - first, "seconds")
