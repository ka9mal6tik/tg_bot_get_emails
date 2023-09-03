#!/usr/bin/env python
from config import *
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
)
from check_email import *
from datetime import datetime

# Stages
START_ROUTES, INFO_LIST = range(2)
# Callback data
BACK, DELETE = range(2)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.from_user.id not in ALLOWED_USERS:
        await update.message.reply_text("У Вас нету доступа к данному боту!")
        return -1

    current_datetime = datetime.now()
    date_and_time = "%02d.%02d.%04d - %02d:%02d:%02d" % (
        current_datetime.day, current_datetime.month, current_datetime.year, current_datetime.hour,
        current_datetime.minute,
        current_datetime.second)
    emails = check_email()
    if len(emails) != 0:
        list_of_email = list(emails.keys())
        list_of_email.reverse()
        keyboard = [[InlineKeyboardButton(emails[key], callback_data=str(key))] for key in list_of_email[:10]] + \
                   [[InlineKeyboardButton("🔄Обновить", callback_data=str(BACK))]]
    else:
        keyboard = [[InlineKeyboardButton("🔄Обновить", callback_data=str(BACK))]]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(f"{date_and_time} Choose from list:", reply_markup=reply_markup)
    return START_ROUTES


async def choose_list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    choosing_list: str = ''
    answer: str
    emails = check_email()
    email_number = update.callback_query.data
    if email_number in list(emails):
        choosing_list = check_email_body(email_number)
    if choosing_list != "":
        answer = choosing_list
    else:
        answer = "Не удалось загрузить письмо"
    query = update.callback_query
    await query.answer()
    keyboard = [[InlineKeyboardButton("⏪Назад", callback_data=str(BACK))],
                [InlineKeyboardButton("❌Удалить", callback_data=str(DELETE))]]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text=answer, reply_markup=reply_markup
    )
    return INFO_LIST


async def delete(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    current_datetime = datetime.now()
    date_and_time = "%02d.%02d.%04d - %02d:%02d:%02d" % (
        current_datetime.day, current_datetime.month, current_datetime.year, current_datetime.hour,
        current_datetime.minute,
        current_datetime.second)
    lists = check_email()
    query = update.callback_query
    email_number = update.callback_query.data
    delete_email_message(email_number)
    emails = check_email()
    if len(emails) != 0:
        list_of_email = list(emails.keys())
        list_of_email.reverse()
        keyboard = [[InlineKeyboardButton(emails[key], callback_data=str(key))] for key in list_of_email[:10]] + \
                   [[InlineKeyboardButton("🔄Обновить", callback_data=str(BACK))]]
    else:
        keyboard = [[InlineKeyboardButton("🔄Обновить", callback_data=str(BACK))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text=f"{date_and_time} Choose from list:", reply_markup=reply_markup
    )
    return START_ROUTES


async def back(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    current_datetime = datetime.now()
    date_and_time = "%02d.%02d.%04d - %02d:%02d:%02d" % (
        current_datetime.day, current_datetime.month, current_datetime.year, current_datetime.hour,
        current_datetime.minute,
        current_datetime.second)
    query = update.callback_query
    emails = check_email()
    if len(emails) != 0:
        list_of_email = list(emails.keys())
        list_of_email.reverse()
        keyboard = [[InlineKeyboardButton(emails[key], callback_data=str(key))] for key in list_of_email[:10]] + \
                   [[InlineKeyboardButton("🔄Обновить", callback_data=str(BACK))]]
    else:
        keyboard = [[InlineKeyboardButton("🔄Обновить", callback_data=str(BACK))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text=f"{date_and_time} Choose from list:", reply_markup=reply_markup
    )
    return START_ROUTES


def main() -> None:
    application = Application.builder().token(TOKEN).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            START_ROUTES: [
                CallbackQueryHandler(choose_list, pattern="^[1-9][0-9]*$"),
                CallbackQueryHandler(back, pattern="^" + str(BACK) + "$")
            ],
            # START_ROUTES, MAP_ROUTES, SETTING_ROUTES, INFO_ROUTES
            INFO_LIST: [CallbackQueryHandler(back, pattern="^" + str(BACK) + "$"),
                        CallbackQueryHandler(delete, pattern="^" + str(DELETE) + "$")],
        },
        fallbacks=[CommandHandler("start", start)],
    )

    application.add_handler(conv_handler)
    application.run_polling()


if __name__ == "__main__":
    main()
