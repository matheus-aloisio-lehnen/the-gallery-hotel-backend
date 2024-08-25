from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.models import Room, Reservation


@api_view(['GET'])
def get_all(request):

    today = timezone.now().date()

    # Contar quartos vagos
    freeRooms = Room.objects.filter(status='vago').count()

    # Contar saídas (reservas que terminaram antes de hoje)
    outs = Reservation.objects.filter(
        endDate__lt=today,
        room__status='ocupado'
    ).count()

    # Contar entradas (reservas que começam hoje ou antes e terminam hoje ou depois)
    ins = Reservation.objects.filter(startDate__lte=today, endDate__gte=today).count()

    summaryCard = {
        'freeRooms': freeRooms,
        'outs': outs,
        'ins': ins,
    }

    rooms = Room.objects.all()
    roomList = []
    for room in rooms:
        # Obter a reserva atual do quarto, se existir
        reservation = Reservation.objects.filter(room=room, startDate__lte=today, endDate__gte=today).first()
        roomList.append({
            'id': room.id,
            'price': room.price,
            'status': room.status,
            'reservation': {
                'id': reservation.id if reservation and reservation.user else None,
                'user': reservation.user.personalData.name if reservation and reservation.user else None,
                'startDate': reservation.startDate if reservation else None,
                'endDate': reservation.endDate if reservation else None,
            } if reservation else None,
        })

    # Construir a resposta
    contract = {
        'summaryCard': summaryCard,
        'roomList': roomList,
    }

    response = {
        'data': contract
    }

    return Response(response)
