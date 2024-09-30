from django.http import JsonResponse
from django.shortcuts import redirect, render

from .forms import ErrorsForm, NotesForm
from .models import Service
from .telegram_sender import send_message
from .utils import get_available_slots


def main(request):
    """
    Функція обробляє відображення головної сторінки з усіма доступними послугами.

    Параметри:
    запит (HttpRequest): Вхідний об'єкт запиту, що містить інформацію про клієнта.

    Повертає:
    HttpResponse: Зренерована головна сторінка з усіма доступними послугами.
    """
    services = Service.objects.all()
    data = {"services": services}
    return render(request, "main/index.html", context=data)


def make_appointment(request):
    """
    Ця функція обробляє процес створення запису. Вона відображає форму запису,
    перевіряє дані форми, зберігає запис, надсилає сповіщення адміністратору,
    та перенаправляє на сторінку успіху.

    Параметри:
    request (HttpRequest): Вхідний об'єкт запиту, що містить інформацію про клієнта.

    Повертає:
    HttpResponse: Зренерована сторінка форми запису, якщо метод запиту не є POST.
    HttpResponse: Зренерована сторінка успіху з деталями запису, якщо метод запиту є POST і форма дійсна.
    """
    if request.method == "POST":
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
            return render(request, "main/success.html", {"form": data})
    else:
        form = NotesForm()
    return render(request, "main/appointment.html", {"form": form})


def get_available_slots_view(request):
    """
    Ця функція обробляє отримання доступних часів запису на основі наданої дати та послуги.
    Вона отримує дату та service_id з GET-параметрів запиту.
    Якщо дата надана, вона викликає функцію get_available_slots для отримання доступних часів для вказаної дати та послуги.
    Потім повертає JsonResponse з доступними часами.
    Якщо дата не надана, повертається порожній JsonResponse.

    Параметри:
    request (HttpRequest): Вхідний об'єкт запиту, що містить інформацію про клієнта.

    Повертає:
    JsonResponse: Об'єкт JsonResponse, що містить доступні часи для вказаної дати та послуги.
    Якщо дата не надана, повертається порожній JsonResponse.
    """
    date = request.GET.get("date")
    service_id = request.GET.get("service_id")
    if date:
        available_slots = get_available_slots(date, service_id)
        return JsonResponse({"slots": available_slots})
    else:
        return JsonResponse({"slots": []})


def report_errors(request):
    """
    Ця функція обробляє звіти про помилки. Вона відображає форму для звітування про помилки,
    перевіряє дані форми, зберігає звіт про помилку, та перенаправляє на головну сторінку.

    Параметри:
    request (HttpRequest): Вхідний об'єкт запиту, що містить інформацію про клієнта.

    Повертає:
    HttpResponse: Зренерована сторінка звіту про помилки, якщо метод запиту не є POST.
    HttpResponseRedirect: Перенаправляє на головну сторінку, якщо метод запиту є POST і форма дійсна.
    """
    if request.method == "POST":
        form = ErrorsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("main")
    else:
        form = ErrorsForm()
    return render(request, "main/report_errors.html", {"form": form})
