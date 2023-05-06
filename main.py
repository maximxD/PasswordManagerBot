from bot.bot_main import Bot
from db.db_api import BotDB

if __name__ == '__main__':
    db = BotDB()
    bot = Bot(db)
    bot.bot.run_polling()
