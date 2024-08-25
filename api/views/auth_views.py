from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from api.models import User


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
                'message': f'Seja bem vindo {user.personalData.name}'
            }, status=status.HTTP_200_OK)
        else:
            return Response('Credenciais inválidas' , status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)