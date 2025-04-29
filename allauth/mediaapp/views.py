from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from allauth.account.forms import LoginForm

# def custom_login_view(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             user = authenticate(request, username=form.cleaned_data['login'], password=form.cleaned_data['password'])
#             if user is not None:
#                 login(request, user)
#                 return redirect('home')  # Redirect to your homepage after login
#             else:
#                 messages.error(request, "Invalid credentials")
#     else:
#         form = LoginForm()
    
#     return render(request, 'account/login.html', {'form': form})
from django.contrib.auth import logout
from django.shortcuts import redirect

def custom_logout_view(request):
    logout(request)  # This logs out the user
    return redirect('account_login')  # Redirect to the login page after logging out



from django.shortcuts import render, redirect
from allauth.account.forms import SignupForm
from allauth.account.utils import complete_signup
from allauth.account import app_settings

def custom_signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(request)  # Save the user
            return complete_signup(request, user, app_settings.EMAIL_VERIFICATION, 'home')  # Redirect after signup
    else:
        form = SignupForm()

    return render(request, 'account/signup.html', {'form': form})



from django.shortcuts import render
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin

def custom_password_reset_view(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save(
                request=request,
                use_https=request.is_secure(),
                email_template_name='account/password_reset_email.html',
                subject_template_name='account/password_reset_subject.txt',
            )
            return render(request, 'account/password_reset_done.html')
    else:
        form = PasswordResetForm()

    return render(request, 'account/password_reset.html', {'form': form})


from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

def custom_change_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important for keeping the user logged in after password change
            messages.success(request, 'Your password was successfully updated!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'account/password_change.html', {'form': form})



from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

class EmailChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']

@login_required
def custom_change_email_view(request):
    if request.method == 'POST':
        form = EmailChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your email has been updated!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = EmailChangeForm(instance=request.user)
    
    return render(request, 'account/change_email.html', {'form': form})





from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from allauth.account.forms import LoginForm
from django.http import HttpResponseRedirect

def custom_login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        remember_me = request.POST.get('remember_me', False)  # Get the 'remember me' value from the form
        if form.is_valid():
            # Manually authenticate the user
            user = authenticate(request, username=form.cleaned_data['login'], password=form.cleaned_data['password'])
            if user is not None:
                # Log in the user
                login(request, user)
                # Handle the "Remember Me" functionality
                if remember_me:
                    request.session.set_expiry(1209600)  # 2 weeks expiry for "Remember Me"
                else:
                    request.session.set_expiry(0)  # Session expires on browser close
                return HttpResponseRedirect('/')  # Redirect to the homepage or desired URL after login
            else:
                messages.error(request, "Invalid login credentials")
        else:
            messages.error(request, "Error in the form")
    else:
        form = LoginForm()

    return render(request, 'account/login.html', {'form': form})




