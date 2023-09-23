from rest_framework.exceptions import ValidationError

from habit.models import Habit


class HabitValidator:

    def __call__(self, value):
        tmp_related_habit = dict(value).get('related_habit')
        tmp_award = dict(value).get('award')
        tmp_is_nice_habit = dict(value).get('is_nice_habit')
        tmp_ctime = dict(value).get('time_to_complete')

        if tmp_is_nice_habit and tmp_award:
            raise ValidationError('У приятной привычки не может быть вознаграждения!')

        if tmp_is_nice_habit and tmp_related_habit:
            raise ValidationError('У приятной привычки не может быть связанной привычки!')

        if tmp_related_habit and tmp_award:
            raise ValidationError('Нельзя одновременно выбрать связанную привычку и вознаграждение!')

        print(tmp_related_habit)

        if tmp_related_habit:
            if not tmp_related_habit.is_nice_habit:
                raise ValidationError(f'В связанные привычки можно добавить только приятную привычку.'
                                f' "{tmp_related_habit}" не является приятной привычкой!')

        check_time = tmp_ctime.hour * 3600 + tmp_ctime.minute * 60 + tmp_ctime.second
        if check_time > 120:
            raise ValidationError('Время на выполнение привычки не должно превышать 2 минуты!')
