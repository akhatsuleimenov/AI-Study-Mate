from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from config.logger_config import logger


async def check_user_restrictions(db_manager, username, message, admins):
    if username in admins:
        return True
    if not db_manager.is_user_authorized(username):
        await message.reply(
            "You are not authorized, purchase access from @nurkkyz to use the bot."
        )
        return False
    if db_manager.is_rate_limited(username):
        await message.reply(
            "You have reached the hourly limit of 100 requests. Please try again later."
        )
        return False
    return True


def setup_router(assistant_manager, db_manager, admins):
    router = Router()

    @router.message(CommandStart())
    async def send_welcome(message: Message):
        username = message.from_user.username
        logger.info(f"Received start or help command from user {username}")
        if await check_user_restrictions(db_manager, username, message, admins):
            await message.reply(
                "Hi! I'm an OnStudy English Tutor Bot. Ask me how to learn English."
            )

    async def handle_user_command(message: Message, command_handler):
        username = message.from_user.username
        if username not in admins:
            await message.reply("You do not have permission to use this command.")
            return

        args = message.text.split()
        if len(args) < 2:
            await message.reply("Please provide a username.")
            return

        try:
            await command_handler(message, db_manager, args[1])
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            await message.reply("An error occurred while processing your request.")

    async def add_user_handler(message, db_manager, username_to_add):
        if db_manager.add_authorized_user(username_to_add):
            await message.reply("User authorized successfully.")
        else:
            await message.reply("User was already authorized.")

    async def delete_user_handler(message, db_manager, username_to_delete):
        if db_manager.delete_authorized_user(username_to_delete):
            await message.reply("User deleted successfully.")
        else:
            await message.reply("User wasn't authorized.")

    @router.message(Command(commands=["adduser"]))
    async def add_user(message: Message):
        logger.info(
            f"Received adduser command from user {message.from_user.username} with args {message.text}"
        )
        await handle_user_command(message, add_user_handler)

    @router.message(Command(commands=["deleteuser"]))
    async def delete_user(message: Message):
        logger.info(
            f"Received deleteuser command from user {message.from_user.username} with args {message.text}"
        )
        await handle_user_command(message, delete_user_handler)

    @router.message()
    async def echo(message: Message):
        username = message.from_user.username
        logger.info(f"Received {message.text} from user {username}")
        if await check_user_restrictions(db_manager, username, message, admins):
            try:
                thread_id = db_manager.get_thread(username)
                if thread_id is None:
                    thread_id = assistant_manager.create_thread().id
                    db_manager.save_thread(username, thread_id)
                answer = assistant_manager.handle_message(thread_id, message.text)
                await message.answer(answer)
                db_manager.log_request(username)
            except Exception as e:
                logger.error(f"An error occurred: {e}")

    return router
