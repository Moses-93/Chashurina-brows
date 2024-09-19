from django import forms
from .models import Notes, Service, FreeDate
from .utils import get_available_slots, generate_slots

def select_service():
    return Service.objects.all()

def select_date():
    free_date = FreeDate.objects.filter(free=True)
    return [(date.date, date.date) for date in free_date]


class NotesForm(forms.ModelForm):
    name = forms.CharField(max_length=150, required=True)
    phone = forms.CharField(max_length=15, required=True)
    service = forms.ModelChoiceField(queryset=select_service(), required=True)
    date = forms.ChoiceField(choices=[('', '-------')] + select_date(), required=True)
    time = forms.ChoiceField()
    
    class Meta:
        model = Notes
        fields = ['name', 'phone', 'service', 'date', 'time']
    
    def __init__(self, *args, **kwargs):
        super(NotesForm, self).__init__(*args, **kwargs)
        if 'date' in self.data:
            try:
                selected_date = self.data.get('date')
                # Використовуємо утилітну функцію для отримання доступних слотів
                available_slots = get_available_slots(selected_date)
                self.fields['time'].choices = [(slot, slot) for slot in available_slots]
            except (ValueError, TypeError):
                self.fields['time'].choices = []
        else:
            self.fields['time'].choices = [(slot, slot) for slot in generate_slots()]

