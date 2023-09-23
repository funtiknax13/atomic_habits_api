from django.core.management.base import BaseCommand
from django.conf import settings

from telebot import TeleBot

from users.models import User

bot = TeleBot(settings.TG_API, threaded=False)


class Command(BaseCommand):

    @bot.message_handler(content_types=['text'])
    def get_text_messages(message):
        if message.text == "/start" or message.text == "/help":
            bot.send_message(message.from_user.id,
                             text='Для синхронизации введите свою почту, с которой регистрировались на сайте')
        else:
            if User.objects.filter(email=message.text).exists():
                user = User.objects.get(email=message.text)
                user.telegram = message.chat.id
                user.save()
                bot.send_message(message.from_user.id,
                                 text='Синхронизация прошла успешно!')
            else:
                bot.send_message(message.from_user.id,
                                 text='Нет пользователя с такой почтой!')

    bot.polling(none_stop=True, interval=0)
