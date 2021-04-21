from pydantic import BaseSettings


class Config(BaseSettings):
    # Your Config Here

    webdriver_command_executor: str = 'http://localhost:4444/wd/hub'
    # extension: path to the \*.crx file
    webdriver_extension_filepath: str = '/mnt/d/wevsm/project/AwesomeBot/volumes/chrome/data/canvas-fingerprint-defend.crx'

    class Config:
        extra = "ignore"
