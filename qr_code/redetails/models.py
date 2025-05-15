from django.db import models

class QRCode(models.Model):
    data = models.CharField(max_length=255)
    image = models.ImageField(upload_to='qrcodes/', blank=True)

    def __str__(self):
        return self.data



class QRCode2(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    email = models.EmailField()
    contact = models.CharField(max_length=15)
    extra_image = models.ImageField(upload_to='extra_images/', blank=True, null=True)
    
    data = models.CharField(max_length=255)
    image = models.ImageField(upload_to='qrcodes/', blank=True)

    def __str__(self):
        return f"{self.name} - {self.data}"
