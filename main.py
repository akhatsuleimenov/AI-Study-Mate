import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv

from bot.handlers import setup_router
from config.logger_config import logger
from database.db_manager import DatabaseManager
from openai_api.assistant_manager import AssistantManager

load_dotenv()

tg_bot_token = os.getenv("TG_BOT_TOKEN")
assistant_token = os.getenv("ASSISTANT_TOKEN")
assistant_id = os.getenv("ASSISTANT_ID")
db_path = os.getenv("DB_PATH")
ADMIN_USER_IDS = set(int(uid) for uid in os.getenv("ADMIN_USER_IDS", "").split(","))

# Initialize managers
assistant_manager = AssistantManager(api_key=assistant_token, assistant_id=assistant_id)
db_manager = DatabaseManager(db_path=db_path)

# Create and configure the bot
bot = Bot(token=tg_bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# Setup router with dependencies
router = setup_router(assistant_manager, db_manager, ADMIN_USER_IDS)
dp.include_router(router)


async def main() -> None:
    logger.info("Bot is starting...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
