from django.db import models

from users.models import User


NULLABLE = {'null': True, 'blank': True}


# Create your models here.
class Habit(models.Model):
    PERIODICITY_CHOICE = (
        (1, 'раз в день'),
        (2, 'раз в 2 дня'),
        (3, 'раз в 3 дня'),
        (4, 'раз в 4 дня'),
        (5, 'раз в 5 дней'),
        (6, 'раз в 6 дней'),
        (7, 'раз в неделю'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь', **NULLABLE)
    place = models.CharField(max_length=300, verbose_name='место')
    time = models.TimeField(verbose_name='время')
    action = models.CharField(max_length=300, verbose_name='действие')
    is_nice_habit = models.BooleanField(default=False, verbose_name='признак приятной привычки')
    related_habit = models.ForeignKey('self', on_delete=models.CASCADE, verbose_name='связанная привычка', **NULLABLE)
    periodicity = models.IntegerField(choices=PERIODICITY_CHOICE, default=1, verbose_name='периодичность')
    award = models.CharField(max_length=300, verbose_name='вознаграждение', **NULLABLE)
    time_to_complete = models.TimeField(verbose_name='время на выполнение')
    is_public = models.BooleanField(default=False, verbose_name='признак публичности')

    def __str__(self):
        return f'Я буду {self.action} в {self.time} в {self.place}'

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'


class Log(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, verbose_name='привычка')
    last_send_time = models.DateTimeField(verbose_name='последняя отправка')

    def __str__(self):
        return f'Привычка "{self.habit}" - отправлена {self.last_send_time}'

    class Meta:
        verbose_name = 'Log'
        verbose_name_plural = 'Logs'
