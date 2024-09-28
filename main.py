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

if os.path.exists(".env"):
    load_dotenv()

tg_bot_token = os.getenv("TG_BOT_TOKEN")
assistant_token = os.getenv("ASSISTANT_TOKEN")
assistant_id = os.getenv("ASSISTANT_ID")
DATABASE_URL = os.getenv("DATABASE_URL")
ADMIN_USERNAMES = set(
    username for username in os.getenv("ADMIN_USERNAMES", "").split(",")
)

# Initialize managers
assistant_manager = AssistantManager(api_key=assistant_token, assistant_id=assistant_id)
db_manager = DatabaseManager(DATABASE_URL)

# Create and configure the bot
bot = Bot(token=tg_bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(bot)

# Setup router with dependencies
router = setup_router(assistant_manager, db_manager, ADMIN_USERNAMES, tg_bot_token)
dp.include_router(router)


async def main() -> None:
    logger.info("Bot is starting...")
    try:
        await dp.start_polling(bot, timeout=20, relax=0.1)
    except Exception as e:
        logger.error("An error occurred during polling: %s", str(e))


if __name__ == "__main__":
    asyncio.run(main())
