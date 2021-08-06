import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
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

if __name__ == '__main__':
    init()
    get_term("2021 Fall Term")
    get_career("Undergraduate")
    show_all()
    dept = driver.find_element_by_xpath("/html/body/div[1]/main/div/form/div/div[4]/div/div/div/input")
    dept.clear()
    dept.send_keys("BIOLOGY")
    dept.send_keys(Keys.ARROW_DOWN)
    dept.send_keys(Keys.RETURN)
    search_button()
    time.sleep(3)
    page_end()
    details = [x.text for x in
               driver.find_elements_by_xpath("//div[contains(@class, 'MuiGrid-root MuiGrid-container')]")]
    for x in details:
        print(x.split('\n'))