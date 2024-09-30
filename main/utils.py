from datetime import datetime, timedelta

from .models import Notes, Service


def generate_slots():
    """
    Функція генерує список доступних часових слотів для замовлення послуги.
    Часові слоти генеруються з 10:00 до 18:00 з кроком 10 хвилин.

    Повертає:
    list: Список часових слотів у форматі "ГГ:ХХ".

    """
    slots = []

    start_time = datetime.strptime("10:00", "%H:%M")
    end_time = datetime.strptime("18:00", "%H:%M")
    slot_duration = timedelta(minutes=10)
    current_time = start_time
    while current_time < end_time:
        slots.append(current_time.strftime("%H:%M"))  # час у форматі ГГ:ХХ
        current_time += slot_duration

    return slots


def get_available_slots(date, service_id=None):
    """
    Отримати доступні часові слоти для певної дати, враховуючи тривалість послуги.

    Параметри:
    date (str): Дата, для якої потрібно знайти доступні слоти у форматі "РРРР-ММ-ДД".
    service_id (int, опціонально): Ідентифікатор послуги, для якої потрібно знайти доступні слоти.
        Якщо не вказано, функція не буде враховувати тривалість послуги.

    Повертає:
    list: Список доступних часових слотів у форматі "ГГ:ХХ".
        Якщо доступних слотів немає, повертається список з одним повідомленням: "Вільних місць немає. Оберіть іншу дату".
    """
    booked_slots = Notes.objects.filter(date=date).values_list("time", flat=True)
    available_slots = generate_slots()

    if service_id:
        try:
            service_duration = Service.objects.get(id=service_id).durations
        except Service.DoesNotExist:
            service_duration = timedelta(
                hours=1
            )  # Встановлюємо за замовчуванням тривалість 1 година

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
