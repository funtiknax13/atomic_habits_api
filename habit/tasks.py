from datetime import timedelta, datetime

from celery import shared_task
from django.utils import timezone
from telebot import TeleBot
from django.conf import settings

from habit.models import Habit, Log
from users.models import User

bot = TeleBot(settings.TG_API, threaded=False)


@shared_task
def send_daily_message() -> None:
    try:
        users = User.objects.all()
        for user in users:
            if user.telegram:
                habits = Habit.objects.filter(user=user)
                habits_message = ''
                for habit in habits:
                    habits_message += f'- {habit}\n'
                if habits_message != '':
                    bot.send_message(user.telegram, 'Напоминаем о всех привычках, которые вы тренируете:\n'
                                     + habits_message)

    except Exception as ex:
        print(f'Send message error: {ex}')


@shared_task
def send_message() -> None:
    now = datetime.now(timezone.utc)
    try:
        habits = Habit.objects.all()
        for habit in habits:
            last_send = habit.log_set.order_by('-last_send_time').first()
            if last_send:
                send_time = last_send.last_send_time + timedelta(days=habit.periodicity)
                if send_time - now < timedelta(minutes=2):
                    if habit.user.telegram:
                        bot.send_message(habit.user.telegram,
                                         f'Напоминаем о привычке:\n{habit}')
                        log = Log.objects.create(habit=habit, last_send_time=now + timedelta(minutes=2))
                        log.save()

            else:
                if habit.time.hour == now.hour and habit.time.minute == now.minute:
                    if habit.user.telegram:
                        bot.send_message(habit.user.telegram,
                                         f'Напоминаем о привычке:\n{habit}')
                        log = Log.objects.create(habit=habit, last_send_time=now)
                        log.save()
    except Exception as ex:
        print(f'Send message error: {ex}')
