from rest_framework import serializers

from habit.models import Habit
from habit.validators import HabitValidator


class NiceHabitSerializer(serializers.ModelSerializer):

    class Meta:
        model = Habit
        fields = ['action', 'place', 'time_to_complete']


class HabitSerializer(serializers.ModelSerializer):
    related_habit_detail = NiceHabitSerializer(source='related_habit', read_only=True)

    class Meta:
        model = Habit
        fields = '__all__'
        validators = [HabitValidator(), ]


