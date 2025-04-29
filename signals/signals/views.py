# views.py

from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Student
from .forms import StudentForm
from django.core.signals import got_request_exception





# views.py
import logging

logger = logging.getLogger(__name__)

def my_view(request):
    logger.info("User visited this page!")
    logger.warning("Page is taking too long to load!")
    logger.error("Page crashed due to some error!")
    return HttpResponse("Check your console for logs!")













# READ (List all students)
def student_list(request):
    try:
        students = Student.objects.all()
        
        # Force an error
        # print(10 / 0)

        return render(request, 'student_list.html', {'students': students})

    except Exception as e:
        got_request_exception.send(sender=Student, exception=e)
        return render(request, 'student_list.html', {'error':e})




  
# CREATE
def student_create(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'student_form.html', {'form': form})

# UPDATE
def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'student_form.html', {'form': form})

# DELETE
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        return redirect('student_list')
    return render(request, 'student_confirm_delete.html', {'student': student})



from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

# Login view
def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have logged in successfully.")
            return redirect('home')  # Redirect to home after login
        else:
            messages.error(request, "Invalid credentials.")
    return render(request, 'login.html')

# Logout view
def logout_view(request):
    logout(request)
    messages.success(request, "You have logged out successfully.")
    return redirect('home')  # Redirect to home after logout

# Registration view
def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful. You can now log in.")
            return redirect('login')  # Redirect to login page after successful registration
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})



