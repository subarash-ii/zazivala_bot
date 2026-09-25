import asyncio

asyncio.set_event_loop(asyncio.new_event_loop())

from aiogram import Bot, Dispatcher

from config import TOKEN
from member_fetcher import app
from handlers.call import router as call_router

bot = Bot(token=TOKEN)
dp = Dispatcher()


async def on_startup():
    await app.start()
    print("Bot is running")


async def on_shutdown():
    if getattr(app, "is_initialized", False) and app.is_connected:
        try:
            await app.stop(block=False)
        except Exception as e:
            print(f"Error while stopping Pyrogram: {e}")


async def main():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    dp.include_router(call_router)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())