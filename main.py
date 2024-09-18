import os

from aiogram import Bot, Dispatcher
from aiogram.utils import executor
from dotenv import load_dotenv

from bot.handlers import setup_handlers
from database.db_manager import DatabaseManager
from openai_api.assistant_manager import AssistantManager

load_dotenv()

tg_bot_token = os.getenv("TG_BOT_TOKEN")
assistant_token = os.getenv("ASSISTANT_TOKEN")
assistant_id = os.getenv("ASSISTANT_ID")
db_path = os.getenv("DB_PATH")

ADMIN_USER_IDS = set(int(uid) for uid in os.getenv("ADMIN_USER_IDS", "").split(","))


bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)

assistant_manager = AssistantManager(api_key=assistant_token, assistant_id=assistant_id)
db_manager = DatabaseManager(db_path=db_path)

setup_handlers(dp, db_manager, assistant_manager, ADMIN_USER_IDS)

if __name__ == "__main__":
    executor.start_polling(dp)
