
import time
import queue
from time import localtime, strftime
from nonebot import get_driver
from nonebot.adapters.cqhttp import (Bot, Event, Message, MessageEvent,
                                     MessageSegment)
from nonebot.matcher import Matcher
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from nonebot.typing import T_State
from .config import Config

global_config = get_driver().config
status_config = Config(**global_config.dict())


OLD_STR = 'Hi 老朋友欢迎你来学干货~'
NEW_STR = 'Hi 新伙伴欢迎你来学干货~'


# 执行打卡逻辑
async def execute_once(url: str) -> bool:
    print('execute_once')
    options = webdriver.ChromeOptions()
    options.add_argument('lang=zh_CN.UTF-8')
    options.add_argument('--disable-web-security')
    options.add_argument('--allow-running-insecure-content')
    # 加载插件
    options.add_extension(status_config.webdriver_extension_filepath)

    driver = webdriver.Remote(
        command_executor=status_config.webdriver_command_executor,
        options=options
    )

    # 最大等待时间20s
    driver.implicitly_wait(20)
    driver.get(url)
    driver.execute_script('window.localStorage.clear();')
    driver.delete_all_cookies()
    time.sleep(1)
    wrap_elements: WebElement = driver.find_element_by_xpath(
        '/html/body/div[2]/div/div/i')
    text: str = wrap_elements.get_attribute("innerHTML")
    print('text', text)
    if text == NEW_STR:
        driver.close()
        return True
    elif text == OLD_STR:
        driver.close()
        return False
    else:
        driver.close()
        return False


class Webdriver(object):
    WEBDRIVER_COMMAND_EXECUTOR = status_config.webdriver_command_executor
    WEBDRIVER_EXTENSION_FILEPATH = status_config.webdriver_extension_filepath

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
        wrap_elements: WebElement = self.driver.find_element_by_xpath(
            '/html/body/div[2]/div/div/i')
        text: str = wrap_elements.get_attribute("innerHTML")
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
