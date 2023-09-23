from django.urls import path

from habit.apps import HabitConfig
from habit.views import HabitCreateAPIView, HabitListAPIView, HabitRetrieveAPIView, HabitUpdateAPIView, \
    HabitDestroyAPIView, HabitPublicListAPIView

app_name = HabitConfig.name

urlpatterns = [
    path('habit/create/', HabitCreateAPIView.as_view(), name='habit-create'),
    path('habit/', HabitListAPIView.as_view(), name='habit-list'),
    path('habit/<int:pk>/', HabitRetrieveAPIView.as_view(), name='habit-detail'),
    path('habit/<int:pk>/update/', HabitUpdateAPIView.as_view(), name='habit-update'),
    path('habit/<int:pk>/delete/', HabitDestroyAPIView.as_view(), name='habit-delete'),
    path('habit/public/', HabitPublicListAPIView.as_view(), name='habit-public'),

]
