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


def gen_free_slots_today(date: datetime, now: datetime) -> list[str]:
    """
    Генерує список доступних часових слотів для бронювання послуг на поточний день.

    Ця функція фільтрує список доступних часових слотів, згенерованих функцією `generate_slots`,
    щоб включати лише ті слоти, які знаходяться у майбутньому відносно наданого об'єкта `now` datetime.

    Параметри:
    date (datetime): Дата, для якої потрібно згенерувати доступні часові слоти.
        Це повинен бути об'єкт datetime, який представляє дату, з часом встановлено на 00:00.
    now (datetime): Поточний об'єкт datetime.
        Це повинен бути об'єкт datetime, який представляє поточний час.

    Повертає:
    list[str]: Список доступних часових слотів для бронювання послуг на поточний день.
        Кожен часовий слот представлений як рядок у форматі "ГГ:ХХ".
    """
    available_slots = generate_slots()
    available_slots = [
        slot
        for slot in available_slots
        if datetime.combine(date, datetime.strptime(slot, "%H:%M").time()) > now
    ]
    return available_slots


def get_blocked_time(date: str) -> tuple:
    """
    Отримати заброньовані часові слоти для певної дати з бази даних.

    Параметри:
    date (str): Дата, для якої потрібно отримати заброньовані часові слоти у форматі "РРРР-ММ-ДД".

    Повертає:
    tuple: Кортеж, що містить заброньовані часові слоти. Кожен часовий слот представлений як рядок у форматі "ГГ:ХХ".
    """
    booked_slots = Notes.objects.filter(date=date).values_list("time", flat=True)
    return booked_slots


def get_service_duration(service_id: int) -> timedelta:
    """
    Отримати тривалість послуги з бази даних за ідентифікатором послуги.

    Параметри:
    service_id (int): Унікальний ідентифікатор послуги, для якої потрібно отримати тривалість.

    Повертає:
    timedelta: Тривалість послуги у форматі timedelta.
    """
    duration = Service.objects.get(id=service_id).durations
    return duration


def get_available_slots(date_str: str, service_id=None) -> list:
    """
    Отримати доступні часові слоти для певної дати, враховуючи тривалість послуги.

    Параметри:
    date_str (str): Дата, для якої потрібно знайти доступні слоти у форматі "РРРР-ММ-ДД".
    service_id (int, опціонально): Ідентифікатор послуги, для якої потрібно знайти доступні слоти.
        Якщо не вказано, функція не буде враховувати тривалість послуги.

    Повертає:
    list: Список доступних часових слотів у форматі "ГГ:ХХ".
        Якщо доступних слотів немає, повертається список з одним повідомленням: "Вільних місць немає. Оберіть іншу дату".
    """
    # Перетворюємо строку на об'єкт datetime для порівняння
    date = datetime.strptime(date_str, "%Y-%m-%d").date()
    now = datetime.now() + timedelta(hours=1)

    # Отримуємо всі заброньовані слоти для цієї дати
    available_slots = generate_slots()

    # Якщо користувач обрав поточну дату, фільтруємо час, який вже пройшов
    if date == now.date():
        available_slots = gen_free_slots_today(date, now)
    booked_slots = get_blocked_time(date_str)
    if service_id:
        service_duration = get_service_duration(service_id)
        # Видаляємо часові слоти, які перетинаються з уже заброньованими
        for booked_time in booked_slots:
            booked_datetime = datetime.strptime(booked_time, "%H:%M")
            booked_end_time = booked_datetime + service_duration
            booked_start_time = booked_datetime - service_duration

            # Видаляємо всі слоти, які потрапляють в проміжок занятого часу
            available_slots = [
                slot
                for slot in available_slots
                if not (
                    booked_start_time
                    <= datetime.strptime(slot, "%H:%M")
                    < booked_end_time
                )
            ]

    if available_slots:
        return available_slots
    else:
        return ["Вільних місць немає. Оберіть іншу дату"]
