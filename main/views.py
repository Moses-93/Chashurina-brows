from django.shortcuts import render
from .forms import NotesForm
from .utils import get_available_slots
from django.http import JsonResponse

def main(request):
    return render(request, 'main/index.html')

def make_appointment(request):
    if request.method == 'POST':
        form = NotesForm(request.POST)
        if form.is_valid():
            form.save()
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
    






