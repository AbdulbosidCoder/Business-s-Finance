import asyncio
import logging
import sys
import handlers, middlewares
from loader import dp, bot, db
from utils.set_botcommands import commands
from utils.notify_admins import start, shutdown
from aiogram.types.bot_command_scope_all_private_chats import BotCommandScopeAllPrivateChats


async def main():
    try:
        try:
            db.create_incoming_payment_table()
            db.create_outgoing_payment_table()
            db.create_menu_table()
            db.create_product_table()
            db.create_user_table()
        except Exception as e:
            print(e)
        await  bot.delete_webhook(drop_pending_updates=True)
        await bot.set_my_commands(commands=commands, scope=BotCommandScopeAllPrivateChats(type='all_private_chats'))
        dp.startup.register(start)
        dp.shutdown.register(shutdown)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Bot is shutting down')
