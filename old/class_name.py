import pandas as pd
from selenium import webdriver
import time
import datetime
import os
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
    details = [x.text for x in driver.find_elements_by_xpath("//div[contains(@class, 'MuiGrid-root MuiGrid-container')]")]
    findtopic = details[1].split("\n")
    topic = findtopic[14]
    className = findtopic[0]
    cn = driver.find_element_by_xpath("/html/body/div[1]/main/div/form/div/div[7]/div/div/div/input")
    for i in range(len(str(x))):
        cn.send_keys(Keys.BACKSPACE)
    return className, topic, x


def get_list(file):
    df = pd.read_csv(file)
    numbers = df['Class Number'].unique().tolist()
    return numbers


def find(x):
    courses = []
    topics = []
    digits = []
    init()
    get_term("2021 Fall Term")
    get_career("Undergraduate")
    show_all()
    start = time.time()
    print("start time:", datetime.datetime.now())
    result = get_list(x)
    for item in result:
        obj = get_class(item)
        print(obj)
        courses.append(obj[0])
        topics.append(obj[1])
        digits.append(obj[2])
    end = time.time()
    print("time: ", end - start)
    print("end time:", datetime.datetime.now())
    df = pd.DataFrame({"Course Name": courses, "Topic": topics, "Course Number": digits})
    filename = x[:x.index('f')] + "class numbers.csv"
    df.to_csv(filename, index=False)


if __name__ == '__main__':
    depts = [x[:-1] for x in open('fall21dept.txt')]
    files = [os.path.join(r'/Users/nadiabey/PycharmProjects/classRegistration/data/',
                          x + ' fall 2021.csv') for x in depts]
    #test_list = [os.path.join(r'/Users/nadiabey/PycharmProjects/classRegistration/data/',
    #                          z + ' fall 2021.csv') for z in ['UNIV -']]
    for x in files:
        find(x)
