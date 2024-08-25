from rest_framework.exceptions import ValidationError
from api.models import User, Address, PersonalData


def create_user(data):
    if User.objects.filter(email=data.get('email')).exists():
        raise ValidationError('Já existe um usuário com este email')

    address_data = data.get('address')
    address = None
    if address_data:
        address = Address.objects.create(
            zipCode=address_data.get('zipCode'),
            street=address_data.get('street'),
            number=address_data.get('number'),
            city=address_data.get('city'),
            uf=address_data.get('uf')
        )
    personalData = None
    personalData_data = data.get('personalData')
    if personalData_data:
        personalData = PersonalData.objects.create(
            name=personalData_data.get('name'),
            documentNumber=personalData_data.get('documentNumber'),
            mobile=personalData_data.get('mobile')
        )
    user = User.objects.create(
        email=data.get('email'),
        password=data.get('password'),
        role=data.get('role'),
        personalData=personalData,
        address=address
    )
    return user


def get_address_data(address):
    try:
        return {
            'zipCode': address.zipCode,
            'street': address.street,
            'number': address.number,
            'city': address.city,
            'uf': address.uf
        }
    except AttributeError:
        return None


def get_personal_data(personal_data):
    try:
        return {
            'name': personal_data.name,
            'documentNumber': personal_data.documentNumber,
            'mobile': personal_data.mobile
        }
    except AttributeError:
        return None


def get_user_data(user):
    try:
        return {
            'id': user.id,
            'email': user.email,
            'personalData': get_personal_data(user.personalData),
            'address': get_address_data(user.address)
        }
    except AttributeError:
        return None
