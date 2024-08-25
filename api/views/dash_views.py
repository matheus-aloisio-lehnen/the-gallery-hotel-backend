from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from api.models import Room, Reservation
from api.serializers import ReservationSerializer
from api.services.reservation_service import get_reservation_data
from api.services.qr_code_service import generate_qr_code_base64


@api_view(['GET'])
def get_all(request):
    today = timezone.now().date()
    rooms = Room.objects.all()
    outs = Reservation.objects.filter(room__status='ocupado', endDate__exact=today).count()
    ins = Reservation.objects.filter(startDate__lte=today, endDate__gte=today, room__status='reservado').count()
    freeRooms = rooms.count() - ins - outs
    summaryCard = {
        'freeRooms': freeRooms,
        'outs': outs,
        'ins': ins,
    }
    roomList = []
    for room in rooms:
        reservation = Reservation.objects.filter(
            room=room,
            startDate__lte=today,
            endDate__gte=today,
            checkedOut=False
        ).select_related('user__personalData', 'user__address').first()

        roomList.append({
            'id': room.id,
            'price': room.price,
            'status': room.status,
            'reservation': get_reservation_data(reservation),
        })
    response = {
        'data': {
            'summaryCard': summaryCard,
            'roomList': roomList,
        }
    }
    return Response(response)


@api_view(['PUT'])
def checkout(request, id):
    try:
        today = timezone.now().date()
        room = Room.objects.get(id=id)
        reservation = Reservation.objects.filter(
            room=room,
            startDate__lte=today,
            endDate__gte=today
        ).first()

        has_other_reservation = Reservation.objects.filter(
            room=room,
            startDate__lte=today,
            endDate__gte=today
        ).exclude(id=reservation.id).exists()

        print('other', has_other_reservation)

        if has_other_reservation:
            room.status = 'reservado'
        else:
            room.status = 'vago'
            reservation.checkedOut = True

        room.save()
        reservation.qrCodeStatus = False
        reservation.save()

        response = {
            'data': True,
            'message:': "Checkout concluído com sucesso."
        }

        return Response(response, status=status.HTTP_200_OK)

    except Room.DoesNotExist:
        return Response({"message": "Quarto não encontrado."}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def checkin(request):
    try:
        reservation_id = request.data.get('id')
        reservation = Reservation.objects.get(id=reservation_id)
        room = reservation.room

        if reservation:
            reservation.qrCodeStatus = True
            reservation_info = (
                f"Reserva ID: {reservation.id}\n"
                f"Nome do Hóspede: {reservation.user.personalData.name if reservation.user.personalData else 'Não disponível'}\n"
                f"Data de Check-in: {reservation.startDate}\n"
                f"Data de Check-out: {reservation.endDate}\n"
                f"Preço: {reservation.room.price}\n"
                f"Quarto: {reservation.room.description}\n"
                f"QR Code Status: {'Ativo' if reservation.qrCodeStatus else 'Inativo'}"
            )
            qr_code_base64 = generate_qr_code_base64(reservation_info)
            reservation.qrCode = qr_code_base64
            room.status = 'ocupado'
            reservation.save()
            room.save()

            send_mail(
                'Teste',
                'Por favor, encontre o QR Code para sua reserva abaixo.',
                settings.DEFAULT_FROM_EMAIL,
                [reservation.user.email],
                fail_silently=False,
                html_message=f'<p>Por favor, encontre o QR Code para sua reserva abaixo.</p><img src="data:image/png;base64,{qr_code_base64}" alt="QR Code"/>'
            )

            serializer = ReservationSerializer(reservation)

            response = {
                'data': serializer.data,
                'message': "Check-in realizado com sucesso."
            }

            return Response(response, status=status.HTTP_200_OK)

    except Reservation.DoesNotExist:
        return Response({"detail": "Reserva não encontrada."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
