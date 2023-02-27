from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from seleniumwire import webdriver
from selenium_stealth import stealth
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
from assistant.settings import PROXY_OPTIONS
from bs4 import BeautifulSoup
import time
from assistant.settings import PATH_DRIVER


def get_page(url: str, proxy: bool = False, background: bool = False):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("start-maximized")
    if background:
        chrome_options.add_argument('headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    global PROXY_OPTIONS
    if proxy:
        seleniumwire_options = {
            'proxy': {
                'http': f'http://{PROXY_OPTIONS}',
                'https': f'https://{PROXY_OPTIONS}',
                'no_proxy': 'localhost,127.0.0.1'
            }
        }
        chrome = webdriver.Chrome(executable_path=PATH_DRIVER,
                                  service=Service(ChromeDriverManager().install()),
                                  options=chrome_options,
                                  seleniumwire_options=seleniumwire_options)
    else:
        chrome = webdriver.Chrome(executable_path=PATH_DRIVER,
                                  service=Service(ChromeDriverManager().install()),
                                  options=chrome_options)

    stealth(
        driver=chrome,
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko)Chrome/109.0.0.0 Safari/537.36",
        languages=["ru", "en"],
        platform="Win32",
        webgl_vendor="Google Inc. (NVIDIA)",
        renderer="ANGLE (NVIDIA, NVIDIA GeForce RTX 3060 Ti Direct3D11 vs_5_0 ps_5_0, D3D11)",
        fix_hairline=True,
        run_on_insecure_origins=False
    )
    chrome.set_page_load_timeout(5)
    try:
        chrome.get(url)
        time.sleep(4)
    except TimeoutException as ex:
        isrunning = 0
        # print("Exception has been thrown. " + str(ex))
        chrome.close()
        chrome.quit()
        return False
    return chrome


def website_availability_check(chrome: webdriver):
    if isinstance(chrome, type(webdriver.Chrome())):
        return True
    return False


def input_data_cab_mi(chrome: webdriver, task):
    id_in_doc_num = chrome.find_element(by=By.ID, value='id_in_doc_num')
    id_in_doc_num.send_keys(task.rzn_number)
    time.sleep(2)
    id_in_doc_num = chrome.find_element(by=By.ID, value='id_in_doc_dt')
    id_in_doc_num.send_keys(task.rzn_date)
    time.sleep(2)
    search = chrome.find_element(by=By.XPATH, value="/html/body/div[1]/div[5]/div/div/div[2]/div/form/button")
    search.click()
    time.sleep(3)
    return chrome


def input_data_le(chrome: webdriver, task):
    if task.type.id == 4:
        id_in_doc_num = chrome.find_element(by=By.ID, value='id_doc_num')
        id_in_doc_num.send_keys(task.rzn_number)
        time.sleep(2)
        id_in_doc_num = chrome.find_element(by=By.ID, value='id_doc_dt')
        id_in_doc_num.send_keys(task.rzn_date)
        type_select = Select(chrome.find_element(by=By.ID, value='id_doc_type'))
        type_select.select_by_value('1')
    elif task.type.id == 5:
        id_in_doc_num = chrome.find_element(by=By.ID, value='id_doc_num')
        id_in_doc_num.send_keys(task.dec_number)
        time.sleep(2)
        id_in_doc_num = chrome.find_element(by=By.ID, value='id_doc_dt')
        id_in_doc_num.send_keys(task.dec_date)
        type_select = Select(chrome.find_element(by=By.ID, value='id_doc_type'))
        type_select.select_by_value('2')
    time.sleep(2)
    search = chrome.find_element(by=By.XPATH,
                                 value="/html/body/div[1]/div[6]/div/div/div[2]/div[2]/form/button")
    search.click()
    time.sleep(3)
    return chrome


def input_data(chrome: webdriver, task):
    if task.type.id == 1 or task.type.id == 2 or task.type.id == 3:
        input_data_cab_mi(chrome, task)
    elif task.type.id == 4 or task.type.id == 5:
        input_data_le(chrome, task)
    return chrome


def close_webdriver(chrome: webdriver):
    chrome.close()
    chrome.quit()


def get_html(chrome: webdriver):
    return chrome.page_source


def get_page_screenshot(chrome: webdriver, path: str, name: str):
    ele = chrome.find_element(by=By.CLASS_NAME, value='m-cabinet')
    ele.screenshot(f"{path}/{name}.png")


def get_html_rzn_page(url: str):
    page = get_page(url, proxy=True)
    print(page)
    html = None
    if page == webdriver:
        print('html')
        html = get_html(page)
        close_webdriver(page)
    return html
