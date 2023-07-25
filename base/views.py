from django.shortcuts import render
from .models import Room

# room_list = [
#     {'id': 1, 'name': 'Room 1'},
#     {'id': 2, 'name': 'Room 2'},
#     {'id': 3, 'name': 'Room 3'}
# ]


def home(request):
    room_list = Room.objects.all()
    context = room_list
    return render(request, 'base/home.html', {'rooms': context})

def room(request, pk):
    room = Room.objects.get(id=pk)
    context = {'id': room.id, 'name': room.name}
    return render(request, 'base/room.html', {'room': context})

def createRoom(request):
    return render(request, 'base/room_form.html')