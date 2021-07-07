import pandas as pd
from selenium import webdriver
import time
import datetime
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")
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
    time.sleep(4)
    className = driver.find_element_by_xpath("//div[contains(@class, 'MuiGrid-root css-1veqt9o MuiGrid-item')]")
    cn = driver.find_element_by_xpath("/html/body/div[1]/main/div/form/div/div[7]/div/div/div/input")
    for ch in x:
        cn.send_keys(Keys.BACKSPACE)
    return className.text, x


if __name__ == '__main__':
    nums = [x[:-1] for x in open('class numbers 2021-07-06 20:22:02.635226.txt')]
    courses = []
    digits = []
    init()
    get_term("2021 Fall Term")
    get_career("Undergraduate")
    show_all()
    start = time.time()
    print("start time:", datetime.datetime.now())
    for x in nums:
        obj = get_class(x)
        print(obj)
        courses.append(obj[0])
        digits.append(obj[1])
    end = time.time()
    print("time: ", end - start)
    print("end time:", datetime.datetime.now())
    final = pd.DataFrame({"Name": courses, "Course Number": digits})
    final.to_csv('classnumberstest.csv')