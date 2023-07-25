from django.shortcuts import render

room_list = [
    {'id': 1, 'name': 'Room 1'},
    {'id': 2, 'name': 'Room 2'},
    {'id': 3, 'name': 'Room 3'}
]

def home(request):
    return render(request, 'base/home.html', {'rooms': room_list})

def room(request,pk):
    room = None
    for i in room_list:
        if i['id'] == int(pk):
            room = i
            break
    return render(request, 'base/room.html', {'room': room})

