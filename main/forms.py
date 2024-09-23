from django import forms

from .models import Errors, FreeDate, Notes, Service
from .utils import generate_slots, get_available_slots


def select_service():
    # Вибираємо всі послуги з таблиці Service
    return Service.objects.all()


def select_date():
    # Вибираємо всі вільні дати з таблиці FreeDate
    free_date = FreeDate.objects.filter(free=True)
    return [(date.date, date.date) for date in free_date]


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
        super(NotesForm, self).__init__(*args, **kwargs)
        if "date" in self.data:
            try:
                selected_date = self.data.get("date")
                # Використовуємо утилітну функцію для отримання доступних слотів
                available_slots = get_available_slots(selected_date)
                self.fields["time"].choices = [(slot, slot) for slot in available_slots]
            except (ValueError, TypeError):
                self.fields["time"].choices = []
        else:
            self.fields["time"].choices = [(slot, slot) for slot in generate_slots()]


class ErrorsForm(forms.ModelForm):
    name = forms.CharField(label="Ваше ім'я:", max_length=50, required=True)
    phone = forms.CharField(label="Номер телефону:", max_length=15, required=True)
    description = forms.CharField(
        label="Опишіть помилку", widget=forms.Textarea, required=True
    )

    class Meta:
        model = Errors
        fields = ["name", "phone", "description"]
