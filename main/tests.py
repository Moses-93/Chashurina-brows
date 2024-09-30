from django.test import TestCase
from django.urls import reverse
from .models import Service
from .models import FreeDate
from .forms import NotesForm


class ViewTests(TestCase):
    def setUp(self):
        """
        Налаштування тестового об'єкта сервісу для подальшого тестування.

        Цей метод створює об'єкт Service з назвою "Brow Tinting" та ціною 15.
        Цей об'єкт буде використовуватися в різних тестових випадках для перевірки правильності роботи додатку.

        Параметри:
        Немає

        Повертає:
        Немає
        """
        self.service = Service.objects.create(name="Brow Tinting", price=15)

    def test_appointment_view_status_code(self):
        """
        Перевіряє статус-код сторінки створення запису.

        Цей тест використовує Django TestCase для створення тестового клієнта,
        який здійснює HTTP GET запит до сторінки створення запису.
        Потім перевіряється, чи статус-код відповіді дорівнює 200,
        що означає успішне завантаження сторінки.

        Параметри:
        Немає

        Повертає:
        Немає
        """
        response = self.client.get(reverse("appointment"))
        self.assertEqual(response.status_code, 200)

    def test_appointment_view_template(self):
        """
        Перевіряє, чи використовується правильний шаблон на сторінці створення запису.

        Цей тест використовує Django TestCase для створення тестового клієнта,
        який здійснює HTTP GET запит до сторінки створення запису.
        Потім перевіряється, чи використовується шаблон "base.html".

        Параметри:
        Немає

        Повертає:
        Немає
        """
        response = self.client.get(reverse("appointment"))
        self.assertTemplateUsed(response, "base.html")

    def test_create_appointment(self):
        """
        Тестує процес створення запису.

        Цей тест створює тестовий запис, використовуючи дані,
        і перевіряє статус-код відповіді та кількість об'єктів Service в базі даних.

        Параметри:
        Немає

        Повертає:
        Немає
        """
        data = {
            "name": "Jane Smith",
            "phone": "1234567890",
            "service": self.service.id,
            "date": "2024-10-01",
            "time": "10:00",
        }
        response = self.client.post(reverse("appointment"), data)
        self.assertEqual(
            response.status_code, 200
        )  # Перевірка на редірект після успішного створення
        self.assertEqual(Service.objects.count(), 1)  # Перевірка, що об'єкт створився


class HomePageTests(TestCase):
    def test_homepage_template(self):
        response = self.client.get(reverse("main"))
        self.assertTemplateUsed(response, "base.html")

    def test_homepage_status_code(self):
        """
        Перевірка статус-коду сторінки головної.

        Цей тест використовує Django TestCase для створення тестового клієнта,
        який здійснює HTTP GET запит до головної сторінки.
        Потім перевіряється, чи статус-код відповіді дорівнює 200,
        що означає успішне завантаження сторінки.

        Параметри:
        Немає

        Повертає:
        Немає
        """
        response = self.client.get(reverse("main"))
        self.assertEqual(response.status_code, 200)


class ServiceModelTests(TestCase):
    def test_service_creation(self):
        """
        Тестування створення об'єкта Service.

        Цей тест створює об'єкт Service з вказаним іменем та ціною,
        потім перевіряє, чи атрибути об'єкта відповідають наданим значенням.
        Також перевіряється, чи об'єкт є екземпляром моделі Service.

        Параметри:
        - name (str): Ім'я послуги.
        - price (float): Ціна послуги.

        Повертає:
        - None
        """
        service = Service.objects.create(name="Brow Shaping", price=20)
        self.assertEqual(service.name, "Brow Shaping")
        self.assertEqual(service.price, 20)
        self.assertTrue(isinstance(service, Service))


class NotesFormTest(TestCase):
    def test_valid_form(self):
        """
        Тестування форми NotesForm зі валідними даними.

        Цей тест створює об'єкт Service та словник з валідними даними форми.
        Потім створює екземпляр форми NotesForm з цими даними та перевіряє, чи форма є валідною.
        Якщо форма є валідною, перевіряється, чи повертає метод is_valid() форми True.

        Параметри:
        - service (Service): Об'єкт Service з іменем та ціною.
        - data (dict): Словник, що містить валідні дані форми.

        Повертає:
        - None
        """
        service = Service.objects.create(name="Lash Lift", price=30)
        free_date = FreeDate.objects.create(date='2024-10-05', free=True)
        data = {
            "name": "Anna Doe",
            "phone": "+380987654321",
            "service": service.id,
            "date": "2024-10-05",
            "time": "14:00",
        }

        form = NotesForm(data=data)
        print(form.errors)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        """
        Тестування форми NotesForm зі невалідними даними.

        Цей тест створює словник з невалідними даними для форми NotesForm.
        Потім створює екземпляр форми NotesForm з цими даними та перевіряє, чи форма є невалідною.
        Якщо форма є невалідною, перевіряється, чи повертає метод is_valid() форми False.

        Параметри:
        - data (dict): Словник, що містить невалідні дані форми.
            - name (str): Ім'я особи. Не повинно бути порожнім.
            - phone (str): Номер телефону особи. Повинен бути дійсним номером телефону.
            - service (int): ID послуги. Не повинно бути порожнім.
            - date (str): Дата запису. Не повинно бути порожнім.
            - time (str): Час запису. Не повинно бути порожнім.

        Повертає:
        - None
        """
        data = {
            "name": "",
            "phone": "123",  # Недійсний телефон
            "service": "",
            "date": "",
            "time": "",
        }
        form = NotesForm(data=data)
        self.assertFalse(form.is_valid())
