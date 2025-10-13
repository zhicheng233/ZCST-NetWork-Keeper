import asyncio

from loguru import logger
from telegram.ext import ApplicationBuilder

import config

app = None

def start_bot():
    global app
    if config.TG_Enable:
        logger.info("Telegram Bot启动ing...")
        try:
            app = (ApplicationBuilder()
                   .token(config.TG_TOKEN)
                   .base_url(config.TG_api_url)
                   .build()
                   )
            logger.success("Telegram Bot启动成功")
        except Exception as e:
            logger.error(f"Telegram Bot启动失败:\n{e}")
async def send_Message(log_message):
    global app
    if not config.TG_Enable:
        return 
    try:
        await app.bot.send_message(chat_id=config.TG_chat_id, text=config.TG_Bot_name + "\n" + log_message)
        logger.info("TG消息发送成功")
    except Exception as e:
        logger.error(f"TG消息发送失败:\n{e}")

def send_TG(log_message):
    try:
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        if loop.is_running():
            asyncio.ensure_future(send_Message(log_message))
        else:
            loop.run_until_complete(send_Message(log_message))
    except Exception as e:
        # 记录异常
        logger.error(f"TG消息发送异常: {e}")
