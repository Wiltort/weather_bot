import asyncio
from aiohttp import web
from settings import bot, dp
from handlers.commands import router


async def health_check(request):
    return web.Response(text="OK")

async def main():

    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

async def start_health_check_server():
    app = web.Application()
    app.router.add_get('/health', health_check)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8080)
    await site.start()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(start_health_check_server())
    loop.run_until_complete(main())
