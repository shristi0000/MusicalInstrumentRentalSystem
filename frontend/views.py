# frontend/views.py
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin

# from InstrumentHUB.InstrumentHUB import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage, send_mail
from django.db.models import CharField, DurationField, ExpressionWrapper, F, Sum, Value
from django.db.models.functions import Coalesce, Concat, ExtractDay, TruncDate
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils.html import strip_tags

from . import views
from .forms import CustomUserCreationForm as UserCreationForm
from .forms import InstrumentForm, RentForm
from .models import Instrument, RentInstruments
from .tokens import generate_token

# def login(req):
#     return render(req, 'frontend/login.html')


def landing(req):
    data = Instrument.objects.all()
    for item in data:
        item.image = item.image.url if item.image else None
    return render(req, "frontend/landing.html", {"data": data})


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # Save the user and additional data
            user = form.save()

            # Log the user in
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(request, username=username, password=password)
            # login(request, user)

            # Redirect to the login page using reverse
            return redirect(reverse("login"))
    else:
        form = UserCreationForm()

    return render(request, "frontend/register.html", {"form": form})


def user_login(request):
    if request.method == "POST":
        print(request.POST)
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("dashboard")
    else:
        form = AuthenticationForm()

    return render(request, "frontend/login.html", {"form": form})


def dashboard(request):
    if request.user.is_superuser:
        instruments = Instrument.objects.all()
    else:
        instruments = Instrument.objects.filter(user=request.user)
    total_instruments = instruments.count()

    meta_data = {
        "total_instruments": total_instruments,
        "total_users": (
            User.objects.all().count() if request.user.is_superuser else None
        ),
    }
    for instrument in list(instruments):
        if instrument.status is None:
            instrument.status = "Available"
        instrument.image = instrument.image.url if instrument.image else None
    return render(
        request,
        "frontend/dashboard.html",
        {"instrument": instruments, "meta_data": meta_data},
    )


def customer_dashboard(request):
    instruments = Instrument.objects.all()

    for instrument in list(instruments):
        instrument.image = instrument.image.url if instrument.image else None
    return render(
        request, "frontend/Customerdashboard.html", {"instrument": instruments}
    )


def user_logout(request):
    logout(request)
    return render(request, "frontend/login.html")


def users(request):
    # if user is superuser the get all users
    if request.user.is_superuser:
        users = User.objects.all().values(
            "id", "username", "first_name", "last_name", "email"
        )
        return render(request, "frontend/users.html", {"users": users})
    else:
        return render(request, "frontend/dashboard.html")


def delete_user(request, user_id):
    print(request.user)
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect("users")


def add_instrument(request):
    if request.method == "POST":
        form = InstrumentForm(request.POST, request.FILES)
        if form.is_valid():
            # form.user=request.user
            instrument = form.save()
            instrument.user = request.user
            instrument.status = "Available"
            instrument.save()
            messages.success(request, "Instrument added successfully")
            return redirect("dashboard")
    else:
        form = InstrumentForm()

    return render(request, "frontend/add_instrument.html", {"form": form})


def ForgetPassword(request):

    try:
        if request.method == "POST":
            username = request.POST.get("username")

            if not User.objects.filter(email=username).first():
                messages.error(request, "No user found with this username.")
                return redirect("/forget-password/")
            myuser = User.objects.get(email=username)

            # Email Address Confirmation Email
            current_site = get_current_site(request)
            email_subject = "Verify your email @ Rents!"
            message = render_to_string(
                "frontend/email_reset.html",
                {
                    "name": myuser.first_name,
                    "domain": current_site.domain,
                    "username": myuser.username,
                    "token": generate_token.make_token(myuser),
                },
            )
            plain_message = strip_tags(message)

            send_mail(
                email_subject,
                plain_message,
                "np03cs4a210040@heraldcollege.edu.np",  # Sender's email address
                [myuser.email],  # Recipient's email address
                html_message=message,
            )

            return render(request, "frontend/password_reset_done.html")

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
    return render(request, "frontend/forget-password.html")


def changePassword(request, username, token):

    myuser = User.objects.get(username=username)

    try:

        if request.method == "POST":
            raw_password = request.POST["new_password"]
            confirm_password = request.POST["reconfirm_password"]
            myuser.set_password(raw_password)
            myuser.save()

            if raw_password != confirm_password:
                messages.success(request, "both should  be equal.")
                return redirect(f"/change-password/{token}/")

            return redirect("login")

    except Exception as e:
        print(e)
    return render(request, "frontend/change-password.html")


def about_us(request):
    return render(request, "frontend/Aboutus.html")


def contact_us(request):
    return render(request, "frontend/Contact_US.html")


def livelistings(request):
    instruments = Instrument.objects.all()

    for instrument in list(instruments):
        if instrument.status is None:
            instrument.status = "Available"
        instrument.image = instrument.image.url if instrument.image else None
        print(instrument.images)
    return render(request, "frontend/livelistings.html", {"instrument": instruments})
    # class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = "frontend/password_reset.html"
    subject_template_name = "users/password_reset_subject"
    success_message = (
        "We've emailed you instructions for setting your password, "
        "if an account exists with the email you entered. You should receive them shortly."
        " If you don't receive an email, "
        "please make sure you've entered the address you registered with, and check your spam folder."
    )
    success_url = reverse_lazy("users-home")


def password_reset_done(request):
    return render(request, "frontend/password_reset_done.html")


def instrument_update(request, id):

    try:
        instrument_obj = Instrument.objects.get(id=id)

        # if instrument_obj.user != request.user:
        #   return redirect('/')
        if instrument_obj.user == request.user:
            form = InstrumentForm(request.POST, request.FILES, instance=instrument_obj)
            if form.is_valid():
                instrument = form.save()
                messages.success(request, "Instrument updated successfully")
                return redirect("dashboard")
            else:
                form = InstrumentForm()

            return render(
                request, "frontend/update_instruments.html", {"item": instrument_obj}
            )
    # else:

    except Exception as e:
        print(e)

        return render(request, "frontend/update_instruments.html")


def instrument_delete(request, id):
    print("instrument delete")
    instrument = get_object_or_404(Instrument, id=id)
    if instrument.user == request.user:
        instrument.delete()
    return redirect("dashboard")


def instrument_details(request, id):
    instruments = Instrument.objects.get(id=id)
    instruments.image = instruments.image.url if instruments.image else None
    return render(
        request, "frontend/instrument_details.html", {"instrument_obj": instruments}
    )


def my_listings(request):
    instruments = Instrument.objects.filter(user=request.user)
    for instrument in list(instruments):
        instrument.image = instrument.image.url if instrument.image else None
    return render(request, "frontend/my_listings.html", {"instruments": instruments})


def instrument_reports(request):
    if request.user.is_superuser:
        instruments = RentInstruments.objects.values(
            "id",
            "instrument__name",
            "status",
            "date",
            "pickup_date",
            "dropoff_date",
            "pickup_address",
            "dropoff_address",
            "renter__email",
        ).annotate(
            owner_name=Concat(
                F("instrument__user__first_name"),
                Value(" "),
                F("instrument__user__last_name"),
                output_field=CharField(),
            ),
            renter_name=Concat(
                F("renter__first_name"),
                Value(" "),
                F("renter__last_name"),
                output_field=CharField(),
            ),
            rented_days=ExpressionWrapper(
                F("dropoff_date") - F("pickup_date"), output_field=DurationField()
            ),
        )
    else:
        instruments = (
            RentInstruments.objects.filter(instrument__user=request.user)
            .values(
                "id",
                "instrument__name",
                "status",
                "date",
                "pickup_date",
                "dropoff_date",
                "pickup_address",
                "dropoff_address",
                "renter__email",
            )
            .annotate(
                owner_name=Concat(
                    F("instrument__user__first_name"),
                    Value(" "),
                    F("instrument__user__last_name"),
                    output_field=CharField(),
                ),
                renter_name=Concat(
                    F("renter__first_name"),
                    Value(" "),
                    F("renter__last_name"),
                    output_field=CharField(),
                ),
                rented_days=ExpressionWrapper(
                    F("dropoff_date") - F("pickup_date"), output_field=DurationField()
                ),
            )
        )
    # Extract days component

    for obj in instruments:
        if obj["rented_days"].days == 0 or obj["rented_days"].days == 1:
            obj["rented_days"] = "1 day"
        else:
            obj["rented_days"] = str(obj["rented_days"].days) + " days"
    return render(
        request, "frontend/instrument_reports.html", {"instruments": instruments}
    )


def my_rentals(request):
    instruments = (
        RentInstruments.objects.filter(renter=request.user)
        .values(
            "id",
            "instrument__name",
            "status",
            "date",
            "pickup_date",
            "dropoff_date",
            "pickup_address",
            "dropoff_address",
            "renter__email",
        )
        .annotate(
            owner_name=Concat(
                F("instrument__user__first_name"),
                Value(" "),
                F("instrument__user__last_name"),
                output_field=CharField(),
            ),
            renter_name=Concat(
                F("renter__first_name"),
                Value(" "),
                F("renter__last_name"),
                output_field=CharField(),
            ),
            rented_days=ExpressionWrapper(
                F("dropoff_date") - F("pickup_date"), output_field=DurationField()
            ),
        )
    )
    # Extract days component

    for obj in instruments:
        if obj["rented_days"].days == 0 or obj["rented_days"].days == 1:
            obj["rented_days"] = "1 day"
        else:
            obj["rented_days"] = str(obj["rented_days"].days) + " days"
    return render(request, "frontend/my_rentals.html", {"instruments": instruments})


def rent_instrument(request, instrument_id):
    if request.method == "POST":
        post_data = request.POST.copy()  # Make a mutable copy
        post_data["renter"] = request.user
        instrument = Instrument.objects.get(id=instrument_id)
        post_data["instrument"] = instrument
        post_data["status"] = "Accepted"

        form = RentForm(post_data)

        if form.is_valid():
            rent_instrument = form.save()
            instrument.status = "Rented"
            instrument.save()
            messages.success(request, "Instrument has been Rented")
            return redirect("dashboard")
    else:
        form = RentForm()

    return render(
        request,
        "frontend/rent_instrument.html",
        {"form": form, "instrument_id": instrument_id},  # Corrected context
    )


def return_instrument(request, id):
    rent_instrument = RentInstruments.objects.get(id=id)
    rent_instrument.status = "Returned"
    rent_instrument.save()
    instrument = Instrument.objects.get(id=rent_instrument.instrument.id)
    instrument.status = "Available"
    instrument.save()
    return redirect("my_rentals")

from .forms import ImagesForm
from .models import Image

def index(request):
    images = Image.objects.all()
    context = {'images': images}
    return render(request, "add_instrument.html", context)
def fileupload(request):
    form = ImagesForm(request.POST, request.FILES)
    if request.method == 'POST':
        images = request.FILES.getlist('pic')
        for image in images:
            image_ins = Image(pic = image)
            image_ins.save()
        return redirect('index')
    context = {'form': form}
    return render(request, "instrument_details.html", context)

# def post_detailview(request, id):
   
#   if request.method == 'POST':
#     cf = CommentForm(request.POST or None)
#     if cf.is_valid():
#       content = request.POST.get('content')
#       comment = Comment.objects.create(post = post, user = request.user, content = content)
#       comment.save()
#       return redirect(post.get_absolute_url())
#     else:
#       cf = CommentForm()
       
#     context ={
#       'comment_form':cf,
#       }
#     return render(request, 'frontend / instrument_details.html', context)

# def notification_page_view(request):
#     return render(request,'frontend/notification_page.html')