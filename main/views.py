from django.http import JsonResponse
from django.shortcuts import render
from .forms import NotesForm
from .models import Notes
from datetime import datetime, timedelta

def main(request):
    return render(request, 'main/index.html')

def make_appointment(request):
    if request.method == 'POST':
        form = NotesForm(request.POST)
        print(type(request.POST.get('time')))
        print(request.POST.get('time'))
        print(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'main/success.html')
    else:
        form = NotesForm()
    return render(request, 'main/appointment.html', {'form': form})
    
def make_success(request):
    ...

# Генерація часових слотів


def get_available_slots(request):
    date = request.GET.get('date', None)
    if date:
        booked_slots = Notes.objects.filter(date=date).values_list('time', flat=True)
        available_slots = [slot for slot in generate_slots() if slot not in booked_slots]
        return JsonResponse({'available_slots': available_slots})
    return JsonResponse({'error': 'No date provided'}, status=400)


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



