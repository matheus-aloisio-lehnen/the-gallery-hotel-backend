from rest_framework import serializers
from .models import Address, PersonalData, User, Room, Reservation


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

class PersonalDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalData
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    personalData = PersonalDataSerializer()
    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'role', 'personalData', 'address']
        extra_kwargs = {
            'password': {'write_only': True}
        }

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

class ReservationSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    room = RoomSerializer()

    class Meta:
        model = Reservation
        fields = '__all__'