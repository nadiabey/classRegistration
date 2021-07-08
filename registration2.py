import datetime, time, multiprocessing, os
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By

"""
This version of the script excludes the class_name function in favor of getting all course names one time.
"""

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")
driver = webdriver.Chrome(r"/Users/nadiabey/PycharmProjects/classRegistration/chromedriver 2", options=chrome_options)
driver.implicitly_wait(10)


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
    finally:
        time.sleep(3)


def num_search(listy):
    """
    get info for class number
    """
    temp = []
    for item in listy:
        if "Class Number" in item:
            index = item.rfind('r')
            num = item[index + 1:]
            section = item[0:item.find(',')]
            temp.append(section)  # index 0
            temp.append(num)  # index 1

        if "seats" in item:
            # reserved and waitlist use rfind because 'seats' is present multiple times
            if "reserved" in item:
                if "Closed" not in item:
                    avail = int(item[item.find('d,') + 3:item.find('of') - 1])
                    total = int(item[item.find('of') + 3:item.rfind('seats') - 1])
                    temp.append(avail)  # index 2
                    temp.append(total)  # index 3
                    temp.append("Yes")  # index 4
                else:
                    avail = int(item[item.rfind('d,') + 3:item.find('of') - 1])
                    total = int(item[item.find('of') + 3:item.rfind('seats') - 1])
                    temp.append(avail)  # index 2
                    temp.append(total)  # index 3
                    temp.append("Yes")  # index 4
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
                temp.append((total - avail) / total * 100)  # index 5
                temp.append(str(datetime.datetime.now()))  # index 6
            except ZeroDivisionError:
                temp.append("check")
                temp.append(str(datetime.datetime.now()))

    return temp


def input_subject(x):
    """
    x - department
    returns dictionary of lists
    """
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
        time.sleep(3)
        secNum = driver.find_elements_by_xpath("//span[contains(@class, 'sr-only')]")
        y = [z.text for z in secNum]
        info = num_search(y)
        sections = info[0::7]
        numbers = info[1::7]
        availability = info[2::7]
        totals = info[3::7]
        reserves = info[4::7]
        percent = info[5::7]
        times = info[6::7]

        rows = {'Section': sections, 'Class Number': numbers, 'Open Seats': availability,
                'Total Seats': totals, 'Reserved Seats': reserves, 'Percent': percent, 'Timestamp': times}
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


def run(x, y, z, f):
    """
    run all functions
    x - term
    y - career
    z - subject
    f - filename
    """
    init()
    get_term(x)
    get_career(y)
    show_all()
    start = time.time()
    result = input_subject(z)
    end = time.time()
    print(z, end - start)
    if type(result) is None:
        pass
    else:
        df = pd.DataFrame(result)
        to_file(f, df)


def repeat(l):
    term = '2021 Fall Term'
    career = 'Undergraduate'
    print("start time: ", str(datetime.datetime.now()))
    first = time.time()
    pool = multiprocessing.Pool()
    pool.starmap(run, [(term, career, x,
                        os.path.join(r'/Users/nadiabey/PycharmProjects/classRegistration/data/',
                                     x + ' fall 2021.csv')) for x in l])
    pool.close()
    driver.quit()
    last = time.time()
    print("end time: ", str(datetime.datetime.now()))
    print("time elapsed:", last - first, "seconds")


if __name__ == '__main__':
    fall = [x[:-1] for x in open('fall21dept.txt', 'r').readlines()]
    day = datetime.datetime.today().day
    while datetime.datetime.now() < datetime.datetime(2021, 7, day, 8, 0):
        repeat(fall)
        if datetime.datetime.now() > datetime.datetime(2021, 7, day, 8, 0):
            break
