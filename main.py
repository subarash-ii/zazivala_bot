import asyncio

asyncio.set_event_loop(asyncio.new_event_loop())

from aiogram import Bot, Dispatcher

from globals import TOKEN
from member_fetcher import pyrogram_app
from handlers.call import register_call_handler

bot = Bot(token=TOKEN)
dp = Dispatcher()

register_call_handler(dp)


async def main():
    print("Bot is running")

    await pyrogram_app.start()

    try:
        await dp.start_polling(bot)
    finally:
        await pyrogram_app.stop()


if __name__ == "__main__":
    asyncio.run(main())