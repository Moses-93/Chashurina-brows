from django import forms
from .models import Notes, Service, FreeDate

def select_service():
    return Service.objects.all()

def select_date():
    free_date = FreeDate.objects.filter(free=True)
    return [(date.date, date.date) for date in free_date]


class NotesForm(forms.ModelForm):
    name = forms.CharField(max_length=150, required=True)
    phone = forms.CharField(max_length=15, required=True)
    service = forms.ModelChoiceField(queryset=select_service(), required=True)
    date = forms.ChoiceField(choices=select_date(), required=True)
    time = forms.ChoiceField()
    class Meta:
        model = Notes
        fields = ['name', 'phone', 'service', 'date', 'time']
