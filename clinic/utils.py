from django.utils.crypto import get_random_string

def gen_tr_no(length=25):
    return str(get_random_string(length=length, allowed_chars='1234567890'))

from datetime import datetime, time, timedelta

def date_range(start, end):
    start, end = datetime.strptime(start, '%Y-%m-%d'), datetime.strptime(end, '%Y-%m-%d')
    delta = end - start
    days = [start + timedelta(days=i) for i in range(delta.days + 1)]
    return days

def combine_dt_time(dt, t_time):
    return datetime.combine(dt,t_time)

def get_free_slots(hours, booked, duration=timedelta(hours=1)):
    available = []
    slots = sorted([(hours[0], hours[0])] + booked + [(hours[1], hours[1])])
    for start, end in ( (slots[i][1], slots[i+1][0]) for i in range(len(slots)-1) ):
        assert start <= end
        while start + duration <= end:
            free_slot = {}
            done = start + duration
            # free_slot["date"] = start.strftime("%Y-%m-%d")
            free_slot["start"] = start.strftime("%H:%M:%S")
            free_slot["end"] = done.strftime("%H:%M:%S")
            available.append(free_slot)
            start = start+duration
    return available

def is_overlapped(range1, range2):
    if max(range1[0], range2[0]) < min(range1[1], range2[1]):
        return True
    else:
        return False
