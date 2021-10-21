#!/usr/bin/env python
# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the CC0 license.

"""
First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

FIO, AGE, CITY, NUMBER, EMAIL, EDUCATION, ABILITY, EXPERIENCE, LINK, WORK, SALARY, SOURCE = range(12)


def start(update: Update, context: CallbackContext) -> int:
    """Starts the conversation and asks the user about their gender."""

    update.message.reply_text(
        'Здравствуйте! '
        '\n'
        'Как Вас зовут?',
    )

    return FIO


def fio(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("ФИО of %s: %s", user.first_name, update.message.text)
    update.message.reply_text(
        'Ваш возраст? ',
    )

    return AGE


def age(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    global points
    if (int(update.message.text) <= 40):
        points = 1
    else:
        points = 0
    logger.info("Возраст of %s: %s", user.first_name, update.message.text)
    update.message.reply_text(
        'Ваше место жительства?',
    )

    return CITY


def city(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("Место жительства of %s: %s", user.first_name, update.message.text)
    update.message.reply_text(
        'Ваша номер телефона?'
    )

    return NUMBER


def number(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("Номер телефона of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('Ваш email?')

    return EMAIL


def email(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("E-mail of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('Есть ли у вас образование в сфере дизайна?')

    return EDUCATION


def education(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    global points
    if (update.message.text == 'Да'):
        points = points + 1
    logger.info("Education of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('Умеете ли вы работать в Adobe Illustrator и Photoshop?')

    return ABILITY


def ability(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    global points
    if (update.message.text == 'Да'):
        points = points + 1
    logger.info("Способности of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('Ваш стаж работы графическим дизайнером (число лет)?')

    return EXPERIENCE


def experience(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    global points
    if (int(update.message.text) >= 1):
        points = points + 1
    logger.info("Стаж работы дизайнером of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('Пришлите, пожалуйста, ссылку на портфолио')

    return LINK


def link(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("Ссылка на портфолио of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('Готовы ли вы к работе на полную занятость в нашей компании, 5-8ч/день')

    return WORK


def work(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    global points
    if (update.message.text == 'Да'):
        points = points + 1
    logger.info("Занятость of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('На какой уровень дохода вы рассчитываете?')

    return SALARY


def salary(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    global points
    if (int(update.message.text) <= 70000):
        points = points + 1
    logger.info("Зарплата of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('Из какого источника вы узнали о вакансии?')

    return SOURCE


def source(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("Источник of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('Спасибо! Обрабатываем ответы.')
    global points
    if (points > 5):
        update.message.reply_text('Поздравляем! Вы приглашены на работу.')
    else:
        update.message.reply_text('К сожалению, Вы нам не подходите. Желаем удачи в поисках работы!')

    return ConversationHandler.END


def cancel(update: Update, context: CallbackContext) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        'Bye! I hope we can talk again some day.',
    )

    return ConversationHandler.END


def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("2077046165:AAGbMY6P-Km-gK8sSgPZExx6ng5051XmRa4")
    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            FIO: [MessageHandler(Filters.regex('\w+\s\w+(\s\w+)?') & ~Filters.command, fio)],
            AGE: [MessageHandler(Filters.regex('\d+') & ~Filters.command, age)],
            CITY: [MessageHandler(Filters.text & ~Filters.command, city)],
            NUMBER: [MessageHandler(Filters.regex('^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$'), number)],
            EMAIL: [MessageHandler(Filters.regex('.+@.+\..+'), email)],
            EDUCATION: [MessageHandler(Filters.regex('^(Да|Нет)$'), education)],
            ABILITY: [MessageHandler(Filters.regex('^(Да|Нет)$'), ability)],
            EXPERIENCE: [MessageHandler(Filters.regex('\d+'), experience)],
            LINK: [MessageHandler(Filters.text, link)],
            WORK: [MessageHandler(Filters.regex('^(Да|Нет)$'), work)],
            SALARY: [MessageHandler(Filters.regex('\d+'), salary)],
            SOURCE: [MessageHandler(Filters.text, source)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
