from django.shortcuts import render, redirect
from .models import Room
from .forms import RoomForm

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
    form = RoomForm()

    if request.method == 'POST':
        print('Printing POST:', request.POST)
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    context =  {'form': form}
    return render(request, 'base/room_form.html', context)

def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    
    if request.method == 'POST':
        print('Printing POST:', request.POST)
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('/')
    
    context = {'form': form}

    return render(request, 'base/room_form.html', context)

def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)   
    
    if request.method == 'POST':
        room.delete()
        return redirect('/')

    return render(request, 'base/delete.html', {"obj": room})