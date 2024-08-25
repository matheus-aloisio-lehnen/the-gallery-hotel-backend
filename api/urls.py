from django.urls import path
from .views import room_views, auth_views, staff_views, home_views, reservation_views, dash_views

urlpatterns = [
    path('on-air', home_views.on_air, name = 'on_air'),
    path('', home_views.hello_world, name = 'hello_world'),

    path('auth/sign-in', auth_views.sign_in, name='sign_in'),

    path('staff/get-all', staff_views.get_all, name='get_all_staffs'),
    path('staff/<int:id>', staff_views.get_one, name='get_staff'),
    path('staff/create', staff_views.create, name='create_staff'),
    path('staff/delete/<int:id>', staff_views.delete, name='delete_staff'),

    path('room/get-all', room_views.get_all, name='get_all_rooms'),
    path('room/<int:id>', room_views.get_one, name='get_room'),
    path('room/create', room_views.create, name='create_room'),
    path('room/delete/<int:id>', room_views.delete, name='delete_room'),
    path('room/is-available', room_views.is_available, name='is_room_available'),

    path('reservation/get-all', reservation_views.get_all, name='get_all_reservations'),
    path('reservation/create', reservation_views.create, name='create_reservation'),
    path('reservation/delete/<int:id>', reservation_views.delete, name='delete_reservation'),

    path('dash/get-all', dash_views.get_all, name='get_all_dash'),
    path('dash/checkout/<int:id>', dash_views.checkout, name='checkout'),
    path('dash/checkin', dash_views.checkin, name='checkin'),
]
