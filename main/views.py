from django.shortcuts import render
from .forms import NotesForm, ErrorsForm
from .models import Service
from .utils import get_available_slots
from django.http import JsonResponse
from .telegram_sender import send_message

def main(request):
    services = Service.objects.all()
    data = {
        'services': services
    }
    return render(request, 'main/index.html', context=data)

def make_appointment(request):
    if request.method == 'POST':
        form = NotesForm(request.POST)
        if form.is_valid():
            form.save()
            data = form.cleaned_data
            message = (
            f"Новий запис:\n"
            f"Ім'я: {data['name']}\n"
            f"Телефон: {data['phone']}\n"
            f"Дата: {data['date']}\n"
            f"Час: {data['time']}\n"
            f"Послуга: {data['service'].name}"
            )
            send_message(1763711362, message)
            return render(request, 'main/success.html')
    else:
        form = NotesForm()
    return render(request, 'main/appointment.html', {'form': form})
    
def make_success(request):
    ...


def get_available_slots_view(request):
    date = request.GET.get('date')
    service_id = request.GET.get('service_id')
    if date:
        available_slots = get_available_slots(date, service_id)
        return JsonResponse({'slots': available_slots})
    else:
        return JsonResponse({'slots': []})
    

def report_errors(request):
    if request.method == 'POST':
        form = ErrorsForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = ErrorsForm()
    return render(request, 'main/report_errors.html', {'form': form})





