from django.test import TestCase
from django.urls import reverse
from .models import Service
from django.test import SimpleTestCase
from django.contrib.auth.models import User


class ViewTests(TestCase):
    def setUp(self):
        # Створюємо тестовий об'єкт сервісу
        self.service = Service.objects.create(name="Brow Tinting", price=15)

    def test_appointment_view_status_code(self):
        # Перевіряємо чи сторінка створення запису повертає 200
        response = self.client.get(reverse("appointment"))
        self.assertEqual(response.status_code, 200)

    def test_appointment_view_template(self):
        # Перевірка, чи використовується правильний шаблон
        response = self.client.get(reverse("appointment"))
        self.assertTemplateUsed(response, "base.html")

    def test_create_appointment(self):
        # Тест створення запису
        data = {
            "name": "Jane Smith",
            "service": self.service.id,
            "date": "2024-10-01 10:00",
        }
        response = self.client.post(reverse("appointment"), data)
        self.assertEqual(
            response.status_code, 200
        )  # Перевірка на редірект після успішного створення
        self.assertEqual(Service.objects.count(), 1)  # Перевірка, що об'єкт створився


class HomePageTests(TestCase):
    def test_homepage_status_code(self):
        response = self.client.get(reverse("main"))
        self.assertEqual(response.status_code, 200)

    def test_homepage_template(self):
        response = self.client.get(reverse("main"))
        self.assertTemplateUsed(response, "base.html")
