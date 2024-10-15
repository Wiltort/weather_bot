import asyncio
import signal
from aiohttp import web
from settings import bot, dp
from handlers.commands import router

async def health_check(request):
    return web.Response(text="OK")

async def main():
    # Set up your application and routes
    app = web.Application()
    app.router.add_get('/health', health_check)
    
    # Add your bot's router
    app.add_routes(router)

    # Create a runner and site for the web application
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8080)
    await site.start()

    # Handle shutdown signals
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, lambda: asyncio.create_task(shutdown(runner)))

    print("Server started at http://0.0.0.0:8080")
    await asyncio.Event().wait()  # Run forever

async def shutdown(runner):
    print("Shutting down...")
    await runner.cleanup()
    await bot.close()
    await dp.storage.close()

if __name__ == "__main__":
    asyncio.run(main())