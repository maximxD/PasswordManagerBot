import asyncio
import os

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, Message
from telegram.constants import ParseMode
from telegram.ext import Application, ContextTypes, CommandHandler, MessageHandler, CallbackQueryHandler, Defaults
from telegram.ext.filters import BaseFilter

from bot import bot_messages
from db.db_api import BotDB


class Bot:
    def __init__(self, db: BotDB):
        self.db = db
        self.bot = Application.builder()\
            .token(os.getenv("PASSWORD_MANAGER_BOT_TOKEN"))\
            .defaults(Defaults(parse_mode=ParseMode.MARKDOWN))\
            .build()
        self.bot.add_handler(CommandHandler(bot_messages.START_CMD, self.start))
        self.bot.add_handler(CommandHandler(bot_messages.SET_CMD, self.set_service))
        self.bot.add_handler(CommandHandler(bot_messages.GET_CMD, self.get_service))
        self.bot.add_handler(CommandHandler(bot_messages.DELETE_CMD, self.delete_service))
        self.bot.add_handler(CommandHandler(bot_messages.HELP_CMD, self.help))
        self.bot.add_handler(CallbackQueryHandler(self.button_handler))
        self.bot.add_handler(MessageHandler(BaseFilter(), self.start))
        self._overwrite_service_keyboard = [[
            InlineKeyboardButton(bot_messages.YES_MSG, callback_data=bot_messages.OVERWRITE_SERVICE_ACCEPTED_CB),
            InlineKeyboardButton(bot_messages.NO_MSG, callback_data=bot_messages.OVERWRITE_SERVICE_CANCELED_CB),
        ]]
        self._delete_service_keyboard = [[
            InlineKeyboardButton(bot_messages.YES_MSG, callback_data=bot_messages.DELETE_SERVICE_ACCEPTED_CB),
            InlineKeyboardButton(bot_messages.NO_MSG, callback_data=bot_messages.DELETE_SERVICE_CANCELED_CB),
        ]]
        self.message_visible_duration = 1

    async def delete_service(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        service_data = update.message.text.split()[1:]
        if len(service_data) == 1:
            if self.db.is_service_exists(service_data[0], update.message.from_user.id):
                context.user_data["service_data"] = service_data
                context.user_data["tg_id"] = update.message.from_user.id
                await update.message.reply_text(bot_messages.service_delete_confirm_msg(service_data[0]),
                                                reply_markup=InlineKeyboardMarkup(self._delete_service_keyboard))
            else:
                await update.message.reply_text(bot_messages.service_is_not_exists_msg(service_data[0]))
        else:
            await update.message.reply_text(bot_messages.INCORRECT_DELETE_SERVICE_FORMAT_MSG)

    async def get_service(self, update: Update, _: ContextTypes.DEFAULT_TYPE):
        service_data = update.message.text.split()[1:]
        if len(service_data) == 1:
            login, password = self.db.get_service_login_password(service_data[0], update.message.from_user.id)
            if login and password:
                asyncio.create_task(self.delete_message_from_chat(
                    await update.message.reply_text(bot_messages.service_data_msg(
                        service_data[0], login, password, self.message_visible_duration)
                    ),
                    service_data[0],
                    self.message_visible_duration*60
                ))
            else:
                await update.message.reply_text(bot_messages.service_is_not_exists_msg(service_data[0]))
        else:
            await update.message.reply_text(bot_messages.INCORRECT_GET_SERVICE_FORMAT_MSG)

    async def set_service(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        service_data = update.message.text.split()[1:]
        if len(service_data) == 3:
            if not self.db.is_service_exists(service_data[0], update.message.from_user.id):
                self.db.save_service(service_data, update.message.from_user.id)
                await update.message.reply_text(bot_messages.set_service_success_msg(service_data[0]))
            else:
                context.user_data["service_data"] = service_data
                context.user_data["tg_id"] = update.message.from_user.id
                await update.message.reply_text(bot_messages.service_already_exists_msg(service_data[0]),
                                                reply_markup=InlineKeyboardMarkup(self._overwrite_service_keyboard))
        else:
            await update.message.reply_text(bot_messages.INCORRECT_SET_SERVICE_FORMAT_MSG)

    async def button_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        service_data = context.user_data.get("service_data")
        tg_id = context.user_data.get("tg_id")
        await query.answer()
        if query.data == bot_messages.OVERWRITE_SERVICE_ACCEPTED_CB and service_data and tg_id:
            self.db.overwrite_service(service_data, tg_id)
            await update.callback_query.message.edit_text(bot_messages.set_service_success_msg(service_data[0]))
        elif query.data == bot_messages.OVERWRITE_SERVICE_CANCELED_CB:
            await update.callback_query.message.edit_text(bot_messages.overwrite_service_cancel_msg(service_data[0]))
        elif query.data == bot_messages.DELETE_SERVICE_ACCEPTED_CB and service_data and tg_id:
            self.db.delete_service(service_data[0], tg_id)
            await update.callback_query.message.edit_text(bot_messages.service_deleted_msg(service_data[0]))
        elif query.data == bot_messages.DELETE_SERVICE_CANCELED_CB:
            await update.callback_query.message.edit_text(bot_messages.delete_service_cancel_msg(service_data[0]))

    @staticmethod
    async def delete_message_from_chat(message: Message, service_name: str, delay: int):
        await asyncio.sleep(delay)
        await message.edit_text(bot_messages.there_was_service_data_msg(service_name))

    @staticmethod
    async def start(update: Update, _: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(bot_messages.START_MSG)

    @staticmethod
    async def help(update: Update, _: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(bot_messages.HELP_MSG)
