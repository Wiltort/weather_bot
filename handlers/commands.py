from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from utils.weather import get_coordinates, get_weather

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        f"Привет, {message.from_user.full_name}! Хочешь узнать погоду?"
    )
    await message.answer('Введи команду "/weather [город]".')


@router.message(Command("weather"))
async def weather(message: Message):
    # получение названия города
    try:
        city = message.text.split()[1]
        if not city:
            await message.answer(
                'Не был введен город. Введи команду "/weather [город]".'
            )
    except IndexError:
        await message.answer(
            'Не был введен город. Введи команду "/weather [город]".'
            )
        return None
    # проверка на наличие города в базе
    coordinates = await get_coordinates(city_name=city)
    if not coordinates:
        await message.answer(f"Ошибка: Город {city} в базе не найден")
    await message.answer(f"{city}: загрузка погоды...")
    try:
        weather_data = await get_weather(coordinates=coordinates)
    except Exception:
        await message.answer("Ошибка")
        return None
    await message.answer(
        f"Погода в городе {city}:\n"
        f"Температура: {round(weather_data.Variables(0).Value(), 1)} C;\n"
        f"Относительная влажность: {weather_data.Variables(1).Value()} %;\n"
        f"По ощущениям: {round(weather_data.Variables(2).Value(), 1)} С;\n"
        f"Осадки: {weather_data.Variables(3).Value()} мм;\n"
        f"Скорость ветра: {round(weather_data.Variables(5).Value(), 1)} км/ч."
    )
