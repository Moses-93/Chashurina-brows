from django.http import JsonResponse
from django.shortcuts import render
from .forms import NotesForm, generate_slots
from .models import Notes

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


def get_available_slots(request):
    select_data = request.GET.get('date')
    if select_data:
        slots = generate_slots()
        booked_slots = Notes.objects.filter(date=select_data).values_list('time', flat=True)
        available_slots = [slot for slot in slots if slot not in booked_slots]
        return JsonResponse({'slots': available_slots})
    else:
        return JsonResponse({'slots': []})
    






