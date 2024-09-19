from django import forms
from .models import Notes, Service, FreeDate
from datetime import datetime, timedelta


def select_service():
    return Service.objects.all()

def select_date():
    free_date = FreeDate.objects.filter(free=True)
    return [(date.date, date.date) for date in free_date]

def generate_slots():
    start_time = datetime.strptime('09:00', '%H:%M')
    end_time = datetime.strptime('18:00', '%H:%M')
    slot_duration = timedelta(minutes=30)
    
    slots = []
    current_time = start_time
    while current_time < end_time:
        slots.append(current_time.strftime('%H:%M'))  # час у форматі H:M
        current_time += slot_duration

    return slots

    
    return slots
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

        # Ініціалізуємо choices для поля time
        if 'date' in self.data:
            try:
                selected_date = self.data.get('date')
                booked_slots = Notes.objects.filter(date=selected_date).values_list('time', flat=True)
                available_slots = [slot for slot in generate_slots() if slot not in booked_slots]
                self.fields['time'].choices = [(slot, slot) for slot in available_slots]
                
                # Перевіряємо, чи правильні варіанти часу зберігаються
                print("Available slots after form submission:", available_slots)
                
            except (ValueError, TypeError):
                self.fields['time'].choices = []
        else:
            self.fields['time'].choices = [(slot, slot) for slot in generate_slots()]

