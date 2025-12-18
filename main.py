import asyncio
import os
import json

from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode, ContentType
from aiogram.types import WebAppInfo, KeyboardButton, ReplyKeyboardMarkup


bot = Bot('7246301763:AAFD_8vaxy4cUm3tOJLWrAAgtZ0ZKoqabsM')
dp = Dispatcher()

@dp.message()
async def show_miniapp(message: types.Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(
                text="Открыть MiniApp",
                ##### Заменить ниже:
                web_app=WebAppInfo(url="https://ССЫЛКА-КОТОРУЮ-ВЫ-ПОЛУЧИТЕ-ПОЗЖЕ/")
            )]
        ],
        resize_keyboard=True
    )
    await message.answer("Нажмите кнопку ниже, чтобы открыть Mini App:", reply_markup=keyboard)


@dp.message(F.content_type == ContentType.WEB_APP_DATA)
async def handle_webapp_data(message: types.Message):
    try:
        data = json.loads(message.web_app_data.data)
        name = data.get("name", "Неизвестный пользователь")
        msg = data.get("message", "(пусто)")

        await message.answer(
            f"<b>{name}</b> отправил(а) сообщение:\n\n{msg}",
            parse_mode=ParseMode.HTML
        )

    except Exception as e:
        await message.answer("Произошла ошибка при разборе данных из Mini App")

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())