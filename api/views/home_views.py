from django.http import HttpResponse
import sqlite3


def on_air(request):
    return HttpResponse('On Air!')


def hello_world(request):
    return HttpResponse('Hello World!')

