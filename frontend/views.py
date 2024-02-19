# frontend/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm as UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render
from .models import Instrument
from .forms import InstrumentForm

# def login(req):
#     return render(req, 'frontend/login.html')

def landing(req):
    data = {'data': [
        {
        'title': 'Cecilio 4-4 CVNAE-Black+SR Ebony Fitted',
        'description': 'Welcome to InstrumentHub',
        'image': '/media/images/Rectangle 241.png',
        'price': 'Rs 5000'
        },{
        'title': 'Hand Carved Coconut Karimba Mbira',
        'description': 'Welcome to InstrumentHub',
        'image': '/media/images/Rectangle 242.png',
        'price': 'Rs 5300'
        },{
        'title': 'Mendini MDS80-BK Complete Full Size',
        'description': 'Welcome to InstrumentHub',
        'image': '/media/images/Rectangle 243.png',
        'price': 'Rs 4000'
        },{
        'title': 'Rizatti Bronco RB31GW Diatonic Accc',
        'description': 'Welcome to InstrumentHub',
        'image': '/media/images/Rectangle 244.png',
        'price': 'Rs 34900'
        },{
        'title': 'Z ZTDM Professional Alto Eb Saxophone',
        'description': 'Welcome to InstrumentHub',
        'image': '/media/images/Rectangle 250.png',
        'price': 'Rs 2399'
        },{
        'title': 'Rizatti Bronco RB31GW Diatonic Accc',
        'description': 'Welcome to InstrumentHub',
        'image': '/media/images/Rectangle 244.png',
        'price': 'Rs 5000'
        },{
        'title': 'Hand Carved Coconut Karimba Mbira',
        'description': 'Welcome to InstrumentHub',
        'image': '/media/images/Rectangle 242.png',
        'price': 'Rs 5500'
        },{
        'title': 'Mendini MDS80-BK Complete Full Size',
        'description': 'Welcome to InstrumentHub',
        'image': '/media/images/Rectangle 243.png',
        'price': 'Rs 5000'
        }
    ]}
    return render(req, 'frontend/landing.html', data)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # Save the user and additional data
            user = form.save()

            # Log the user in
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            # login(request, user)

            # Redirect to the login page using reverse
            return redirect(reverse('login'))
    else:
        form = UserCreationForm()

    return render(request, 'frontend/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        print(request.POST)
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()

    return render(request, 'frontend/login.html', {'form': form})

def dashboard(request):
    return render(request, 'frontend/dashboard.html')

def user_logout(request):
    logout(request)
    return render(request, 'frontend/login.html')


def users(request):
    # if user is superuser the get all users
    if request.user.is_superuser:
        users = User.objects.all().values('username', 'first_name', 'last_name', 'email')
        return render(request, 'frontend/users.html', {'users': users})
    else:
        return render(request, 'frontend/dashboard.html')
    
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        user.delete()
        return redirect('your_user_list_view')  # Redirect to your user list view



def add_instrument(request):
    if request.method == 'POST':
        form = InstrumentForm(request.POST, request.FILES)
        if form.is_valid():
            instrument = form.save()
            return render(request, 'add_instrument.html', {'instrument': instrument})
    else:
        form = InstrumentForm()

    return render(request, 'frontend/add_instrument.html', {'form': form})
