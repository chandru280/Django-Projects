from django.shortcuts import render, redirect, get_object_or_404
from .models import Staff, Student, Event, Notification
from .forms import StaffForm, StudentForm, EventForm
from django.contrib.auth.decorators import login_required

# Staff CRUD
@login_required
def create_staff(request):
    if request.method == 'POST':
        form = StaffForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('staff_list')
    else:
        form = StaffForm()
    return render(request, 'staff_form.html', {'form': form})

@login_required
def update_staff(request, pk):
    staff = get_object_or_404(Staff, pk=pk)
    if request.method == 'POST':
        form = StaffForm(request.POST, instance=staff)
        if form.is_valid():
            form.save()
            return redirect('staff_list')
    else:
        form = StaffForm(instance=staff)
    return render(request, 'staff_form.html', {'form': form})

@login_required
def delete_staff(request, pk):
    staff = get_object_or_404(Staff, pk=pk)
    if request.method == 'POST':
        staff.delete()
        return redirect('staff_list')
    return render(request, 'confirm_delete.html', {'object': staff})

@login_required
def list_staff(request):
    staffs = Staff.objects.all()
    return render(request, 'staff_list.html', {'staffs': staffs})

# Student CRUD
@login_required
def create_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'student_form.html', {'form': form})

@login_required
def update_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'student_form.html', {'form': form})

@login_required
def delete_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        return redirect('student_list')
    return render(request, 'confirm_delete.html', {'object': student})

@login_required
def list_student(request):
    students = Student.objects.all()
    return render(request, 'student_list.html', {'students': students})

# Event creation and notification
@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user.staff
            event.save()
            students = Student.objects.all()
            for student in students:
                Notification.objects.create(event=event, student=student)
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'event_form.html', {'form': form})

@login_required
def list_event(request):
    events = Event.objects.all()
    return render(request, 'event_list.html', {'events': events})







from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to a home page or another page
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout as auth_logout

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('home')  # Redirect to home or another page after login
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout(request):
    auth_logout(request)
    return redirect('login')  # Redirect to login page or home page after logout








from django.http.response import JsonResponse, HttpResponse
from django.views.decorators.http import require_GET, require_POST
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from webpush import send_user_notification
import json
from django.conf import settings


@require_GET
def home(request):
   webpush_settings = getattr(settings, 'WEBPUSH_SETTINGS', {})
   vapid_key = webpush_settings.get('VAPID_PUBLIC_KEY')
   user = request.user
   return render(request, 'home.html', {user: user, 'vapid_key': vapid_key})


@require_POST
@csrf_exempt
def send_push(request):
    try:
        body = request.body
        data = json.loads(body)

        if 'head' not in data or 'body' not in data or 'id' not in data:
            return JsonResponse(status=400, data={"message": "Invalid data format"})

        user_id = data['id']
        user = get_object_or_404(User, pk=user_id)
        payload = {'head': data['head'], 'body': data['body']}
        send_user_notification(user=user, payload=payload, ttl=1000)

        return JsonResponse(status=200, data={"message": "Web push successful"})
    except TypeError:
        return JsonResponse(status=500, data={"message": "An error occurred"})
    






from pywebpush import webpush, WebPushException
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import base64
from django.http import JsonResponse

def generate_vapid_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    public_key = private_key.public_key()
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    public_key_b64 = base64.urlsafe_b64encode(public_pem).decode().rstrip("=")
    private_key_b64 = base64.urlsafe_b64encode(private_pem).decode().rstrip("=")

    return {
        'publicKey': public_key_b64,
        'privateKey': private_key_b64
    }

def key(request):
    keys = generate_vapid_keys()
    return JsonResponse({
        "VAPID Public Key": keys['publicKey'],
        "VAPID Private Key": keys['privateKey']
    })



# "VAPID Public Key": "LS0tLS1CRUdJTiBQVUJMSUMgS0VZLS0tLS0KTUlJQklqQU5CZ2txaGtpRzl3MEJBUUVGQUFPQ0FROEFNSUlCQ2dLQ0FRRUFxcTQvZDA2NitaMndSSENCRjNURApSUXJrYU4vK2gxUkhlMExoVThnSlZHSUN5YThGTlhOR0FHaERxNFR6TFNmTUJYYUFNK1JRWU9vd2xlN3ZWdHBvCllUMWcyVjNwV3ZCK25mY0NYRE5mUVB5S1BsWG5NSko0NDNDV0lING9mSHppdEJmVFBRcGFDTU9leUpRN3VPQnUKV09pL1R0ZDBTTThPbHVGR1NxeHhTRUJ0MmZLVVA2SjZJZXRQR0lxSnQyTHB1SWlrbmxtazdZbzhya3Z1cEQ4eAp2ZlFjMnd1MkFJSzc4dThOZ0tBTUpLVFM1OGdPWTROUGNKSVJST1NRMk13SW9ZRm9kTEF5eVJsS1BoNTRRTDVmCks5enorVGpxbG85TTJOeTEvTWpXNng0dVVYQ0JJZGUzUlJPc2NIZHRZRDJ2WkpZaXZ5VnVTazIwZXplQmVLWEIKN3dJREFRQUIKLS0tLS1FTkQgUFVCTElDIEtFWS0tLS0tCg",

# "VAPID Private Key": "LS0tLS1CRUdJTiBQUklWQVRFIEtFWS0tLS0tCk1JSUV2d0lCQURBTkJna3Foa2lHOXcwQkFRRUZBQVNDQktrd2dnU2xBZ0VBQW9JQkFRQ3FyajkzVHJyNW5iQkUKY0lFWGRNTkZDdVJvMy82SFZFZDdRdUZUeUFsVVlnTEpyd1UxYzBZQWFFT3JoUE10Sjh3RmRvQXo1RkJnNmpDVgo3dTlXMm1oaFBXRFpYZWxhOEg2ZDl3SmNNMTlBL0lvK1ZlY3drbmpqY0pZZ2ZpaDhmT0swRjlNOUNsb0l3NTdJCmxEdTQ0RzVZNkw5TzEzUkl6dzZXNFVaS3JIRklRRzNaOHBRL29ub2g2MDhZaW9tM1l1bTRpS1NlV2FUdGlqeXUKUys2a1B6Rzk5QnpiQzdZQWdydnk3dzJBb0F3a3BOTG55QTVqZzA5d2toRkU1SkRZekFpaGdXaDBzRExKR1VvKwpIbmhBdmw4cjNQUDVPT3FXajB6WTNMWDh5TmJySGk1UmNJRWgxN2RGRTZ4d2QyMWdQYTlrbGlLL0pXNUtUYlI3Ck40RjRwY0h2QWdNQkFBRUNnZ0VBQ0daZG0rZzFXTkRqT3BCZTMySDd0T0RUQk9aTDNIL1AvM0pNZ2V4aVU5TjUKclB0VUY2RlRYSjhhVlhmMjVTTlptSENRaS8wOGgzTXB3NkhvQ0MrUGhpN3R5VVRQUUk1OWJNREVvNkpUbWNYVAo5K1ZsRDFybUN0WWc5L3NTMEZoRkZVcVJqQ1lxUllGN0d3YWw1SFN4enVaYXpwZlpQVGErSjd3YjB0T25Ha0J5Ck44M1VCTzlnTXY3bElvM3BrQ2VtUVFacCtMRU9YZ3ZLNEs0bkFMY1B2djdUMHFtMFo5MTBYTXAwVDhzMWVGbW0KVlY2Ryt1RndpbU1ydjZzYmhCa0hzamxvdEkwSWYvUGVwdWVaSThWZmE4MnVCK05PeUV2UVFPakRISVd0YmM4SwpjN2tnNm1jTnphRGxMZTRlc3dCTjhLbTUrUWdKaTB2ZDlpU3pIMDR4UVFLQmdRRGNUYTlRYmh2a2FLTEtqQTdKCmNaRS82YXlBakNHUU9yZ3ZSdTV2WFlWMWJjMndia2lSRk9XZzl1dHZma08xL1RTdTl2anRlTGxVMVJYaURQMHEKeFAzdmlPVG1xV29XTjZUZEVCMnU3V1pQbitQSzloWUdkWDZNcUpVWk1wVUVTYlJkd3ZIRHhieVpoQkZDUkt5SwphNXVjVzFwUW1SSWJDM1AyalNiYkxyTXh1UUtCZ1FER1ZpNDRFRlNMS2hBWndodkJSZFFlS285K29EWjJXQTlCCkFyNzlucmVWR1ZhUVNkTEdaWHlaRDE1dnk1UlRWT2lTZ1B4S0x6b1kvblU5NmpYaDljL3AyWTR6QWZTS1BBV0YKMUVzVEkycHU2VG9aYjlKMS9pWEVYVWcrN0cycGdQNFBhVWJQdEpUTmxsdWVBNzB2Um1sOHJxdXZOODBQNHFyZApuL2E2RkJVRTV3S0JnUUNFb0FmdzViakk4dTA5L3I5UUtweUUyNHBNQVJDYm9aNE1hQ2xXeGZoNFQxaEs1TG12CkRlT0gyZDYyeWs2OUd1aENoTkFyTmtoc2Q3T3EyS0w0d29zVlQxWnVQb050U0tacHB6QVhoVGZZcTZzWkhyajMKdm5nbStiNTQ0dWl2SWlnQllrRGwyUDdIZEtobk9xeWMwRmRuODk4Vk1uR2g4bTBuZXFadndWZURrUUtCZ1FDKwppYXg5VDdMb3Z0QVk3dEdiSzJwTVVMYnAveUJUTU9YMm5weTlLZTFUMzdPNWlqSmpScndjanhjNmIybGZaUUxKClBBRWpnNXRjeDVmNmt6YVFqWVhnTXBEWmo5ZE50YnZZaGNwWjZId25jUWZQeUExNExXQTY5U0tpMEovSlo1S3IKVzRnYm9uQVIwWkRTak9VQ3RiSkJoY3lKMkNHNFVSbTFNQ2ZuTzhPMW9RS0JnUUN6QmpXMWZoMFNwNmRGSTBiUQpQZGVPdU1NNlRZdVNBY1NHWHByZFBIRDdURThKNXpNUGs5K2V5NjBiMEVqU05aZGFqZWM3MmJTcEkyZGh2d3cxCnd1S2N0djQ3emVuNVBIMmpqRzI4cG9WcDd1SzdoT3ZaME13ZnVaS1lvbzNicmFvbmJyTnhrTDdDYytKNGRQbysKb0N1cE94YlpWdnVNWWp2WmtmMy9uZ3luQWc9PQotLS0tLUVORCBQUklWQVRFIEtFWS0tLS0tCg"




# views.py
from django.shortcuts import render
from django.http import JsonResponse
from django_webpush import send_user_notification
from .models import Notification, WebPushSubscription
from django.contrib.auth.decorators import login_required

@login_required
def subscribe(request):
    """Handle subscription to push notifications."""
    if request.method == 'POST':
        subscription_info = request.POST.get('subscription_info')  # Get subscription details from frontend
        # Save subscription details to the database
        WebPushSubscription.objects.update_or_create(
            user=request.user,
            defaults={'subscription': subscription_info}
        )
        return JsonResponse({"status": "subscribed"})

@login_required
def send_notification(request):
    """Send notification to a specific user."""
    # Example notification: when a staff creates a test detail
    notification = Notification.objects.create(user=request.user, message="New test created!")
    
    # Payload to be sent in the notification
    payload = {
        "head": "New Notification",
        "body": notification.message,
        "icon": "/static/icons/notification.png",  # Your icon path
        "url": "/some-url/"  # URL to redirect the user to when they click the notification
    }
    
    # Send the notification to the user
    send_user_notification(user=request.user, payload=payload, ttl=1000)
    
    return JsonResponse({"status": "sent"})
