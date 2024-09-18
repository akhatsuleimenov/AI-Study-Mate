from aiogram import types
from config.logger_config import logger


async def check_user_restrictions(db_manager, user_id, message):
    if not db_manager.is_user_authorized(user_id):
        await message.reply(
            "You are not authorized, purchase access from @akhatsuleimenov to use the bot."
        )
        return True
    if db_manager.is_rate_limited(user_id):
        await message.answer(
            "You have reached your request limit for today. Please try again tomorrow."
        )
        return True
    return False


def setup_handlers(dp, db_manager, assistant_manager, admins):
    @dp.message_handler(commands=["start", "help"])
    async def send_welcome(message: types.Message):
        user_id = message.from_user.id
        logger.info(f"Received start or help command from user {user_id}")
        if user_id not in admins and await check_user_restrictions(
            db_manager, user_id, message
        ):
            return
        try:
            db_manager.get_or_create_thread(user_id)
            await message.reply(
                "Hi! I'm an OnStudy English Tutor Bot. Ask me how to learn English."
            )
        except Exception as e:
            logger.error(f"An error occurred: {e}")

    @dp.message_handler(commands=["adduser"])
    async def add_user(message: types.Message):
        user_id = message.from_user.id
        logger.info(f"Received adduser command from user {user_id}")
        if user_id not in admins:
            await message.reply("You are not authorized to add users.")
            return

        try:
            user_id_to_add = int(message.get_args())
            if db_manager.add_authorized_user(user_id_to_add):
                await message.reply("User authorized successfully.")
            else:
                await message.reply("User was already authorized.")
        except ValueError:
            await message.reply("Please provide a valid user ID.")

    @dp.message_handler()
    async def echo(message: types.Message):
        user_id = message.from_user.id
        logger.info(f"Received {message.text} from user {user_id}")
        if user_id not in admins and await check_user_restrictions(
            db_manager, user_id, message
        ):
            return
        try:
            thread_id = db_manager.get_or_create_thread(user_id)
            answer = assistant_manager.handle_message(thread_id, message.text)
            await message.answer(answer)
            db_manager.log_request(user_id)
        except Exception as e:
            logger.error(f"An error occurred: {e}")
