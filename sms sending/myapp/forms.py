from django import forms

class WhatsAppForm(forms.Form):
    to = forms.CharField(label='Recipient Number', max_length=15, help_text='Format: +1234567890')
    message = forms.CharField(widget=forms.Textarea, label='Message')



class SMSSendForm(forms.Form):
    to = forms.CharField(
        label='Recipient Number',
        max_length=15,
        help_text='Enter the recipient\'s phone number in E.164 format, e.g., +1234567890'
    )
    body = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4}),
        label='Message'
    )


    # forms.py
from django import forms

class SendMessageForm(forms.Form):
    phone = forms.CharField(label="Phone Number", max_length=15, widget=forms.TextInput(attrs={'placeholder': 'Enter phone number'}))
    message = forms.CharField(label="Message", widget=forms.Textarea(attrs={'placeholder': 'Enter your message'}))
