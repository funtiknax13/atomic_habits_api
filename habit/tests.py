from rest_framework import status
from rest_framework.test import APITestCase

from habit.models import Habit
from users.models import User


class HabitTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(
            email='test@test.com'
        )
        self.user.set_password('1234')
        self.user.save()

        self.nice_habit = Habit.objects.create(
            place="Дом",
            time="12:00:00",
            action="выпить протеиновый коктейль",
            is_nice_habit=True,
            periodicity=1,
            time_to_complete="00:02:00",
            is_public=True,
            user=self.user
        )

        self.habit = Habit.objects.create(
            place="Дом",
            time="12:00:00",
            action="Присесть 25 раз",
            is_nice_habit=False,
            periodicity=1,
            time_to_complete="00:02:00",
            is_public=True,
            user=self.user,
            related_habit=self.nice_habit
        )

    def test_create_habit(self):
        """ Тестирование создания привычки """
        data = {
            'place': 'test_place',
            'time': '12:00:00',
            'action': 'test_action',
            'is_nice_habit': False,
            'periodicity': 1,
            'time_to_complete': '00:02:00',
            'is_public': True,
            'user': self.user.pk,
            'related_habit': self.nice_habit.pk
        }

        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            '/habit/create/',
            data=data
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertTrue(
            Habit.objects.all().exists(),
            {'id': 2,
             'title': 'test_place',
             'place': 'test_place',
             'time': '12:00:00',
             'action': 'test_action',
             'is_nice_habit': False,
             'periodicity': 1,
             'time_to_complete': '00:02:00',
             'is_public': True,
             'user': 1,
             'related_habit': 2})

    def test_list_habit(self):
        """Тестирование вывода списка привычек"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(
            '/habit/',
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json().get("results"),
            [{'id': self.nice_habit.pk, 'related_habit_detail': None, 'place': 'Дом', 'time': '12:00:00',
              'action': 'выпить протеиновый коктейль', 'is_nice_habit': True, 'periodicity': 1, 'award': None,
              'time_to_complete': '00:02:00', 'is_public': True, 'user': self.user.pk, 'related_habit': None},
             {'id': self.habit.pk, 'related_habit_detail': {'action': 'выпить протеиновый коктейль', 'place': 'Дом',
                                                'time_to_complete': '00:02:00'},
              'place': 'Дом', 'time': '12:00:00', 'action': 'Присесть 25 раз', 'is_nice_habit': False,
              'periodicity': 1, 'award': None, 'time_to_complete': '00:02:00', 'is_public': True, 'user': self.user.pk,
              'related_habit': self.nice_habit.pk}]
        )

    def test_habit_retrieve(self) -> None:
        self.client.force_authenticate(user=self.user)

        response = self.client.get(f'/habit/{self.habit.pk}/')

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        response = response.json()

        self.assertEqual(response.get('action'), 'Присесть 25 раз')
        self.assertEqual(response.get('time'), '12:00:00')
        self.assertEqual(response.get('periodicity'), 1)
        self.assertEqual(response.get('related_habit'), self.nice_habit.pk)
        self.assertEqual(response.get('time_to_complete'), '00:02:00')
        self.assertEqual(response.get('user'), self.user.pk)

    def test_habit_update(self):
        self.client.force_authenticate(user=self.user)

        data = {
            'place': 'Update_test_place',
            'time': '12:00:00',
            'action': 'Update_test_action',
            'is_nice_habit': False,
            'periodicity': 1,
            'time_to_complete': '00:02:00',
            'is_public': True,
            'user': self.user.pk,
            'related_habit': self.nice_habit.pk
        }

        response = self.client.put(
            path=f'/habit/{self.habit.pk}/update/', data=data,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        response = response.json()

        self.assertEqual(response.get('action'), 'Update_test_action')
        self.assertEqual(response.get('time'), '12:00:00')
        self.assertEqual(response.get('periodicity'), 1)
        self.assertEqual(response.get('related_habit'), self.nice_habit.pk)
        self.assertEqual(response.get('time_to_complete'), '00:02:00')
        self.assertEqual(response.get('user'), self.user.pk)
        self.assertEqual(response.get('place'), 'Update_test_place')

    def test_habit_delete(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.delete(
            f'/habit/{self.habit.pk}/delete/',
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        self.client.delete(
            f'/habit/{self.nice_habit.pk}/delete/',
        )
        self.assertFalse(
            Habit.objects.all().exists(),
        )

    def tearDown(self) -> None:
        self.user.delete()
        self.habit.delete()
        self.nice_habit.delete()


class UserTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(
            email='test@test.com'
        )
        self.user.set_password('1234')
        self.user.save()

    def test_create_user(self):
        """ Тестирование создания пользователя """
        data = {
            "password": "1234",
            "email": "test@yandex.ru"
        }

        response = self.client.post(
            '/users/register/',
            data=data
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_201_CREATED
        )

    def tearDown(self) -> None:
        self.user.delete()




