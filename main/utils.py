from datetime import datetime, timedelta

from .models import Notes, Service


def generate_slots():
    slots = []

    start_time = datetime.strptime("10:00", "%H:%M")
    end_time = datetime.strptime("18:00", "%H:%M")
    slot_duration = timedelta(minutes=10)
    current_time = start_time
    while current_time < end_time:
        slots.append(current_time.strftime("%H:%M"))  # час у форматі H:M
        current_time += slot_duration

    return slots


def get_available_slots(date, service_id=None):
    """Повертає доступні часові слоти для певної дати з врахуванням тривалості послуги."""
    booked_slots = Notes.objects.filter(date=date).values_list("time", flat=True)
    available_slots = generate_slots()

    if service_id:
        try:
            service_duration = Service.objects.get(id=service_id).durations
        except Service.DoesNotExist:
            service_duration = timedelta(
                hours=1
            )  # Встановлюємо за замовчуванням 1 година

        # Видаляємо часові слоти, які перетинаються з уже заброньованими
        for booked_time in booked_slots:
            booked_datetime = datetime.strptime(booked_time, "%H:%M")
            booked_end_time = booked_datetime + service_duration

            # Видаляємо всі слоти, які потрапляють в проміжок занятого часу
            available_slots = [
                slot
                for slot in available_slots
                if not (
                    booked_datetime
                    <= datetime.strptime(slot, "%H:%M")
                    < booked_end_time
                )
            ]
    if available_slots:
        return available_slots
    else:
        return ["Вільних місць немає. Оберіть іншу дату"]
