from api.models import Reservation, Room

def check_room_availability(roomId, startDate, endDate):
    try:
        room = Room.objects.get(pk=roomId)
        overlapping_reservations = Reservation.objects.filter(
            room=room,
            startDate__lt=endDate,
            endDate__gt=startDate
        )
        return not overlapping_reservations.exists()
    except Room.DoesNotExist:
        return None