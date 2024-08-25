from datetime import datetime, timedelta

from django.utils import timezone
from django.utils.dateparse import parse_date
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.models import Reservation, Room
from api.serializers import ReservationSerializer
from api.services.reservation_service import create_reservation
from api.services.room_service import check_room_availability


def get_month_range(month_index, year=None):
    if year is None:
        year = datetime.now().year

    first_day_of_month = datetime(year, month_index, 1)
    next_month = first_day_of_month.replace(day=28) + timedelta(days=4)
    last_day_of_month = next_month - timedelta(days=next_month.day)

    return first_day_of_month, last_day_of_month

@api_view(['GET'])
def get_all(request):
    month = request.GET.get('month')
    year = request.GET.get('year', datetime.now().year)

    # Verifica se `month` e `year` são válidos
    try:
        month = int(month)
        year = int(year)
    except ValueError:
        return Response('Parâmetros de mês ou ano inválidos', status=status.HTTP_400_BAD_REQUEST)

    # Calcular o primeiro e o último dia do mês
    first_day_of_month = datetime(year, month, 1)
    last_day_of_month = (first_day_of_month + timedelta(days=31)).replace(day=1) - timedelta(days=1)

    rooms = Room.objects.all()
    data = []
    days = [(first_day_of_month + timedelta(days=i)).strftime('%d') for i in range((last_day_of_month - first_day_of_month).days + 1)]

    for room in rooms:
        room_data = {
            'id': room.id,
            'description': room.description,
            'reservations': [],
            'dailyStatus': {day: False for day in days}
        }

        reservations = Reservation.objects.filter(
            room=room,
            startDate__lte=last_day_of_month,
            endDate__gte=first_day_of_month
        )

        for reservation in reservations:
            # Preservar informações da reserva
            reservation_data = ReservationSerializer(reservation).data
            room_data['reservations'].append(reservation_data)

            # Atualizar o status diário para o período da reserva
            start_date_str = str(reservation.startDate)
            end_date_str = str(reservation.endDate)
            start_date = parse_date(start_date_str)
            end_date = parse_date(end_date_str)

            if start_date and end_date:
                current_date = start_date
                while current_date <= end_date:
                    room_data['dailyStatus'][current_date.strftime('%d')] = True
                    current_date += timedelta(days=1)

        data.append(room_data)

    response = {
        'data': data
    }
    return Response(response)

@api_view(['GET'])
def get_one(request, id):
    try:
        room = Reservation.objects.get(pk=id)
        serializer = ReservationSerializer(room)
        return Response(serializer.data)
    except Reservation.DoesNotExist:
        return Response('Reserva não encontrada', status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def create(request):
    data = request.data
    roomId = data.get('roomId')
    startDateStr = data.get('startDate')
    endDateStr = data.get('endDate')

    if not roomId or not startDateStr or not endDateStr:
        return Response('Parâmetros inválidos', status=status.HTTP_400_BAD_REQUEST)

    try:
        startDate = datetime.strptime(startDateStr, '%Y-%m-%d')
        endDate = datetime.strptime(endDateStr, '%Y-%m-%d')
    except ValueError:
        return Response('Formato de data inválido', status=status.HTTP_400_BAD_REQUEST)

    available = check_room_availability(roomId, startDate, endDate)
    if not available:
        return Response('Este quarto não tem vaga para o período selecionado', status=status.HTTP_400_BAD_REQUEST)

    result = create_reservation(data)

    response = {
        'data': result,
        'message': 'Reserva criada com sucesso!'
    }
    return Response(response, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
def delete(request, id):
    try:
        reservation = Reservation.objects.get(id=id)
        room = reservation.room
        reservation.delete()
        today = timezone.now().date()
        if reservation.startDate <= today <= reservation.endDate:
            # Atualizar o status do quarto para 'vago'
            room.status = 'vago'
            room.save()
        response = {
            'data': True,
            'message': 'Reserva excluída com sucesso!'
        }
        return Response(response, status=status.HTTP_200_OK)
    except Reservation.DoesNotExist:
        return Response({'message': 'Reserva não encontrado.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'message': 'Erro interno do servidor. Detalhes: ' + str(e)},
                         status=status.HTTP_500_INTERNAL_SERVER_ERROR)