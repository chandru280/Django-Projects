import qrcode
from django.shortcuts import render, get_object_or_404
from .forms import QRCodeForm, QRCodeForm2
from .models import *
from io import BytesIO
from django.core.files import File
from django.urls import reverse

def generate_qr(request):
    form = QRCodeForm()
    img_url = None

    if request.method == 'POST':
        form = QRCodeForm(request.POST)
        if form.is_valid():
            qr_instance = form.save(commit=False)

            qr = qrcode.make(qr_instance.data)
            buffer = BytesIO()
            qr.save(buffer, format='PNG')
            filename = f'qr_{qr_instance.data}.png'
            qr_instance.image.save(filename, File(buffer), save=True)

            img_url = qr_instance.image.url

    return render(request, 'qr_generator.html', {'form': form, 'img_url': img_url})




def generate_qr2(request):
    form = QRCodeForm2()
    img_url = None

    if request.method == 'POST':
        form = QRCodeForm2(request.POST, request.FILES)
        if form.is_valid():
            qr_instance = form.save(commit=False)

            qr_text = f"Name: {qr_instance.name}\nAddress: {qr_instance.address}\nEmail: {qr_instance.email}\nContact: {qr_instance.contact}"
            qr = qrcode.make(qr_text)
            buffer = BytesIO()
            qr.save(buffer, format='PNG')
            filename = f'qr_{qr_instance.name}.png'
            qr_instance.image.save(filename, File(buffer), save=True)

            qr_instance.save()
            img_url = qr_instance.image.url

    return render(request, 'datas.html', {'form': form, 'img_url': img_url})







def generate_qr3(request):
    form = QRCodeForm()
    img_url = None

    if request.method == 'POST':
        form = QRCodeForm(request.POST, request.FILES)
        if form.is_valid():
            qr_instance = form.save(commit=False)
            qr_instance.save()

            # Build URL to detail page (e.g., /qr/5/)
            url = request.build_absolute_uri(
                reverse('qr_detail', args=[qr_instance.id])
            )

            # Generate QR code that links to the detail page
            qr_img = qrcode.make(url)
            buffer = BytesIO()
            qr_img.save(buffer, format='PNG')
            filename = f'qr_{qr_instance.id}.png'

            # Save QR image to the instance
            qr_instance.image.save(filename, File(buffer), save=True)

            img_url = qr_instance.image.url

    return render(request, 'datas.html', {'form': form, 'img_url': img_url})


def qr_detail(request, pk):
    qr = get_object_or_404(QRCode2, pk=pk)
    print('qr',qr)
    return render(request, 'qr_detail.html', {'qr': qr})
