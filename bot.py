#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import nonebot

from nonebot.adapters.cqhttp import Bot as CQHTTPBot

# from src.adapters.cqhttp import Bot as CQHTTPBot

# from nonebot import require

# scheduler = require('apscheduler').scheduler
# status = require('status').status

# @scheduler.scheduled_job('cron', hour='*/2', id='xxx', args=[1], kwargs={arg2: 2})
# async def run_every_2_hour(arg1, arg2):
#     pass

# scheduler.add_job(run_every_day_from_program_start, "interval", days=1, id="xxx")

# Custom your logger
# 
# from nonebot.log import logger, default_format
# logger.add("error.log",
#            rotation="00:00",
#            diagnose=False,
#            level="ERROR",
#            format=default_format)

# You can pass some keyword args config to init function
nonebot.init()
app = nonebot.get_asgi()


driver = nonebot.get_driver()
driver.register_adapter("cqhttp", CQHTTPBot)

# nonebot.load_builtin_plugins()
# nonebot.load_from_toml("pyproject.toml")

# Modify some config / config depends on loaded configs
config = driver.config
nonebot.load_all_plugins(set(config.plugins), set(config.plugin_dirs))

if __name__ == "__main__":
    nonebot.logger.warning("Always use `nb run` to start the bot instead of manually running!")
    nonebot.run(app="__mp_main__:app")
