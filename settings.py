import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from decouple import config


admins = [int(admin_id) for admin_id in config("ADMINS").split(",")]

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

bot = Bot(
    token=config("TOKEN"),
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher(storage=MemoryStorage())

geoloc_api_key = config("GEOLOC_KEY")
geoloc_api_url = "https://api.opencagedata.com/geocode/v1/json"
meteo_api_url = "https://api.open-meteo.com/v1/forecast"
