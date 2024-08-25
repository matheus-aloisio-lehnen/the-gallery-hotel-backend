from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.models import User, PersonalData, Address
from api.serializers import UserSerializer
from api.services.user_service import create_user


@api_view(['GET'])
def get_all(request):
    try:
        staffs = User.objects.filter(role='recepcionista')
        serializer = UserSerializer(staffs, many=True)
        return Response({'data': serializer.data})
    except User.DoesNotExist:
        return Response('Não foi possível encontrar colaboradores cadastrados', status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_one(request, id):
    try:
        user = User.objects.get(pk=id)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    except User.DoesNotExist:
        return Response('Usuário não encontrado', status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def create(request):
    try:
        data = request.data
        userCreated = create_user(data)
        serializer = UserSerializer(userCreated)
        response = {
            'message': 'Usuário criado com sucesso!',
            'data': serializer.data
        }
        return Response(response, status=status.HTTP_201_CREATED)
    except Exception as e:
        print(f"Erro ao criar o usuário: {e}")
        return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
def delete(request, id):
    try:
        user = User.objects.get(id = id)
        user.delete()
        response = {
            'data': True,
            'message': 'Usuário excluído com sucesso!'
        }
        return Response(response, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'message': 'Usuário não encontrado.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'message': 'Erro interno do servidor. Detalhes: ' + str(e)},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
