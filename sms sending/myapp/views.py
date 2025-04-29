from django.shortcuts import render, redirect
from django.conf import settings
from twilio.rest import Client
from .forms import WhatsAppForm, SMSSendForm
from .models import *


def send_whatsapp(request):
    if request.method == 'POST':
        form = WhatsAppForm(request.POST)
        if form.is_valid():
            to_number = 'whatsapp:' + form.cleaned_data['to']
            message_body = form.cleaned_data['message']
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            try:
                message = client.messages.create(
                    body=message_body,
                    from_=settings.TWILIO_WHATSAPP_NUMBER,
                    to=to_number
                )
                return render(request, 'success.html', {'message_sid': message.sid})
            except Exception as e:
                form.add_error(None, f"An error occurred: {str(e)}")
    else:
        form = WhatsAppForm()
    return render(request, 'send_whatsapp.html', {'form': form})



 
def send_sms(request):
    if request.method == 'POST':
        form = SMSSendForm(request.POST)
        if form.is_valid():
            to_number = form.cleaned_data['to']
            message_body = form.cleaned_data['body']

            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            try:
                message = client.messages.create(
                    body=message_body,
                    from_=settings.TWILIO_PHONE_NUMBER,
                    to=to_number
                )
                SMS.objects.create(
                    user=request.user,
                    to=to_number,
                    body=message_body
                )
                return render(request, 'success.html', {'message_sid': message.sid, 'to_number': to_number})
            except Exception as e:
                form.add_error(None, f"An error occurred: {str(e)}")
    else:
        form = SMSSendForm()
    return render(request, 'send_sms.html', {'form': form})




from django.http import HttpResponse
from twilio.twiml.messaging_response import MessagingResponse

def incoming_message(request):
    # Get the incoming message body
    incoming_msg = request.POST.get('Body', '')
    response = MessagingResponse()

    # Reply to the incoming message
    response.message(f"You said: {incoming_msg}")
    return HttpResponse(str(response), content_type='text/xml')



# views.py
from django.shortcuts import render
from django.http import HttpResponse
from .forms import SendMessageForm
from .services import send_whatsapp_message

def send_message_view(request):
    if request.method == "POST":
        form = SendMessageForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone']
            message = form.cleaned_data['message']
            
            result = send_whatsapp_message(phone_number, message)
            return HttpResponse(f"Message sent successfully. Response: {result}")
        else:
            return HttpResponse("Form is invalid. Please correct the errors.", status=400)
    else:
        form = SendMessageForm()
    
    return render(request, 'send_message.html', {'form': form})
