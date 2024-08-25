from datetime import datetime

from django.utils import timezone

from api.models import Room, User, Reservation
from api.serializers import ReservationSerializer
from api.services.user_service import create_user, get_user_data


def create_reservation(data):
    email = data.get('email')
    role = data.get('role')
    user = User.objects.filter( email=email, role = role ).first()
    if not user:
        user = create_user(data)

    room = Room.objects.get(id=data.get('roomId'))
    startDate = data.get('startDate')
    endDate = data.get('endDate')

    start_date = datetime.strptime(startDate, '%Y-%m-%d').date()
    end_date = datetime.strptime(endDate, '%Y-%m-%d').date()

    today = timezone.now().date()
    if start_date <= today <= end_date:
        # Atualizar o status do quarto para 'reservado'
        room.status = 'reservado'
        room.save()

    reservation = Reservation.objects.create(
        room = room,
        user = user,
        startDate = startDate,
        endDate = endDate
    )
    serializer = ReservationSerializer(reservation)
    return serializer.data

def get_reservation_data(reservation):
    try:
        return {
            'id': reservation.id,
            'startDate': reservation.startDate,
            'endDate': reservation.endDate,
            'qrCode': reservation.qrCode,
            'qrCodeStatus': reservation.qrCodeStatus,
            'user': get_user_data(reservation.user),
            'checkedOut': reservation.checkedOut,
        }
    except AttributeError:
        return None