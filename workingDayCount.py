from datetime import datetime, timedelta
from workalendar.asia import SouthKorea
import requests as requests
import json
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters)
import logging

url = "blurblur"
token = "blurblur"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def get_chat_id(update):
    chat_id = update['message']["chat"]["id"]
    return chat_id

def get_message_text(update):
    message_text = update["message"]["text"]
    return message_text

def send_message(chat_id, message_text):
    params = {"chat_id": chat_id, "text": message_text}
    response = requests.post(url + "sendMessage", data=params)
    return response

def cal_working_day(start_date, end_date):
    cal = SouthKorea()
    return cal.get_working_days_delta(start_date - timedelta(1), end_date)

def check(bot, update, args):
    start_date = datetime.strptime(args[0], '%Y-%m-%d')
    end_date = datetime.strptime(args[1], '%Y-%m-%d')

    while (end_date - start_date).days > 0:
        if start_date + timedelta(30) > end_date:
            month_date = end_date
        else:
            month_date = start_date + timedelta(30)
        working_day = cal_working_day(start_date, month_date)
        text = f'{start_date.date()} ~ {month_date.date()} : {working_day}개'
        send_message(get_chat_id(update), text)
        start_date = month_date

def unknown(bot, update):
    bot.send_message(get_chat_id(update), text='/check 2020-01-01 2020-01-31 형식으로 입력해주세요')

def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)

def main():
    updater = Updater(token)
    dp = updater.dispatcher
    print("bot start")

    updater.start_polling()
    dp.add_handler(CommandHandler('check', check, pass_args=True))
    dp.add_handler(MessageHandler(Filters.command, unknown))

    dp.add_error_handler(error)

    updater.idle()
    updater.stop()

if __name__ == '__main__':
    main()
