from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view

from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from api.models import User, PersonalData, Address
from api.serializers import UserSerializer


def on_air(request):
    return HttpResponse('On Air!')


def hello_world(request):
    return HttpResponse('Hello World!')


@api_view(['GET'])
def get_user(request, id):
    try:
        user = User.objects.get(pk=id)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    except User.DoesNotExist:
        return Response({'error': 'Usuário não encontrado.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def create_user(request):
    try:
        data = request.data
        address_data = data.get('address')
        address = None
        if address_data:
            address = Address.objects.create(
                zip_code=address_data.get('zipCode'),
                street=address_data.get('street'),
                number=address_data.get('number'),
                city=address_data.get('city'),
                uf=address_data.get('uf')
            )
        personal_data = None
        personal_data_data = data.get('personalData')
        if personal_data_data:
            personal_data = PersonalData.objects.create(
                name=personal_data_data.get('name'),
                document_number=personal_data_data.get('documentNumber'),
                mobile=personal_data_data.get('mobile')
            )
        user = User.objects.create(
            email=data.get('email'),
            password=data.get('password'),
            role=data.get('role'),
            personal_data=personal_data,
            address=address
        )
        serializer = UserSerializer(user)
        response = {
            'message': 'Usuário criado com sucesso!',
            'data': serializer.data
        }
        return Response(response, status=status.HTTP_201_CREATED)
    except Exception as e:
        print(f"Erro ao criar o usuário: {e}")
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def sign_in(request):
    try:
        data = request.data
        email = data.get('email')
        password = data.get('password')

        user = User.objects.filter(email=email).first()
        if user is not None and password == user.password:
            access_token = AccessToken.for_user(user)
            return Response({
                'data': {
                    'token': str(access_token),
                    'user': {
                        'id': user.id,
                        'email': user.email,
                        'role': user.role,
                    }
                },
                'message': f'Seja bem vindo {user.personal_data.name}'
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Credenciais inválidas.'}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
