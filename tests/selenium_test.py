import queue
import threading
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

Q: queue.Queue = queue.Queue()
print(type(Q))
OLD_STR = 'Hi 老朋友欢迎你来学干货~'
NEW_STR = 'Hi 新伙伴欢迎你来学干货~'


class Webdriver(object):
    WEBDRIVER_COMMAND_EXECUTOR = 'http://localhost:4444/wd/hub'
    WEBDRIVER_EXTENSION_FILEPATH = '/mnt/d/wevsm/project/AwesomeBot/volumes/chrome/data/canvas-fingerprint-defend.crx'

    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('lang=zh_CN.UTF-8')
        self.options.add_argument('--disable-web-security')
        self.options.add_argument('--allow-running-insecure-content')
        # 加载插件
        self.options.add_extension(self.WEBDRIVER_EXTENSION_FILEPATH)
        self.driver = webdriver.Remote(
            command_executor=self.WEBDRIVER_COMMAND_EXECUTOR,
            options=self.options
        )
        # 最大等待时间10s
        self.driver.implicitly_wait(10)
        # 清除浏览器cookies
        self.driver.delete_all_cookies()

    def execute(self, url: str) -> bool:
        self.driver.get(url)
        time.sleep(2)
        # self.driver.close()
        self.driver.quit()
        return False


def put(q: queue.Queue, url: str):
    for i in range(10):
        time.sleep(0.3)
        print("put:", i, q.qsize())
        q.put({
            'id': i,
            'url': url
        })


def get(q: queue.Queue):

    while True:
        item: dict = q.get()
        print('get:', item)
        url = item.get('url')
        w = Webdriver()
        w.execute(url=url)


def execute(url: str) -> bool:
    options = webdriver.ChromeOptions()
    options.add_argument('lang=zh_CN.UTF-8')
    options.add_argument('--disable-web-security')
    options.add_argument('--allow-running-insecure-content')
    # 加载插件
    # options.add_extension(
    #     '/mnt/d/wevsm/project/AwesomeBot/volumes/chrome/data/canvas-fingerprint-defend.crx')

    driver = webdriver.Remote(
        command_executor='http://localhost:4444/wd/hub',
        options=options
    )

    driver.get(url)
    # driver.execute_script('window.localStorage.clear();')
    # driver.delete_all_cookies()
    # 显式等待 10s
    try:
        # timeout：最长超时等待时间
        # poll_frequency：检测的时间间隔，默认为500ms
        # ignore_exception：超时后抛出的异常信息，默认情况下抛 NoSuchElementException 异常
        wrap_elements: WebElement = WebDriverWait(driver, timeout=10, poll_frequency=0.5,  ignored_exceptions=None).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/i')))
        text: str = wrap_elements.get_attribute("innerHTML")
        print('text', text)
    finally:
        print('finally')
        # driver.close()
        return False

    # time.sleep(1)
    # wrap_elements: WebElement = driver.find_element_by_xpath(
    #     '/html/body/div[2]/div/div/i')
    # text: str = wrap_elements.get_attribute("innerHTML")
    # print('text', text)
    # if text == NEW_STR:
    #     driver.close()
    #     return True
    # elif text == OLD_STR:
    #     driver.close()
    #     return False
    # else:
    #     driver.close()
    #     return False


# 执行打卡逻辑
async def execute_once(url: str) -> bool:
    print('execute_once')
    return execute(url=url)


def main():

    t1 = threading.Thread(target=put, args=(Q, 'https://www.baidu.com'))
    t2 = threading.Thread(target=get, args=(Q,))
    t3 = threading.Thread(target=get, args=(Q,))
    t1.start()
    t2.start()
    t3.start()
    pass


if __name__ == '__main__':
    # url = 'https://learnywhere.cn/bb/activity/article/2020/0619/news?key=7809deb478bf4001be00bdd3839529d4&feat=u52037115&share_platform=qq&show_user_info=1'
    # url = "https://learnywhere.cn/api/activity/article/report?key=7809deb478bf4001be00bdd3839529d4&uaToken=9ca17ae2e6ffcda170e2e6ee96e57af48a9986f680f5b08aa6c85e969e9faff5648e99ffd9cf7f8895a2d3e12af0feaec3b92a96ed8584e43dabeeb68ecd5e968e9ba2c45b8feaa984d768b1b3b6a3c47eed90ee9e"
    # res: bool = execute(url=url)
    # print(res)
    main()

    pass
