from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage, StorageKey

class FSM_ST(StatesGroup):
    after_start = State()
    swnd_msg = State()

bot_tocken = '<BOT_TOKEN>'

bot = Bot(token=bot_tocken,
              default=DefaultBotProperties(parse_mode=ParseMode.HTML))
aio_storage =MemoryStorage()

bot_storage_key = StorageKey(bot_id=bot.id, user_id=bot.id, chat_id=bot.id)

dp = Dispatcher(storage=aio_storage)