from django import forms
from django.db.utils import ProgrammingError
from django.utils import timezone

from .models import Errors, FreeDate, Notes, Service
from .utils import get_available_slots


def select_service():
    """
    Ця функція отримує всі послуги з таблиці 'Послуги'.

    Параметри:
    Немає

    Повертає:
    QuerySet, що містить всі об'єкти послуг.
    """
    return Service.objects.all()


def select_date():
    """
    Ця функція отримує всі доступні дати з таблиці 'FreeDate'.

    Параметри:
    Немає

    Повертає:
    Список кортежів, де кожен кортеж містить дату і її рядкове представлення.
    Якщо виникає помилка ProgrammingError під час отримання даних, повертається список з одним кортежем, що містить порожній рядок і "-------".
    """
    now = timezone.now()
    try:
        free_date = FreeDate.objects.filter(free=True, now__gt=now)
        return [(date.date, date.date) for date in free_date]
    except ProgrammingError:
        return [("", "-------")]


class NotesForm(forms.ModelForm):
    name = forms.CharField(label="Ім'я:", max_length=150, required=True)
    phone = forms.CharField(
        label="Телефон:",
        max_length=13,
        min_length=13,
        required=True,
        widget=forms.TextInput(
            attrs={"placeholder": "+380", "pattern": r"^\+380[0-9]{9}$"}
        ),
    )
    service = forms.ModelChoiceField(
        label="Оберіть послугу зі списку:", queryset=select_service(), required=True
    )
    date = forms.ChoiceField(
        label="Оберіть вільну дату:",
        choices=[("", "-------")] + select_date(),
        required=True,
    )
    time = forms.ChoiceField(label="Оберіть вільний час:")

    class Meta:
        model = Notes
        fields = ["name", "phone", "service", "date", "time"]

    def __init__(self, *args, **kwargs):
        """
        Ініціалізує екземпляр NotesForm з динамічними виборами для поля 'time' на основі обраного 'date'.

        Параметри:
        *args: Невизначена кількість позиційних аргументів. Передається батьківському конструктору класу.
        **kwargs: Аргументи з ключами. Передаються батьківському конструктору класу.

        Повертає:
        Нічого. Функція змінює вибори поля 'time' у формі екземпляра.
        """
        super(NotesForm, self).__init__(*args, **kwargs)
        if "date" in self.data:
            try:
                selected_date = self.data.get("date")
                # Використовується утилітарна функція для отримання доступних слотів
                available_slots = get_available_slots(selected_date)
                self.fields["time"].choices = [(slot, slot) for slot in available_slots]
            except (ValueError, TypeError):
                self.fields["time"].choices = []


class ErrorsForm(forms.ModelForm):
    name = forms.CharField(label="Ваше ім'я:", max_length=50, required=True)
    phone = forms.CharField(label="Номер телефону:", max_length=15, required=True)
    description = forms.CharField(
        label="Опишіть проблему", widget=forms.Textarea, required=True
    )

    class Meta:
        model = Errors
        fields = ["name", "phone", "description"]
