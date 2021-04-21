import asyncio
import queue
import threading
from pathlib import Path
from time import localtime, strftime

import nonebot
from nonebot import (get_driver, on_command, on_message, on_notice,
                     on_startswith)
from nonebot.adapters.cqhttp import (Bot, Event, Message, MessageEvent,
                                     MessageSegment)
from nonebot.log import default_format, logger
from nonebot.matcher import Matcher
from nonebot.rule import to_me
from nonebot.typing import T_State

from .config import Config
from .data_source import Webdriver, execute_once

global_config = get_driver().config
status_config = Config(**global_config.dict())
Q: queue.Queue = queue.Queue()


# logger.add("debug.log",
#            rotation="00:00",
#            diagnose=False,
#            level="DEBUG",
#            format=default_format)

# Export something for other plugin
# export = nonebot.export()
# export.foo = "bar"

# @export.xxx
# def some_function():
#     pass


# 注册一个消息事件响应器，@机器人并且当消息的**https://learnywhere.cn**以指定内容开头时响应。
matcher: Matcher = on_command('打卡', rule=to_me(), priority=10)


def handlePutEventQueue(queue: queue.Queue, bot: Bot, event: MessageEvent, state: T_State) -> int:
    queue.put({
        'bot': bot,
        'event': event,
        'state': state
    })
    return queue.qsize()


def handleGetEventQueue(queue: queue.Queue):
    while True:
        item: dict = queue.get()
        bot: Bot = item.get('bot')
        event: MessageEvent = item.get('event')
        state: T_State = item.get('state')
        url: str = state['url']
        w = Webdriver()
        res: bool = w.execute(url=url)
        if res:
            qsize = queue.qsize()
            message = MessageSegment.reply(
                event.message_id)+"成功,浏览干货文章\n 待处理任务: {}个 \n{}".format(qsize, strftime("%Y年%m月%d日 %H:%M:%S", localtime()))
        else:
            qsize = queue.qsize()
            message = MessageSegment.reply(
                event.message_id)+"失败\n 待处理任务: {}个 \n{}".format(qsize, strftime("%Y年%m月%d日 %H:%M:%S", localtime()))

        async def send():
            await bot.send(event, message, at_sender=True)
        asyncio.run(send())


def threadingStart():
    t = threading.Thread(target=handleGetEventQueue, args=(Q,))
    t.start()


threadingStart()


@matcher.handle()
async def _(bot: Bot, event: Event, state: T_State):
    _args: list = str(event.get_message()).strip().split(' ')
    args: list = list(filter(None, _args))
    if args and len(args) == 2:
        state['count'] = args[0]
        state['url'] = args[1]
    else:
        state['url'] = args[0]


@matcher.got('url', prompt="没有输入打卡链接！")
async def server_clock_learnywhere1(bot: Bot, event: MessageEvent, state: T_State):
    if 'count' in state.keys():
        count: str = state['count']
        try:
            num: int = int(count)
        except Ellipsis as e:
            message = MessageSegment.reply(
                event.message_id)+"错误,参数格式不正确！\n e:{}".format(e)
            await matcher.finish(message=message, at_sender=True)
        else:
            if num > 5:
                qsize = Q.qsize()
                message = MessageSegment.reply(
                    event.message_id)+"错误,一次最多5次！count:{}\n 待处理任务: {}个\n{}".format(count, qsize, strftime("%Y年%m月%d日 %H:%M:%S", localtime()))
                await matcher.send(message=message, at_sender=True)
            else:
                url: str = state['url']
                if url.startswith('https://learnywhere.cn'):
                    for i in range(num):
                        qsize = handlePutEventQueue(
                            queue=Q, bot=bot, event=event, state=state)
                    qsize = Q.qsize()
                    message = MessageSegment.reply(
                        event.message_id)+"收到请求处理中。。。\n 待处理任务: {}个\n{}".format(qsize, strftime("%Y年%m月%d日 %H:%M:%S", localtime()))
                    await matcher.send(message=message, at_sender=True)
                else:
                    message = MessageSegment.reply(
                        event.message_id)+"错误,打卡链接不正确！count:{}\n {}".format(count, strftime("%Y年%m月%d日 %H:%M:%S", localtime()))
                    await matcher.send(message=message, at_sender=True)
        finally:
            pass
    else:
        url: str = state['url']
        if url.startswith('https://learnywhere.cn'):
            qsize = handlePutEventQueue(
                queue=Q, bot=bot, event=event, state=state)
            message = MessageSegment.reply(
                event.message_id)+"收到请求处理中。。。\n 待处理任务: {}个\n{}".format(qsize, strftime("%Y年%m月%d日 %H:%M:%S", localtime()))
            await matcher.send(message=message, at_sender=True)
        else:
            message = MessageSegment.reply(event.message_id)+"错误,打卡链接不正确！"
            await matcher.send(message=message, at_sender=True)


_sub_plugins = set()
_sub_plugins |= nonebot.load_plugins(
    str((Path(__file__).parent / "plugins").
        resolve()))
