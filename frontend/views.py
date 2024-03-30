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
from django.contrib.auth.forms import PasswordResetForm
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.core.mail import EmailMessage
# from InstrumentHUB.InstrumentHUB import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from .tokens import generate_token
from django.core.mail import send_mail
from django.utils.html import strip_tags
from .forms import  InstrumentForm
from . import views
from .forms import RentForm

# def login(req):
#     return render(req, 'frontend/login.html')

def landing(req):
    data=Instrument.objects.all()
    for item in data:
        item.image=item.image.url if item.image else None
    return render(req, 'frontend/landing.html',{'data':data})

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
            if user.is_superuser:
                return redirect('dashboard')
            return redirect('customer_dashboard')
    else:
        form = AuthenticationForm()

    return render(request, 'frontend/login.html', {'form': form})

def dashboard(request):
    instruments = Instrument.objects.all()
    total_instruments= instruments.count()
    total_users= User.objects.all().count()
    meta_data= {
        'total_instruments':total_instruments,
        'total_users':total_users,
    }
    for instrument in list(instruments):
       instrument.image = instrument.image.url if instrument.image else None
    return render(request, 'frontend/dashboard.html',{'instrument':instruments,'meta_data':meta_data})
def customer_dashboard(request):
    instruments = Instrument.objects.all()
    
    for instrument in list(instruments):
       instrument.image = instrument.image.url if instrument.image else None
    return render(request, 'frontend/Customerdashboard.html',{'instrument':instruments})


def user_logout(request):
    logout(request)
    return render(request, 'frontend/login.html')


def users(request):
    # if user is superuser the get all users
    if request.user.is_superuser:
        users = User.objects.all().values('id','username', 'first_name', 'last_name', 'email')
        return render(request, 'frontend/users.html', {'users': users})
    else:
        return render(request, 'frontend/dashboard.html')
    
def delete_user(request, user_id):
    print(request.user)
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('users')

    



def add_instrument(request):
    if request.method == 'POST':
        form = InstrumentForm(request.POST, request.FILES)
        if form.is_valid():
            # form.user=request.user
            instrument = form.save()
            instrument.user=request.user
            instrument.save()
            messages.success(request, 'Instrument added successfully')
            return redirect('dashboard')
    else:
        form = InstrumentForm()

    return render(request, 'frontend/add_instrument.html', {'form': form})


def ForgetPassword(request):
    
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
           
            if not User.objects.filter(email=username).first():
                messages.error(request, 'No user found with this username.')
                return redirect('/forget-password/')
            myuser = User.objects.get(email=username)

            # Email Address Confirmation Email
            current_site = get_current_site(request)
            email_subject = "Verify your email @ Rents!"
            message = render_to_string('frontend/email_reset.html',{
                'name':myuser.first_name,
                'domain':current_site.domain,
                'username':myuser.username,
                'token': generate_token.make_token(myuser),
            })
            plain_message = strip_tags(message)

            send_mail(
            email_subject,
            plain_message,
            "np03cs4a210040@heraldcollege.edu.np",  # Sender's email address
            [myuser.email],  # Recipient's email address
            html_message=message,)

            return render(request, 'frontend/password_reset_done.html')
            

# def send_quotation_email(
#     self, items, recipient_email, sender_details=None, cc_emails=None
# (sad)
#     subject = "Quotation Details"
#     html_message = render_to_string(
#         "purchase_order/quotation/default_template.html",
#         {"items": items, "sender": sender_details},
#     )
#     plain_message = strip_tags(
#         html_message
#     )  # Strip HTML tags for the plain text version

#     send_mail(
#         subject,
#         plain_message,
#         "dev.optixtec@gmail.com",  # Sender's email address
#         recipient_email,  # Recipient's email address
#         html_message=html_message,
#     )
#     return "Done"


    except Exception as e:
        print(e)
    return render(request , "frontend/forget-password.html")

def changePassword(request, username, token):
    
    
    myuser = User.objects.get(username=username)

    try:

        if request.method == 'POST':
            raw_password = request.POST['new_password']
            confirm_password = request.POST['reconfirm_password']
            myuser.set_password(raw_password)
            myuser.save()


            if  raw_password != confirm_password:
                messages.success(request, 'both should  be equal.')
                return redirect(f'/change-password/{token}/')
            
            return redirect('login')

    except Exception as e:
        print(e)
    return render(request , "frontend/change-password.html")

def about_us(request):
    return render(request,"frontend/Aboutus.html")

def contact_us(request):
    return render(request,"frontend/Contact_US.html")

def livelistings(request):
    instruments = Instrument.objects.all()
    
    for instrument in list(instruments):
       instrument.image = instrument.image.url if instrument.image else None
       print(instrument.image)
    return render(request, "frontend/livelistings.html", {"instrument": instruments})
# class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'frontend/password_reset.html'
    subject_template_name = 'users/password_reset_subject'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('users-home')      

def password_reset_done(request):
    return render(request,'frontend/password_reset_done.html')

def instrument_update(request, id):
    
    try:
        instrument_obj = Instrument.objects.get(id=id)

        #if instrument_obj.user != request.user:
         #   return redirect('/')
        if instrument_obj.user==request.user:
            form = InstrumentForm(request.POST, request.FILES,instance=instrument_obj)
            if form.is_valid():
                instrument = form.save()
                messages.success(request, 'Instrument updated successfully')
                return redirect('dashboard')
            else:
                form = InstrumentForm()

            return render(request, 'frontend/update_instruments.html', {'item': instrument_obj})
       # else:

    except Exception as e:
        print(e)

        return render(request,'frontend/update_instruments.html')

def instrument_delete(request, id):
    print('instrument delete')
    instrument = get_object_or_404(Instrument, id=id)
    if instrument.user== request.user:
        instrument.delete()
    return redirect('dashboard')

def instrument_details(request,id):
    instruments = Instrument.objects.get(id=id)
    instruments.image=instruments.image.url if instruments.image else None
    return render(request, "frontend/instrument_details.html", {"instrument_obj": instruments})
 
def my_listings(request):
    instruments = Instrument.objects.filter(user=request.user)
    for instrument in list(instruments):
       instrument.image = instrument.image.url if instrument.image else None
    return render(request, 'frontend/my_listings.html',{'instruments':instruments})

# def search_view(request):
    query = request.GET.get('q')
    if query:
        instruments = Instrument.objects.filter(name__icontains=query)
    else:
        instruments = Instrument.objects.all()
    return render(request, 'frontend/search_results.html', {'instruments': instruments, 'query': query})



def rent_instrument(request):
    if request.method == 'POST':
        form = RentForm(request.POST)
        print(form.data)
        if form.is_valid():
            form.renter=request.user
            form.instrument_id=1
            instrument = form.save()
            instrument.save()
            messages.success(request, 'Instrument has been  Rented')
            return redirect('dashboard')
    else:
        form = RentForm()

    return render(request, 'frontend/rent_instrument.html', {'form': form})