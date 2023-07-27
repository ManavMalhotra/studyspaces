from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Room, Topic, Message
from .forms import RoomForm
from django.contrib import messages


# room_list = [
#     {'id': 1, 'name': 'Room 1'},
#     {'id': 2, 'name': 'Room 2'},
#     {'id': 3, 'name': 'Room 3'}
# ]


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    room_list = Room.objects.filter(Q(topic__name__contains=q) )
    topic = Topic.objects.all()
    room_count = room_list.count()
    context = {'rooms': room_list, 'topics': topic, 'room_count': room_count}
    return render(request, 'base/home.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('-created')
    room_participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    

    context = {'room' : room, 'room_messages': room_messages, 'room_participants': room_participants}
    return render(request, 'base/room.html', context)

@login_required(login_url='login')
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

@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse('You are not allowed here!')
    
    if request.method == 'POST':
        print('Printing POST:', request.POST)
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('/')
    
    context = {'form': form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)   

    if request.method == 'POST':
        room.delete()
        return redirect('/')

    return render(request, 'base/delete.html', {"obj": room})

@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)   

    if request.user != message.user:
        return HttpResponse('You are not allowed here!')
    
    if request.method == 'POST':
        message.delete()
        return redirect('home')

    return render(request, 'base/delete.html', {"obj": message})

def loginView(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        username = str(request.POST.get('username')).lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User doesn't exist")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, "Username OR password is incorrect")

    context = {'page': page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

def registerUser(request):
    page = 'register'

    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = str(user.username).lower()
            user.save()
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, "An error has occurred during registration")
    context = {'page': page}
    return render(request, 'base/login_register.html', {'form': form})