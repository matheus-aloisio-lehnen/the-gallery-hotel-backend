from datetime import datetime

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.models import Room, Reservation
from api.serializers import RoomSerializer
from api.services.room_service import check_room_availability


@api_view(['GET'])
def get_all(request):
    try:
        rooms = Room.objects.all()
        serializer = RoomSerializer(rooms, many=True)
        return Response({'data': serializer.data})
    except Room.DoesNotExist:
        return Response('Não foi possível encontrar quartos cadastrados', status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_one(request, id):
    try:
        room = Room.objects.get(pk=id)
        serializer = RoomSerializer(room)
        return Response(serializer.data)
    except Room.DoesNotExist:
        return Response('Quarto não encontrado', status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def create(request):
    try:
        data = request.data
        room = Room.objects.create(
            price=data.get('price'),
            description=data.get('description')
        )
        serializer = RoomSerializer(room)
        response = {
            'message': 'Quarto criado com sucesso!',
            'data': serializer.data
        }
        return Response(response, status=status.HTTP_201_CREATED)
    except Exception as e:
        print(f"Erro ao criar o usuário: {e}")
        return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
def delete(request, id):
    try:
        room = Room.objects.get(id=id)
        room.delete()
        response = {
            'data': True,
            'message': 'Quarto excluído com sucesso!'
        }
        return Response(response, status=status.HTTP_200_OK)
    except Room.DoesNotExist:
        return Response({'message': 'Quarto não encontrado.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'message': 'Erro interno do servidor. Detalhes: ' + str(e)},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def is_available(request):
    roomId = request.GET.get('roomId')
    startDateStr = request.GET.get('startDate')
    endDateStr = request.GET.get('endDate')

    if not roomId or not startDateStr or not endDateStr:
        return Response('Parâmetros inválidos', status=status.HTTP_400_BAD_REQUEST)

    try:
        startDate = datetime.strptime(startDateStr, '%Y-%m-%d')
        endDate = datetime.strptime(endDateStr, '%Y-%m-%d')
    except ValueError:
        return Response('Formato de data inválido', status=status.HTTP_400_BAD_REQUEST)

    available = check_room_availability(roomId, startDate, endDate)

    if available is None:
        return Response('Quarto não encontrado', status=status.HTTP_404_NOT_FOUND)

    response = {
        'data': available,
        'message': '' if available else 'Este quarto não tem vaga para o período selecionado'
    }
    return Response(response)