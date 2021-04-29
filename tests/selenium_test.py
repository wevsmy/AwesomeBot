import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


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
        self.driver.execute_script('window.localStorage.clear();')
        self.driver.delete_all_cookies()
        time.sleep(1)
        text: str = ''
        try:
            wrap_elements: WebElement = self.driver.find_element_by_xpath(
                '/html/body/div[2]/div/div/i')
            text: str = wrap_elements.get_attribute("innerHTML")
        except Exception as e:
            print('err:', e)

        print('text', text)
        if text == NEW_STR:
            self.driver.quit()
            return True
        elif text == OLD_STR:
            self.driver.quit()
            return False
        else:
            self.driver.quit()
            return False


if __name__ == '__main__':
    # url = 'https://learnywhere.cn/bb/activity/article/2020/0619/news?key=7809deb478bf4001be00bdd3839529d4&feat=u52037115&share_platform=qq&show_user_info=1'
    url = "https://learnywhere.cn/api/activity/article/report?key=7809deb478bf4001be00bdd3839529d4&uaToken=9ca17ae2e6ffcda170e2e6ee96e57af48a9986f680f5b08aa6c85e969e9faff5648e99ffd9cf7f8895a2d3e12af0feaec3b92a96ed8584e43dabeeb68ecd5e968e9ba2c45b8feaa984d768b1b3b6a3c47eed90ee9e"
    w = Webdriver()
    res: bool = w.execute(url=url)
    print(res)

    pass
